from datetime import datetime
from decimal import Decimal

from pydantic import Field
from pydantic import BaseModel


class Precio(BaseModel):
    """Representa un precio de un libro en una fecha para conservar su histórico."""

    libro_id: int = Field(
        ...,
        gt=0,
        description="Identificador del libro"
    )

    moneda_base_id: int = Field(
        ...,
        gt=0,
        description="Identificador de la moneda base del precio"
    )

    precio_base: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        max_digits=10, 
        allow_inf_nan=False,
        description="Precio del libro expresado en la moneda base"
    )
