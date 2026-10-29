"""Compara precios internos y web y genera alertas en CSV."""

import csv
import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from entities.entities import Libro
from scraper.settings import ARCHIVO_SCRAPING
from services.service_scraping import ServicioScraping


class ServicioAlerta:
    """Genera alertas cuando la diferencia supera el umbral porcentual."""

    def __init__(self, libros: list[Libro]):
        """Recibe los libros internos con sus precios por moneda."""
        self.libros = libros
        self._cantidad_alertas = 0

    def obtener_cantidad_alertas(self) -> int:
        """Devuelve la cantidad de alertas de la última ejecución."""
        return self._cantidad_alertas

    def ejecutar(self, umbral: Decimal) -> None:
        """Ejecuta el scraping y escribe las alertas de precios.

        El umbral debe estar entre 0 y 1; 0.10 representa un 10 %.
        La diferencia monetaria es el precio web menos el precio interno.
        Solo se comparan los ISBN presentes en el JSON y con precio interno
        válido en ARS. El CSV se crea aun cuando no existan alertas.
        """
        self._cantidad_alertas = 0

        if not umbral.is_finite() or not Decimal("0") <= umbral <= Decimal("1"):
            raise ValueError("El umbral debe estar entre 0 y 1.")

        ServicioScraping(self.libros).ejecutar()

        archivo_json = Path(ARCHIVO_SCRAPING)
        with archivo_json.open(encoding="utf-8") as archivo:
            resultados = json.load(archivo, parse_float=Decimal)

        libros_por_isbn = {libro.isbn: libro for libro in self.libros}

        fecha = datetime.now().astimezone().date()
        archivo_alertas = archivo_json.parent / (
            f"alertas_precios_{fecha:%Y%m%d}.csv"
        )

        with archivo_alertas.open(
            "w", encoding="utf-8-sig", newline=""
        ) as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([
                "isbn",
                "titulo",
                "precio_interno",
                "precio_web",
                "diferencia",
                "umbral",
                "fecha_extraccion",
            ])

            for resultado in resultados:
                isbn = resultado.get("isbn")
                libro = libros_por_isbn.get(isbn)

                if libro is None:
                    continue

                precio = next(
                    (
                        precio
                        for precio in libro.precios
                        if precio.moneda.codigo_iso == "ARS"
                    ),
                    None,
                )

                if precio is None or precio.precio_base <= 0:
                    continue

                try:
                    precio_web = Decimal(str(resultado.get("precio")))
                except InvalidOperation:
                    continue

                if not precio_web.is_finite() or precio_web <= 0:
                    continue

                precio_interno = precio.precio_base
                diferencia = precio_web - precio_interno

                if abs(diferencia) > precio_interno * umbral:
                    escritor.writerow([
                        isbn,
                        libro.titulo,
                        f"{precio_interno:.2f}",
                        f"{precio_web:.2f}",
                        f"{diferencia:.2f}",
                        f"{umbral * 100:.2f}%",
                        fecha.isoformat(),
                    ])
                    self._cantidad_alertas += 1
