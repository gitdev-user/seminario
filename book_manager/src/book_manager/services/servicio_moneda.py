from typing import List, Optional

from entities.moneda import Moneda
from repositories.impl.csv_archivo_repositorio_moneda_impl import (
    CSVArchivoRepositorioMoneda,
)


class ServicoMoneda:
    """Gestiona las operaciones CRUD de monedas."""

    def __init__(self, repositorio: CSVArchivoRepositorioMoneda):
        self.repositorio = repositorio

    def guardar(self, moneda: Moneda) -> Moneda:
        """Crea la moneda si su ID no existe; en caso contrario, la actualiza."""
        if self.repositorio.leer_por_id(moneda.id) is None:
            return self.repositorio.crear(moneda)
        return self.repositorio.actualizar(moneda)

    def leer_por_id(self, id: int) -> Optional[Moneda]:
        """Devuelve la moneda con el ID indicado, o None si no existe."""
        return self.repositorio.leer_por_id(id)

    def leer_todos(self) -> List[Moneda]:
        """Devuelve la lista de monedas del repositorio."""
        return self.repositorio.leer_todos()

    def eliminar(self, id: int) -> bool:
        """Elimina la moneda y devuelve False si el ID no existe."""
        return self.repositorio.eliminar(id)
