"""Limpia y carga los campos definidos en CuspideLibroItem."""

import re
from decimal import Decimal, InvalidOperation
from typing import Optional

from scrapy.loader import ItemLoader
from itemloaders.processors import Join, MapCompose, TakeFirst

from .items import CuspideLibroItem


def limpiar_texto(valor: str) -> str:
    """Elimina espacios repetidos, tabulaciones y saltos de línea."""
    return " ".join(valor.split())


def limpiar_forma_pago(valor: str) -> str:
    """Elimina el signo > inicial y los espacios sobrantes."""
    return limpiar_texto(valor).lstrip("> ")

def convertir_precio(valor: str) -> Optional[Decimal]:
    """Convierte un precio como "48.500,00" en un Decimal (48500.00).

    En el formato argentino el punto separa miles y la coma, los
    decimales.

    Args:
        valor (str): Texto del precio.

    Returns:
        Optional[Decimal]: El precio, o None si no se pudo interpretar.
    """
    numero = re.sub(r"[^\d,.]", "", valor)
    if not numero:
        return None
    numero = numero.replace(".", "").replace(",", ".")
    try:
        return Decimal(numero)
    except InvalidOperation:
        return None


class CuspideLibroLoader(ItemLoader):
    """Carga textos limpios, el ISBN como texto y el precio como Decimal.

    Une los fragmentos del título encontrado, la descripción y las formas
    de pago. Para los demás campos conserva el primer valor no vacío.
    """

    default_item_class = CuspideLibroItem
    default_output_processor = TakeFirst()

    titulo_buscado_in = MapCompose(limpiar_texto)
    titulo_encontrado_in = MapCompose(limpiar_texto)

    isbn_in = MapCompose (limpiar_texto)
    descripcion_in = MapCompose(limpiar_texto)
    descripcion_out = Join(" ")

    formas_pago_in = MapCompose(limpiar_forma_pago)
    formas_pago_out = Join(" | ")

    precio_in = MapCompose(limpiar_texto, convertir_precio)

