from datetime import datetime

from pydantic import Field, field_validator
from pydantic import BaseModel


class Stock(BaseModel):
    """Representa las existencias de un libro y su última actualización."""

    libro_id: int = Field(
        ...,
        gt=0,
        description="Identificador del libro"
    )

    cantidad_minima: int = Field(
        ...,
        description="Cantidad mínima de ejemplares deseada en stock"
    )

    cantidad_total: int = Field(
        ...,
        description="Cantidad total de ejemplares en stock"
    )

    @field_validator('cantidad_minima', 'cantidad_total')
    @classmethod
    def validar_no_negativo(cls, v: int) -> int:
        if v < 0:
            raise ValueError("La cantidad minima o total no puede ser menor a 0.")
        return v
