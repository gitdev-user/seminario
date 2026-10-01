from pydantic import Field, field_validator
from entities.entidad_base import EntidadBase

class Moneda(EntidadBase):
    """Representa una moneda con su identificador, código ISO y símbolo."""

    codigo_iso: str = Field(
        ...,
        min_length=3,
        max_length=3,
        pattern=r"^[A-Z]{3}$",
        description="Código ISO de la moneda"
    )

    nombre: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Nombre de la moneda"
    )

    simbolo: str = Field(
        ...,
        min_length=1,
        max_length=5,
        description="Símbolo de la moneda"
    )

    @field_validator('codigo_iso')
    @classmethod
    def transformar_iso_a_mayusculas(cls, v: str) -> str:
        return v.upper()
