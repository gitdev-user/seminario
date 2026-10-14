"""Inicializa los repositorios y servicios y ejecuta la consola de la librería.

Al ejecutar este módulo directamente, inicia la aplicación sin precargar datos.
"""

from config.config import config
from preload_data.preload_data import ProcesoPrecarga
from ui.console import ConsolaGeneral
from repositories.repositories import (
    MemoriaRepositorioTipoCotizacion,
    MemoriaRepositorioMoneda,
    MemoriaRepositorioEditorial,
    MemoriaRepositorioGenero,
    MemoriaRepositorioCotizacion,
    MemoriaRepositorioLibro,
    MemoriaRepositorioPrecio,
    MemoriaRepositorioStock,
)
from services.services import (
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

    Crea repositorios en memoria y los comparte entre los servicios. Si se
    solicita, importa los archivos CSV configurados antes de iniciar la consola,
    respetando el orden de las dependencias entre entidades. Los datos se
    conservan únicamente en memoria durante esta ejecución.

    Args:
        import_default_data: Si es True, precarga los datos de los CSV.
            Por defecto, inicia con los repositorios vacíos.

    Raises:
        FileNotFoundError: Si falta un archivo solicitado para la precarga.
        ValueError: Si la precarga encuentra datos inválidos o referencias
            inexistentes. El error interrumpe el inicio de la consola.
    """
    repositorio_tipos = MemoriaRepositorioTipoCotizacion()
    repositorio_monedas = MemoriaRepositorioMoneda()
    repositorio_editoriales = MemoriaRepositorioEditorial()
    repositorio_generos = MemoriaRepositorioGenero()
    repositorio_cotizaciones = MemoriaRepositorioCotizacion()
    repositorio_libros = MemoriaRepositorioLibro()
    repositorio_precios = MemoriaRepositorioPrecio()
    repositorio_stock = MemoriaRepositorioStock()
    
    servicio_tipo_cotizacion = ServicioTipoCotizacion(
        repositorio=repositorio_tipos,
        repositorio_cotizacion=repositorio_cotizaciones,
    )
    servicio_moneda = ServicoMoneda(
        repositorio=repositorio_monedas,
        repositorio_cotizacion=repositorio_cotizaciones,
        repositorio_precio=repositorio_precios,
    )
    servicio_editorial = ServicioEditorial(
        repositorio=repositorio_editoriales,
        repositorio_libro=repositorio_libros,
    )
    servicio_genero = ServicioGenero(
        repositorio=repositorio_generos,
        repositorio_libro=repositorio_libros,
    )
    servicio_cotizacion = ServicioCotizacion(
        repositorio=repositorio_cotizaciones,
    )
    servicio_catalogo = ServicioCatalogo(
        repositorio=repositorio_libros,
        repositorio_editorial=repositorio_editoriales,
        repositorio_genero=repositorio_generos,
        repositorio_precio=repositorio_precios,
        repositorio_stock=repositorio_stock,
    )
    servicio_inventario = ServicioInventario(
        repositorio_libro=repositorio_libros,
        repositorio_precio=repositorio_precios,
        repositorio_stock=repositorio_stock,
        repositorio_moneda=repositorio_monedas,
    )
    
    if import_default_data:
        print("Importando datos predeterminados...")

        archivos = [
            str(config.ruta_repositorio(nombre))
            for nombre in (
                config.repositorio_tipos_cotizacion,
                config.repositorio_monedas,
                config.repositorio_editoriales,
                config.repositorio_generos,
                config.repositorio_cotizaciones,
                config.repositorio_libros,
                config.repositorio_precios,
                config.repositorio_stock,
            )
        ]

        proceso_precarga = ProcesoPrecarga(
            archivos=archivos,
            servicio_tipo_cotizacion=servicio_tipo_cotizacion,
            servicio_moneda=servicio_moneda,
            servicio_editorial=servicio_editorial,
            servicio_genero=servicio_genero,
            servicio_cotizacion=servicio_cotizacion,
            servicio_catalogo=servicio_catalogo,
            servicio_inventario=servicio_inventario,
        )
        proceso_precarga.importar_datos()

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


if __name__ == "__main__":
    main()
