"""Genera archivos de inserts SQL a partir de los CSV de migración."""

import csv
import math
from pathlib import Path


class ProcesoMigracion:
    """Lee los CSV y genera un archivo SQL por tabla."""

    ORDEN_TABLAS = (
        "editoriales", "generos", "monedas", "tipos_cotizacion",
        "cotizaciones", "libros", "precios", "stock",
    )

    @staticmethod
    def migrar_datos(carpeta_csvs: str, carpeta_sqls: str):
        """Función encargada de la migración de datos de csv a sql.

        Se encarga de leer los archivos csv y crear los archivos sql
        para la inserción en la base de datos.

        Args:
            carpeta_csvs (str): Carpeta donde se encuentran los archivos csv de origen.
            carpeta_sqls (str): Carpeta donde se deben guardar los archivos sql generados.
        """
        origen = Path(carpeta_csvs)
        destino = Path(carpeta_sqls)
        if not origen.is_dir():
            raise FileNotFoundError(f"No existe la carpeta de CSV: {origen}")
        destino.mkdir(parents=True, exist_ok=True)

        archivos = sorted(
            origen.glob("*.csv"),
            key=lambda archivo: (
                ProcesoMigracion.ORDEN_TABLAS.index(archivo.stem)
                if archivo.stem in ProcesoMigracion.ORDEN_TABLAS
                else len(ProcesoMigracion.ORDEN_TABLAS),
                archivo.name,
            ),
        )
        for archivo_csv in archivos:
            ProcesoMigracion._generar_sql(archivo_csv, destino / f"{archivo_csv.stem}.sql")

    @staticmethod
    def _generar_sql(archivo_csv: Path, archivo_sql: Path) -> None:
        """Lee un CSV, valida sus filas y escribe los INSERT correspondientes."""
        with archivo_csv.open("r", encoding="utf-8-sig", newline="") as entrada:
            lector = csv.reader(entrada)
            columnas = next(lector, [])
            if not columnas:
                raise ValueError(f"CSV sin encabezados: {archivo_csv.name}")

            columnas_sql = [
                "moneda_id" if archivo_csv.stem == "precios" and c == "moneda_base_id" else c
                for c in columnas
            ]
            agregar_id = archivo_csv.stem == "cotizaciones" and "id" not in columnas
            if agregar_id:
                columnas_sql.insert(0, "id")
            campos = ", ".join('"' + c.replace('"', '""') + '"' for c in columnas_sql)
            tabla = '"' + archivo_csv.stem.replace('"', '""') + '"'
            cantidad = 0

            with archivo_sql.open("w", encoding="utf-8") as salida:
                for fila in lector:
                    if not fila:
                        continue
                    if len(fila) != len(columnas):
                        raise ValueError(
                            f"Fila inválida en {archivo_csv.name}, línea {lector.line_num}."
                        )
                    valores = ", ".join(ProcesoMigracion._valor_sql(valor) for valor in fila)
                    if agregar_id:
                        valores = f"{cantidad + 1}, {valores}"
                    salida.write(f"INSERT INTO {tabla} ({campos}) VALUES ({valores});\n")
                    cantidad += 1
            print(f"{archivo_csv.stem}: {cantidad} inserts generados.")

    @staticmethod
    def _valor_sql(valor: str) -> str:
        """Convierte vacíos en NULL, reconoce números y escapa los textos."""
        texto = valor.strip()
        if not texto:
            return "NULL"
        digitos = texto.lstrip("+-")
        if len(digitos) > 1 and digitos.startswith("0") and digitos[1].isdigit():
            return "'" + valor.replace("'", "''") + "'"
        try:
            return str(int(texto))
        except ValueError:
            pass
        try:
            numero = float(texto)
        except ValueError:
            return "'" + valor.replace("'", "''") + "'"
        if not math.isfinite(numero):
            raise ValueError(f"Número no finito: {valor}")
        return str(numero)
