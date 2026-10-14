"""Recrea las tablas de la aplicación y carga los inserts SQL de migración."""

from pathlib import Path

from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from database.connection import ConexionDB, ContextManager
from migrations.migrations import ProcesoMigracion
from models.models import Base


class ProcesoPrecarga:
    """Reemplaza las tablas del modelo y sus datos mediante archivos SQL."""

    def __init__(self, conexion: ConexionDB):
        """Recibe la conexión de la aplicación, sin asumir su cierre."""
        self.contexto = ContextManager(conexion)

    def importar_datos(self, carpeta_sqls: str) -> None:
        """Verifica los SQL, recrea las tablas y ejecuta los inserts en orden.

        Usa una transacción de PostgreSQL para confirmar los cambios o
        revertirlos si falla la recreación o la carga. La recreación elimina
        los datos y los objetos asociados a las tablas anteriores.

        Args:
            carpeta_sqls: Carpeta con los ocho archivos SQL de migración.

        Raises:
            FileNotFoundError: Si la carpeta o alguno de los SQL no existe.
            ValueError: Si alguno de los archivos SQL está vacío.
            RuntimeError: Si falla la ejecución de un archivo SQL.
        """
        scripts = self._leer_sqls(Path(carpeta_sqls))

        with self.contexto.transaction() as session:
            conexion = session.connection()
            Base.metadata.drop_all(conexion)
            Base.metadata.create_all(conexion)

            for nombre, contenido in scripts:
                try:
                    # No dividir por ';': ese carácter puede estar dentro de textos.
                    with conexion.connection.driver_connection.cursor() as cursor:
                        cursor.execute(contenido)
                except Exception as error:
                    raise RuntimeError(f"No se pudo ejecutar {nombre}: {error}") from error

            self._sincronizar_ids(session)

        print(f"Precarga completada: tablas recreadas y {len(scripts)} archivos SQL cargados.")

    @staticmethod
    def _leer_sqls(carpeta: Path) -> list[tuple[str, str]]:
        """Verifica y lee todos los SQL antes de modificar la base de datos."""
        if not carpeta.is_dir():
            raise FileNotFoundError(f"No existe la carpeta de SQL: {carpeta}")

        scripts = []
        for tabla in ProcesoMigracion.ORDEN_TABLAS:
            archivo = carpeta / f"{tabla}.sql"
            if not archivo.is_file():
                raise FileNotFoundError(f"No existe el archivo: {archivo}")

            contenido = archivo.read_text(encoding="utf-8-sig")
            if not contenido.strip():
                raise ValueError(f"El archivo está vacío: {archivo.name}")
            scripts.append((archivo.name, contenido))

        return scripts

    @staticmethod
    def _sincronizar_ids(session: Session) -> None:
        """Ajusta las secuencias después de cargar IDs explícitos en los inserts."""
        preparador = session.connection().dialect.identifier_preparer

        for tabla in Base.metadata.sorted_tables:
            if "id" not in tabla.c:
                continue

            secuencia = session.scalar(
                text("SELECT pg_get_serial_sequence(:tabla, 'id')"),
                {"tabla": preparador.format_table(tabla)},
            )
            if secuencia is None:
                continue

            ultimo_id = session.scalar(select(func.max(tabla.c.id)))
            session.execute(
                text("SELECT setval(CAST(:secuencia AS regclass), :valor, :usada)"),
                {
                    "secuencia": secuencia,
                    "valor": ultimo_id if ultimo_id is not None else 1,
                    "usada": ultimo_id is not None,
                },
            )
