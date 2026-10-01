import re

from pydantic import Field, field_validator, EmailStr
from entities.entidad_base import EntidadBase

class Editorial(EntidadBase):
    nombre: str = Field(
        ..., 
        min_length=1, 
        max_length=50, 
        description="Nombre de la editorial"
    )

    grupo: str = Field(
        ..., 
        min_length=1, 
        max_length=50, 
        description="Nombre del grupo"
    )

    pais_origen: str = Field(
        ..., 
        min_length=2, 
        max_length=20, 
        description="Pais de origen"
    )

    telefono: str = Field(
        ..., 
        min_length=7, 
        max_length=20, 
        description="Teléfono"
    )

    email: EmailStr = Field(
        ..., 
        description="Correo electronico"
    )

    @field_validator('telefono')
    @classmethod
    def validar_formato_telefono(cls, v: str) -> str:
        patron = r'^\+?[0-9\s\-]{7,20}$'
        if not re.match(patron, v):
            raise ValueError('El teléfono debe contener un formato válido (ej: +123456789 o 444-5555).')
        return v
