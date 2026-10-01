from entities.editorial import Editorial
from repositories.impl.csv_archivo_repositorio_impl import CSVArchivoRepositorioImpl


class CSVArchivoRepositorioEditorialImpl(CSVArchivoRepositorioImpl[Editorial]):

    def __init__(self, ruta_archivo: str = "/editoriales.csv"):
        super().__init__(
            ruta_archivo=ruta_archivo,
            clase_entidad=Editorial
        )