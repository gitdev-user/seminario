from typing import Optional

from pydantic import BaseModel

from dto.precio_detalle import PrecioDetalle
from entities.editorial import Editorial
from entities.genero import Genero
from entities.libro import Libro
from entities.stock import Stock


class LibroDetalle(BaseModel):
    """Reúne un libro con su editorial, género, precio y stock."""

    libro: Libro
    editorial: Editorial
    genero: Genero
    precio: Optional[PrecioDetalle] = None
    stock: Optional[Stock] = None
