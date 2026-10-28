import re
import unicodedata
from urllib.parse import urlencode

import scrapy

from scrapy.http import Response

from entities.entities import Libro

from ..loaders import CuspideLibroLoader


class CuspideSpider(scrapy.Spider):
    """Busca títulos normalizados iguales y entrega la ficha al pipeline."""

    name = "cuspide"
    allowed_domains = ["cuspide.com", "www.cuspide.com"]
    max = 10

    def __init__(self, libros: list[Libro] | None = None, **kwargs):
        """Recibe una lista de entidades Libro para realizar las búsquedas."""
        super().__init__(**kwargs)
        self.libros = libros if libros is not None else []

    async def start(self):
        """Busca cada libro por su título."""

        for libro in self.libros:
            parametros = urlencode({
                "s": libro.titulo,
                "post_type": "product",
            })

            yield scrapy.Request(
                url=f"https://cuspide.com/?{parametros}",
                callback=self.parse_busqueda,
                cb_kwargs={"libro": libro},
                dont_filter=True,
            )


    def parse_busqueda(self, response: Response, libro: Libro):
        """Procesa la primera coincidencia exacta entre títulos normalizados."""
        candidatos = {}
        enlaces = response.css(
            "div.product p.woocommerce-loop-product__title a"
        )

        for enlace in enlaces:
            titulo = " ".join(
                " ".join(enlace.xpath(".//text()").getall()).split()
            )
            href = enlace.attrib.get("href")

            if titulo and href:
                candidatos.setdefault(response.urljoin(href), titulo)

            if len(candidatos) == self.max:
                break

        buscado = self._normalizar(libro.titulo)

        for url, titulo in candidatos.items():
            if self._normalizar(titulo) == buscado:
                print(f"\nBuscado: {libro.titulo}")
                print(f"Seleccionado: {titulo}")
                print("Coincidencia exacta entre títulos normalizados.")

                yield response.follow(
                    url,
                    callback=self.parse_libro,
                    cb_kwargs={"libro": libro},
                    dont_filter=True,
                )
                return

    def parse_libro(self, response, libro):
        """Carga los datos de una ficha mediante CuspideLibroLoader."""

        loader = CuspideLibroLoader(response=response)
        loader.add_value("titulo_buscado", libro.titulo)
        loader.add_css("titulo_encontrado", "h1::text")
        loader.add_css("isbn", "span.sku::text")
        loader.add_css("precio", "p.price bdi::text")
        loader.add_css("url_imagen", "div.woocommerce-product-gallery "
                         "img::attr(data-large_image)")
        loader.add_css("formas_pago", "#contentPaymentsPopUpArg li::text")
        loader.add_css("descripcion", "p.livriz-text-synopsis ::text")
        loader.add_value("url", response.url)
   
        yield loader.load_item()

    @staticmethod
    def _normalizar(texto):
        """Ignora mayúsculas, tildes, puntuación y espacios repetidos."""
        texto = unicodedata.normalize("NFKD", texto.casefold())
        texto = "".join(c for c in texto if not unicodedata.combining(c))
        return " ".join(re.sub(r"[^\w\s]", " ", texto).split())

