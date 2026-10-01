from typing import List, Optional

from entities.genero import Genero
from repositories.impl.csv_archivo_repositorio_genero_impl import (
    CSVArchivoRepositorioGeneroImpl,
)


class ServicioGenero:
    """Gestiona las operaciones CRUD de géneros."""

    def __init__(self, repositorio: CSVArchivoRepositorioGeneroImpl):
        self.repositorio = repositorio

    def guardar(self, genero: Genero) -> Genero:
        """Crea el género si su ID no existe; en caso contrario, lo actualiza."""
        if self.repositorio.leer_por_id(genero.id) is None:
            return self.repositorio.crear(genero)
        return self.repositorio.actualizar(genero)

    def leer_por_id(self, id: int) -> Optional[Genero]:
        """Devuelve el género con el ID indicado, o None si no existe."""
        return self.repositorio.leer_por_id(id)

    def leer_todos(self) -> List[Genero]:
        """Devuelve la lista de géneros del repositorio."""
        return self.repositorio.leer_todos()

    def eliminar(self, id: int) -> bool:
        """Elimina el género y devuelve False si el ID no existe."""
        return self.repositorio.eliminar(id)
