from pydantic import Field
from entities.entidad_base import EntidadBase


class TipoCotizacion(EntidadBase):
    """Representa un tipo de cotización con su identificador y descripción."""

    nombre: str = Field(
        ...,
        min_length=1,
        max_length=15,
        description="Nombre del tipo de cotización"
    )

    descripcion: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Descripcion del tipo de cotización"
    )
