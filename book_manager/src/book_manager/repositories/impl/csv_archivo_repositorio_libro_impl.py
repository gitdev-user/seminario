from entities.libro import Libro
from repositories.impl.csv_archivo_repositorio_impl import CSVArchivoRepositorioImpl


class CSVArchivoRepositorioLibro(CSVArchivoRepositorioImpl[Libro]):

    def __init__(self, ruta_archivo: str = "data/libros.csv"):
        super().__init__(
            ruta_archivo=ruta_archivo,
            clase_entidad=Libro
        )
