"""Valida los libros extraídos antes de exportarlos a JSON."""

from decimal import Decimal
from scrapy.exceptions import DropItem


class CuspideValidacionPipeline:
    """Descarta libros con datos obligatorios ausentes o inválidos."""

    def process_item(self, item):
        """Valida un ítem antes de continuar su procesamiento."""
        if not item.get("titulo_encontrado"):
            raise DropItem("El libro no tiene título.")

        precio = item.get("precio")

        if not isinstance(precio, Decimal):
            raise DropItem("El precio debe ser Decimal.")

        if not precio.is_finite() or precio <= 0:
            raise DropItem("El precio debe ser finito y mayor que cero.")

        url = item.get("url")

        if not url:
            raise DropItem("El libro no tiene URL.")

        if not item.get("descripcion"):
            item["descripcion"] = ""

        return item