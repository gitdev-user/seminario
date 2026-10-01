from entities.tipo_cotizacion import TipoCotizacion
from repositories.impl.csv_archivo_repositorio_impl import CSVArchivoRepositorioImpl


class CSVArchivoRepositorioTipoCotizacion(CSVArchivoRepositorioImpl[TipoCotizacion]):

    def __init__(self, ruta_archivo: str = "data/tipos_cotizacion.csv"):
        super().__init__(
            ruta_archivo=ruta_archivo,
            clase_entidad=TipoCotizacion
        )
