from pydantic import BaseModel, Field
from typing import Optional
from entities.entidad_base import EntidadBase


class Genero(EntidadBase):
    """Representa un tipo de genéro literario."""

    nombre: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="Nombre del género literario"
    )

    descripcion: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Descripción del género literario"
    )