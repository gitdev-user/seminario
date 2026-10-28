"""Coordina la ejecución del scraper y la generación de sus resultados."""

from pathlib import Path

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from entities.entities import Libro
from scraper.spiders.cuspide_spider import CuspideSpider


class ServicioScraping:
    """Ejecuta el scraper usando la configuración de scraper/settings.py.

    El crawler se inicia una sola vez por proceso de Python, ya que el
    reactor de Scrapy no se puede reiniciar.
    """

    def __init__(self, libros: list[Libro]):
        """Recibe las entidades Libro que se buscarán en Cúspide."""
        self.libros = libros

    def ejecutar(self) -> None:
        """Ejecuta el spider y escribe el archivo configurado en reportes."""
        configuracion = Settings()
        configuracion.setmodule("scraper.settings", priority="project")

        archivo = Path(configuracion["ARCHIVO_SCRAPING"])
        archivo.parent.mkdir(parents=True, exist_ok=True)

        proceso = CrawlerProcess(configuracion)
        proceso.crawl(CuspideSpider, libros=self.libros)
        proceso.start()
