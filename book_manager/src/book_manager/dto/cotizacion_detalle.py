from pydantic import BaseModel

from entities.cotizacion import Cotizacion
from entities.moneda import Moneda
from entities.tipo_cotizacion import TipoCotizacion


class CotizacionDetalle(BaseModel):
    """Reúne una cotización con sus monedas y su tipo de cotización."""

    cotizacion: Cotizacion
    moneda_origen: Moneda
    moneda_destino: Moneda
    tipo_cotizacion: TipoCotizacion
