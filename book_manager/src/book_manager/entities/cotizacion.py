from datetime import date
from decimal import Decimal

from pydantic import Field
from pydantic import BaseModel, model_validator


class Cotizacion(BaseModel):
    """Representa el valor de conversión entre dos monedas en una fecha."""

    moneda_origen_id: int = Field(
        ...,
        gt=0,
        description="Identificador de la moneda de origen"
    )

    moneda_destino_id: int = Field(
        ...,
        gt=0,
        description="Identificador de la moneda de destino"
    )

    tipo_cotizacion_id: int = Field(
        ...,
        gt=0,
        description="Identificador del tipo de cotización"
    )

    valor: Decimal = Field(
        ...,
        gt=0,
        decimal_places=2,
        max_digits=12,
        allow_inf_nan=False,
        description="Unidades de moneda de destino por cada unidad de moneda de origen"
    )

    fecha: date = Field(
        ...,
        description="Fecha de la cotización"
    )

    @model_validator(mode='after')
    def verificar_monedas_diferentes(self) -> 'Cotizacion':
        if self.moneda_origen_id == self.moneda_destino_id:
            raise ValueError("La moneda de origen y destino no pueden ser iguales.")
        return self

    @model_validator(mode='after')
    def verificar_fecha_coherente(self) -> 'Cotizacion':
        if self.fecha > date.today():
            raise ValueError("La fecha de la cotización no puede ser una fecha futura.")
        return self
