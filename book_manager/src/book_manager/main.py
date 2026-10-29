"""Inicializa los repositorios y servicios y ejecuta la consola de la librería.

Al ejecutar este módulo directamente, genera los SQL y recrea las tablas
con los datos de precarga antes de iniciar la consola.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from config.config import config
from database.connection import ConexionDB, ContextManager
from migrations.migrations import ProcesoMigracion
from preload_data.preload_data import ProcesoPrecarga
from ui.console import ConsolaGeneral
from repositories.repositories import (
    RepositorioAuditoria,
    RepositorioTipoCotizacion,
    RepositorioMoneda,
    RepositorioEditorial,
    RepositorioGenero,
    RepositorioCotizacion,
    RepositorioLibro,
    RepositorioPrecio,
    RepositorioStock,
)
from services.services import (
    ServicioAuditoria,
    ServicioTipoCotizacion,
    ServicoMoneda,
    ServicioEditorial,
    ServicioGenero,
    ServicioCotizacion,
    ServicioCatalogo,
    ServicioInventario,
)


def main(import_default_data: bool = False) -> None:
    """Construye las dependencias de la aplicación e inicia el menú principal.

    Carga DATABASE_URL del entorno o de book_manager/.env y comparte un
    ContextManager entre los repositorios de base de datos. Si se
    solicita, genera los SQL desde los CSV, recrea las tablas y carga los datos
    antes de iniciar la consola, respetando el orden de ProcesoMigracion. Libera las
    conexiones del motor al terminar, incluso si ocurre un error.

    Args:
        import_default_data: Si es True, genera los SQL y reemplaza las tablas
            y sus datos mediante ProcesoPrecarga.
            Por defecto, utiliza los datos existentes en la base de datos.

    Raises:
        FileNotFoundError: Si no existe la carpeta de CSV o falta un SQL.
        ValueError: Si falta DATABASE_URL o la migración encuentra datos
            inválidos. Interrumpe el inicio.
    """
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    url = os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("La variable DATABASE_URL no está definida.")

    conexion = ConexionDB(url)
    try:
        contexto = ContextManager(conexion)
        repositorio_tipos = RepositorioTipoCotizacion(contexto)
        repositorio_monedas = RepositorioMoneda(contexto)
        repositorio_editoriales = RepositorioEditorial(contexto)
        repositorio_generos = RepositorioGenero(contexto)
        repositorio_cotizaciones = RepositorioCotizacion(contexto)
        repositorio_libros = RepositorioLibro(contexto)
        repositorio_precios = RepositorioPrecio(contexto)
        repositorio_stock = RepositorioStock(contexto)
        repositorio_auditoria = RepositorioAuditoria(contexto)
        servicio_auditoria = ServicioAuditoria(repositorio_auditoria)

        servicio_tipo_cotizacion = ServicioTipoCotizacion(
            repositorio=repositorio_tipos,
            repositorio_cotizacion=repositorio_cotizaciones,
            servicio_auditoria=servicio_auditoria,
        )
        servicio_moneda = ServicoMoneda(
            repositorio=repositorio_monedas,
            repositorio_cotizacion=repositorio_cotizaciones,
            repositorio_precio=repositorio_precios,
            servicio_auditoria=servicio_auditoria,
        )
        servicio_editorial = ServicioEditorial(
            repositorio=repositorio_editoriales,
            repositorio_libro=repositorio_libros,
            servicio_auditoria=servicio_auditoria,
        )
        servicio_genero = ServicioGenero(
            repositorio=repositorio_generos,
            repositorio_libro=repositorio_libros,
            servicio_auditoria=servicio_auditoria,
        )
        servicio_cotizacion = ServicioCotizacion(
            repositorio=repositorio_cotizaciones,
            repositorio_moneda=repositorio_monedas,
            repositorio_tipo_cotizacion=repositorio_tipos,
            servicio_auditoria=servicio_auditoria,
        )
        servicio_catalogo = ServicioCatalogo(
            repositorio=repositorio_libros,
            repositorio_editorial=repositorio_editoriales,
            repositorio_genero=repositorio_generos,
            repositorio_precio=repositorio_precios,
            repositorio_stock=repositorio_stock,
            servicio_auditoria=servicio_auditoria,
        )
        servicio_inventario = ServicioInventario(
            repositorio_libro=repositorio_libros,
            repositorio_precio=repositorio_precios,
            repositorio_stock=repositorio_stock,
            repositorio_moneda=repositorio_monedas,
            servicio_auditoria=servicio_auditoria,
        )

        if import_default_data:
            print("Generando archivos SQL desde los CSV...")
            carpeta_sqls = Path(__file__).resolve().parent / "migrations" / "sql"
            ProcesoMigracion.migrar_datos(
                carpeta_csvs=str(config.directorio_repositorio),
                carpeta_sqls=str(carpeta_sqls),
            )
            print(f"Archivos SQL generados en: {carpeta_sqls}")
            proceso_precarga = ProcesoPrecarga(conexion)
            proceso_precarga.importar_datos(str(carpeta_sqls))

        consola = ConsolaGeneral(
            servicio_editorial=servicio_editorial,
            servicio_genero=servicio_genero,
            servicio_moneda=servicio_moneda,
            servicio_tipo_cotizacion=servicio_tipo_cotizacion,
            servicio_cotizacion=servicio_cotizacion,
            servicio_catalogo=servicio_catalogo,
            servicio_inventario=servicio_inventario,
        )
        consola.ejecutar()
    finally:
        conexion.close()


if __name__ == "__main__":
    main(False)
