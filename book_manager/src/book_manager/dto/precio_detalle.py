from pydantic import BaseModel

from entities.moneda import Moneda
from entities.precio import Precio


class PrecioDetalle(BaseModel):
    """Reúne un precio y su moneda, conservando sus identificadores."""

    precio: Precio
    moneda: Moneda
