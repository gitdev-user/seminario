from datetime import date

from pydantic import Field, field_validator
from entities.entidad_base import EntidadBase


class Libro(EntidadBase):
    """Representa un libro con sus datos bibliográficos y físicos."""

    isbn: str = Field(
        ...,
        min_length=10,
        max_length=13,
        description="ISBN del libro"
    )

    titulo: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Título del libro"
    )

    autor: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Autor del libro"
    )

    peso: float = Field(
        ...,
        gt=0,
        allow_inf_nan=False,
        description="Peso del libro en gramos"
    )

    dimensiones: str = Field(
        ...,
        min_length=5,
        max_length=20,
        description="Dimensiones del libro en centímetros (alto x ancho x grosor)"
    )

    numero_paginas: int = Field(
        ...,
        gt=0,
        description="Número de páginas del libro"
    )

    fecha_publicacion: date = Field(
        ...,
        description="Fecha de publicación del libro"
    )

    idioma: str = Field(
        ...,
        min_length=2,
        max_length=30,
        description="Idioma del libro"
    )

    editorial_id: int = Field(
        ...,
        gt=0,
        description="Identificador de la editorial"
    )

    genero_id: int = Field(
        ...,
        gt=0,
        description="Identificador del género literario"
    )

    @field_validator('fecha_publicacion')
    @classmethod
    def verificar_fecha_publicacion(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("La fecha de publicación no puede ser una fecha futura.")
        return v
