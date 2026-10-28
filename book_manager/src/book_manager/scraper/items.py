"""Define los campos de los libros extraídos del sitio de Cúspide."""

import scrapy


class CuspideLibroItem(scrapy.Item):
    """Agrupa los datos de la ficha de un libro encontrado en Cúspide.

    Attributes:
        titulo_buscado: Título utilizado para buscar el libro.
        titulo_encontrado: Título publicado en la ficha del libro.
        isbn: ISBN publicado para identificar el libro.
        precio: Precio publicado para el libro.
        url_imagen: Dirección de la imagen del libro.
        formas_pago: Información sobre los medios de pago disponibles.
        descripcion: Descripción del libro publicada en su ficha.
        url: Dirección de la página del libro.
    """

    titulo_buscado = scrapy.Field()
    titulo_encontrado = scrapy.Field()
    isbn = scrapy.Field()
    precio = scrapy.Field()
    url_imagen = scrapy.Field()
    formas_pago = scrapy.Field()
    descripcion = scrapy.Field()
    url = scrapy.Field()
