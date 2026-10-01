from batch.proceso_automatico import ProcesoAutomatico
from config.config import config
from preload_data.preload_data import DATOS_PRECARGA
from preload_data.proceso_precarga import ProcesoPrecarga
from ui.consola_principal import ConsolaPrincipal
from ui.consola_catalogo import ConsolaCatalogo
from services.servicio_catalogo import ServicioCatalogo
from ui.consola_inventario import ConsolaInventario
from ui.consola_precios import ConsolaPrecios
from ui.consola_stock import ConsolaStock
from services.servicio_inventario import ServicioInventario
from repositories.impl.csv_archivo_repositorio_libro_impl import CSVArchivoRepositorioLibro
from repositories.impl.csv_archivo_repositorio_precio_impl import CSVArchivoRepositorioPrecioImpl
from repositories.impl.csv_archivo_repositorio_stock_impl import CSVArchivoRepositorioStockImpl
from ui.consola_editoriales import ConsolaEditoriales
from ui.consola_generos import ConsolaGeneros
from ui.consola_monedas import ConsolaMonedas
from ui.consola_tipos_cotizacion import ConsolaTiposCotizacion
from ui.consola_cotizaciones import ConsolaCotizaciones
from ui.consola_gestion_cotizaciones import ConsolaGestionCotizaciones
from services.servicio_cotizacion import ServicioCotizacion
from repositories.impl.csv_archivo_repositorio_cotizacion_impl import CSVArchivoRepositorioCotizacion
from services.servicio_genero import ServicioGenero
from services.servicio_moneda import ServicoMoneda
from services.servicio_tipo_cotizacion import ServicioTipoCotizacion
from repositories.impl.csv_archivo_repositorio_genero_impl import CSVArchivoRepositorioGeneroImpl
from repositories.impl.csv_archivo_repositorio_moneda_impl import CSVArchivoRepositorioMoneda
from repositories.impl.csv_archivo_repositorio_tipo_cotizacion_impl import CSVArchivoRepositorioTipoCotizacion
from services.servicio_editorial import ServicioEditorial
from repositories.impl.csv_archivo_repositorio_editorial_impl import (
    CSVArchivoRepositorioEditorialImpl,
)


def main(import_default_data: bool = False, interactive: bool = True) -> None:
    if import_default_data:
        ProcesoPrecarga().ejecutar(
            carpeta_destino=config.directorio_repositorio,
            datos=DATOS_PRECARGA,
        )

    repositorio_editorial = CSVArchivoRepositorioEditorialImpl(
        ruta_archivo=str(config.ruta_repositorio(config.repositorio_editoriales))
    )
    servicio_editorial = ServicioEditorial(repositorio_editorial)
    servicio_genero = ServicioGenero(CSVArchivoRepositorioGeneroImpl(
        ruta_archivo=str(config.ruta_repositorio(config.repositorio_generos))
    ))
    repositorio_moneda = CSVArchivoRepositorioMoneda(
        ruta_archivo=str(config.ruta_repositorio(config.repositorio_monedas))
    )
    servicio_moneda = ServicoMoneda(repositorio_moneda)
    repositorio_libro = CSVArchivoRepositorioLibro(
        ruta_archivo=str(config.ruta_repositorio(config.repositorio_libros))
    )
    repositorio_precio = CSVArchivoRepositorioPrecioImpl(
        ruta_archivo=str(config.ruta_repositorio(config.repositorio_precios))
    )
    repositorio_stock = CSVArchivoRepositorioStockImpl(
        ruta_archivo=str(config.ruta_repositorio(config.repositorio_stock))
    )
    servicio_inventario = ServicioInventario(
        repositorio_libro=repositorio_libro,
        repositorio_precio=repositorio_precio,
        repositorio_stock=repositorio_stock,
        repositorio_moneda=repositorio_moneda,
    )
    servicio_catalogo = ServicioCatalogo(
        repositorio=repositorio_libro,
        servicio_editorial=servicio_editorial,
        servicio_genero=servicio_genero,
        servicio_inventario=servicio_inventario,
        repositorio_precio=repositorio_precio,
        repositorio_stock=repositorio_stock,
    )
    repositorio_tipo = CSVArchivoRepositorioTipoCotizacion(
        ruta_archivo=str(config.ruta_repositorio(config.repositorio_tipos_cotizacion))
    )
    servicio_tipo = ServicioTipoCotizacion(repositorio_tipo)
    servicio_cotizacion = ServicioCotizacion(
        CSVArchivoRepositorioCotizacion(
            ruta_archivo=str(config.ruta_repositorio(config.repositorio_cotizaciones))
        ),
        repositorio_moneda,
        repositorio_tipo,
    )

    if interactive:
        ConsolaPrincipal(
            catalogo=ConsolaCatalogo(servicio=servicio_catalogo),
            inventario=ConsolaInventario(
                precios=ConsolaPrecios(servicio=servicio_inventario),
                stock=ConsolaStock(servicio=servicio_inventario),
            ),
            editoriales=ConsolaEditoriales(servicio=servicio_editorial),
            generos=ConsolaGeneros(servicio=servicio_genero),
            monedas=ConsolaMonedas(servicio=servicio_moneda),
            cotizaciones=ConsolaCotizaciones(
                tipos=ConsolaTiposCotizacion(servicio=servicio_tipo),
                cotizaciones=ConsolaGestionCotizaciones(servicio=servicio_cotizacion),
            ),
        ).ejecutar()
    else:
        ProcesoAutomatico(
            servicio_editorial=servicio_editorial,
            servicio_genero=servicio_genero,
            servicio_moneda=servicio_moneda,
            servicio_tipo=servicio_tipo,
            servicio_catalogo=servicio_catalogo,
            servicio_inventario=servicio_inventario,
            servicio_cotizacion=servicio_cotizacion,
        ).ejecutar()

if __name__ == "__main__":
    import_default_data: bool = True
    interactive: bool = True
    
    main(import_default_data, interactive)
