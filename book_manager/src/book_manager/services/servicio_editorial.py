from typing import List, Optional

from entities.editorial import Editorial
from repositories.impl.csv_archivo_repositorio_editorial_impl import (
    CSVArchivoRepositorioEditorialImpl,
)


class ServicioEditorial:
    """Gestiona las operaciones CRUD de editoriales."""

    def __init__(self, repositorio: CSVArchivoRepositorioEditorialImpl):
        self.repositorio = repositorio

    def guardar(self, editorial: Editorial) -> Editorial:
        """Crea la editorial si su ID no existe; en caso contrario, la actualiza."""
        if self.repositorio.leer_por_id(editorial.id) is None:
            return self.repositorio.crear(editorial)
        return self.repositorio.actualizar(editorial)

    def leer_por_id(self, id: int) -> Optional[Editorial]:
        """Devuelve la editorial con el ID indicado, o None si no existe."""
        return self.repositorio.leer_por_id(id)

    def leer_todos(self) -> List[Editorial]:
        """Devuelve la lista de editoriales del repositorio."""
        return self.repositorio.leer_todos()

    def eliminar(self, id: int) -> bool:
        """Elimina la editorial y devuelve False si el ID no existe."""
        return self.repositorio.eliminar(id)
