from typing import List, Optional

from entities.tipo_cotizacion import TipoCotizacion
from repositories.impl.csv_archivo_repositorio_tipo_cotizacion_impl import (
    CSVArchivoRepositorioTipoCotizacion,
)


class ServicioTipoCotizacion:
    """Gestiona las operaciones CRUD de tipos de cotización."""

    def __init__(self, repositorio: CSVArchivoRepositorioTipoCotizacion):
        self.repositorio = repositorio

    def guardar(self, tipo_cotizacion: TipoCotizacion) -> TipoCotizacion:
        """Crea el tipo de cotización si su ID no existe; si existe, lo actualiza."""
        if self.repositorio.leer_por_id(tipo_cotizacion.id) is None:
            return self.repositorio.crear(tipo_cotizacion)
        return self.repositorio.actualizar(tipo_cotizacion)

    def leer_por_id(self, id: int) -> Optional[TipoCotizacion]:
        """Devuelve el tipo de cotización con el ID indicado, o None si no existe."""
        return self.repositorio.leer_por_id(id)

    def leer_todos(self) -> List[TipoCotizacion]:
        """Devuelve la lista de tipos de cotización del repositorio."""
        return self.repositorio.leer_todos()

    def eliminar(self, id: int) -> bool:
        """Elimina el tipo de cotización y devuelve False si el ID no existe."""
        return self.repositorio.eliminar(id)
