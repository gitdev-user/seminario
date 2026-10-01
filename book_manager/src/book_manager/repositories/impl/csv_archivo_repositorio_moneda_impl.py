from entities.moneda import Moneda
from repositories.impl.csv_archivo_repositorio_impl import CSVArchivoRepositorioImpl


class CSVArchivoRepositorioMoneda(CSVArchivoRepositorioImpl[Moneda]):

    def __init__(self, ruta_archivo: str = "data/monedas.csv"):
        super().__init__(
            ruta_archivo=ruta_archivo,
            clase_entidad=Moneda
        )
