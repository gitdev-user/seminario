"""Coordina la ejecución del scraper y la generación de sus resultados."""

from multiprocessing import get_context
from pathlib import Path

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from entities.entities import Libro
from scraper.spiders.cuspide_spider import CuspideSpider


def _ejecutar_scraper(libros: list[Libro]) -> None:
    """Inicia el reactor y escribe el JSON dentro del proceso hijo."""
    configuracion = Settings()
    configuracion.setmodule("scraper.settings", priority="project")

    archivo = Path(configuracion["ARCHIVO_SCRAPING"])
    archivo.parent.mkdir(parents=True, exist_ok=True)

    proceso = CrawlerProcess(configuracion)
    crawler = proceso.create_crawler(CuspideSpider)
    errores = []
    proceso.crawl(crawler, libros=libros).addErrback(errores.append)
    proceso.start()

    if errores:
        raise RuntimeError(errores[0].getErrorMessage())

    estadisticas = crawler.stats.get_stats()
    if any(
        valor for nombre, valor in estadisticas.items()
        if nombre.startswith("feedexport/failed_count/")
    ):
        raise RuntimeError("No se pudo escribir el archivo del scraping.")


class ServicioScraping:
    """Ejecuta cada scraping en un proceso independiente.

    Permite repetir la operación desde el menú sin reiniciar el reactor
    de Scrapy en el mismo proceso. Lee las opciones de scraper/settings.py.
    """

    def __init__(self, libros: list[Libro]):
        """Recibe las entidades Libro que se buscarán en Cúspide."""
        self.libros = libros

    def ejecutar(self) -> None:
        """Espera al scraper antes de continuar con la comparación de precios."""
        proceso = get_context("spawn").Process(
            target=_ejecutar_scraper,
            args=(self.libros,),
        )
        proceso.start()
        proceso.join()

        if proceso.exitcode != 0:
            raise RuntimeError("El proceso de scraping no terminó correctamente.")
