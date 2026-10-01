"""Datos ficticios de precarga; los importes no son cotizaciones reales."""

from config.config import config
from entities.editorial import Editorial
from entities.genero import Genero
from entities.moneda import Moneda
from entities.tipo_cotizacion import TipoCotizacion
from entities.libro import Libro
from entities.precio import Precio
from entities.stock import Stock
from entities.cotizacion import Cotizacion

EDITORIALES = [
    {
        "id": 1,
        "nombre": "Editorial Horizonte",
        "grupo": "Grupo Horizonte",
        "pais_origen": "Argentina",
        "telefono": "+541140001000",
        "email": "contacto1@example.com"
    },
    {
        "id": 2,
        "nombre": "Editorial Sendero",
        "grupo": "Grupo Sendero",
        "pais_origen": "Argentina",
        "telefono": "+541140001001",
        "email": "contacto2@example.com"
    },
    {
        "id": 3,
        "nombre": "Editorial Aurora",
        "grupo": "Grupo Aurora",
        "pais_origen": "Argentina",
        "telefono": "+541140001002",
        "email": "contacto3@example.com"
    },
    {
        "id": 4,
        "nombre": "Editorial Faro",
        "grupo": "Grupo Faro",
        "pais_origen": "Argentina",
        "telefono": "+541140001003",
        "email": "contacto4@example.com"
    },
    {
        "id": 5,
        "nombre": "Editorial Raices",
        "grupo": "Grupo Raices",
        "pais_origen": "Argentina",
        "telefono": "+541140001004",
        "email": "contacto5@example.com"
    },
    {
        "id": 6,
        "nombre": "Editorial Brisa",
        "grupo": "Grupo Brisa",
        "pais_origen": "Argentina",
        "telefono": "+541140001005",
        "email": "contacto6@example.com"
    },
    {
        "id": 7,
        "nombre": "Editorial Puente",
        "grupo": "Grupo Puente",
        "pais_origen": "Argentina",
        "telefono": "+541140001006",
        "email": "contacto7@example.com"
    },
    {
        "id": 8,
        "nombre": "Editorial Estrella",
        "grupo": "Grupo Estrella",
        "pais_origen": "Argentina",
        "telefono": "+541140001007",
        "email": "contacto8@example.com"
    },
    {
        "id": 9,
        "nombre": "Editorial Norte",
        "grupo": "Grupo Norte",
        "pais_origen": "Argentina",
        "telefono": "+541140001008",
        "email": "contacto9@example.com"
    },
    {
        "id": 10,
        "nombre": "Editorial Sur",
        "grupo": "Grupo Sur",
        "pais_origen": "Argentina",
        "telefono": "+541140001009",
        "email": "contacto10@example.com"
    }
]

GENEROS = [
    {
        "id": 1,
        "nombre": "Novela",
        "descripcion": "Libros de novela"
    },
    {
        "id": 2,
        "nombre": "Ensayo",
        "descripcion": "Libros de ensayo"
    },
    {
        "id": 3,
        "nombre": "Infantil",
        "descripcion": "Libros de infantil"
    },
    {
        "id": 4,
        "nombre": "Tecnico",
        "descripcion": "Libros de tecnico"
    },
    {
        "id": 5,
        "nombre": "Poesia",
        "descripcion": "Libros de poesia"
    },
    {
        "id": 6,
        "nombre": "Historia",
        "descripcion": "Libros de historia"
    },
    {
        "id": 7,
        "nombre": "Ciencia",
        "descripcion": "Libros de ciencia"
    },
    {
        "id": 8,
        "nombre": "Fantasia",
        "descripcion": "Libros de fantasia"
    },
    {
        "id": 9,
        "nombre": "Biografia",
        "descripcion": "Libros de biografia"
    },
    {
        "id": 10,
        "nombre": "Teatro",
        "descripcion": "Libros de teatro"
    }
]

MONEDAS = [
    {
        "id": 1,
        "codigo_iso": "USD",
        "nombre": "Dolar estadounidense",
        "simbolo": "US$"
    },
    {
        "id": 2,
        "codigo_iso": "ARS",
        "nombre": "Peso argentino",
        "simbolo": "$"
    },
    {
        "id": 3,
        "codigo_iso": "EUR",
        "nombre": "Euro",
        "simbolo": "€"
    },
    {
        "id": 4,
        "codigo_iso": "BRL",
        "nombre": "Real brasileno",
        "simbolo": "R$"
    },
    {
        "id": 5,
        "codigo_iso": "CLP",
        "nombre": "Peso chileno",
        "simbolo": "CL$"
    },
    {
        "id": 6,
        "codigo_iso": "UYU",
        "nombre": "Peso uruguayo",
        "simbolo": "UY$"
    },
    {
        "id": 7,
        "codigo_iso": "GBP",
        "nombre": "Libra esterlina",
        "simbolo": "£"
    },
    {
        "id": 8,
        "codigo_iso": "JPY",
        "nombre": "Yen japones",
        "simbolo": "¥"
    },
    {
        "id": 9,
        "codigo_iso": "CAD",
        "nombre": "Dolar canadiense",
        "simbolo": "CA$"
    },
    {
        "id": 10,
        "codigo_iso": "CHF",
        "nombre": "Franco suizo",
        "simbolo": "CHF"
    }
]

TIPOS_COTIZACION = [
    {
        "id": 1,
        "nombre": "Oficial",
        "descripcion": "Tipo Oficial"
    },
    {
        "id": 2,
        "nombre": "Blue",
        "descripcion": "Tipo Blue"
    },
    {
        "id": 3,
        "nombre": "MEP",
        "descripcion": "Tipo MEP"
    },
    {
        "id": 4,
        "nombre": "CCL",
        "descripcion": "Tipo CCL"
    },
    {
        "id": 5,
        "nombre": "Mayorista",
        "descripcion": "Tipo Mayorista"
    },
    {
        "id": 6,
        "nombre": "Minorista",
        "descripcion": "Tipo Minorista"
    },
    {
        "id": 7,
        "nombre": "Tarjeta",
        "descripcion": "Tipo Tarjeta"
    },
    {
        "id": 8,
        "nombre": "Turista",
        "descripcion": "Tipo Turista"
    },
    {
        "id": 9,
        "nombre": "Compra",
        "descripcion": "Tipo Compra"
    },
    {
        "id": 10,
        "nombre": "Venta",
        "descripcion": "Tipo Venta"
    }
]

LIBROS = [
    {
        "id": 1,
        "isbn": "9780000000001",
        "titulo": "El horizonte",
        "autor": "Autor Horizonte",
        "peso": 250,
        "dimensiones": "20 x 14 x 2",
        "numero_paginas": 120,
        "fecha_publicacion": "2024-01-15",
        "idioma": "Espanol",
        "editorial_id": 1,
        "genero_id": 1
    },
    {
        "id": 2,
        "isbn": "9780000000002",
        "titulo": "Senderos de papel",
        "autor": "Autor Sendero",
        "peso": 270,
        "dimensiones": "20 x 14 x 2",
        "numero_paginas": 140,
        "fecha_publicacion": "2024-02-15",
        "idioma": "Espanol",
        "editorial_id": 2,
        "genero_id": 2
    },
    {
        "id": 3,
        "isbn": "9780000000003",
        "titulo": "La luna azul",
        "autor": "Autor Aurora",
        "peso": 290,
        "dimensiones": "20 x 14 x 2",
        "numero_paginas": 160,
        "fecha_publicacion": "2024-03-15",
        "idioma": "Espanol",
        "editorial_id": 3,
        "genero_id": 3
    },
    {
        "id": 4,
        "isbn": "9780000000004",
        "titulo": "Python inicial",
        "autor": "Autor Faro",
        "peso": 310,
        "dimensiones": "20 x 14 x 2",
        "numero_paginas": 180,
        "fecha_publicacion": "2024-04-15",
        "idioma": "Espanol",
        "editorial_id": 4,
        "genero_id": 4
    },
    {
        "id": 5,
        "isbn": "9780000000005",
        "titulo": "Versos del mar",
        "autor": "Autor Raices",
        "peso": 330,
        "dimensiones": "20 x 14 x 2",
        "numero_paginas": 200,
        "fecha_publicacion": "2024-05-15",
        "idioma": "Espanol",
        "editorial_id": 5,
        "genero_id": 5
    },
    {
        "id": 6,
        "isbn": "9780000000006",
        "titulo": "Memorias del sur",
        "autor": "Autor Brisa",
        "peso": 350,
        "dimensiones": "20 x 14 x 2",
        "numero_paginas": 220,
        "fecha_publicacion": "2024-06-15",
        "idioma": "Espanol",
        "editorial_id": 6,
        "genero_id": 6
    },
    {
        "id": 7,
        "isbn": "9780000000007",
        "titulo": "Ciencia cotidiana",
        "autor": "Autor Puente",
        "peso": 370,
        "dimensiones": "20 x 14 x 2",
        "numero_paginas": 240,
        "fecha_publicacion": "2024-07-15",
        "idioma": "Espanol",
        "editorial_id": 7,
        "genero_id": 7
    },
    {
        "id": 8,
        "isbn": "9780000000008",
        "titulo": "El bosque magico",
        "autor": "Autor Estrella",
        "peso": 390,
        "dimensiones": "20 x 14 x 2",
        "numero_paginas": 260,
        "fecha_publicacion": "2024-08-15",
        "idioma": "Espanol",
        "editorial_id": 8,
        "genero_id": 8
    },
    {
        "id": 9,
        "isbn": "9780000000009",
        "titulo": "Una vida de viajes",
        "autor": "Autor Norte",
        "peso": 410,
        "dimensiones": "20 x 14 x 2",
        "numero_paginas": 280,
        "fecha_publicacion": "2024-09-15",
        "idioma": "Espanol",
        "editorial_id": 9,
        "genero_id": 9
    },
    {
        "id": 10,
        "isbn": "9780000000010",
        "titulo": "El ultimo acto",
        "autor": "Autor Sur",
        "peso": 430,
        "dimensiones": "20 x 14 x 2",
        "numero_paginas": 300,
        "fecha_publicacion": "2024-10-15",
        "idioma": "Espanol",
        "editorial_id": 10,
        "genero_id": 10
    }
]

PRECIOS = [
    {
        "libro_id": 1,
        "moneda_base_id": 1,
        "precio_base": "12.50"
    },
    {
        "libro_id": 2,
        "moneda_base_id": 1,
        "precio_base": "13.50"
    },
    {
        "libro_id": 3,
        "moneda_base_id": 1,
        "precio_base": "14.50"
    },
    {
        "libro_id": 4,
        "moneda_base_id": 1,
        "precio_base": "15.50"
    },
    {
        "libro_id": 5,
        "moneda_base_id": 1,
        "precio_base": "16.50"
    },
    {
        "libro_id": 6,
        "moneda_base_id": 1,
        "precio_base": "17.50"
    },
    {
        "libro_id": 7,
        "moneda_base_id": 1,
        "precio_base": "18.50"
    },
    {
        "libro_id": 8,
        "moneda_base_id": 1,
        "precio_base": "19.50"
    },
    {
        "libro_id": 9,
        "moneda_base_id": 1,
        "precio_base": "20.50"
    },
    {
        "libro_id": 10,
        "moneda_base_id": 1,
        "precio_base": "21.50"
    }
]

STOCK = [
    {
        "libro_id": 1,
        "cantidad_minima": 2,
        "cantidad_total": 0
    },
    {
        "libro_id": 2,
        "cantidad_minima": 2,
        "cantidad_total": 3
    },
    {
        "libro_id": 3,
        "cantidad_minima": 2,
        "cantidad_total": 6
    },
    {
        "libro_id": 4,
        "cantidad_minima": 2,
        "cantidad_total": 9
    },
    {
        "libro_id": 5,
        "cantidad_minima": 2,
        "cantidad_total": 12
    },
    {
        "libro_id": 6,
        "cantidad_minima": 2,
        "cantidad_total": 15
    },
    {
        "libro_id": 7,
        "cantidad_minima": 2,
        "cantidad_total": 18
    },
    {
        "libro_id": 8,
        "cantidad_minima": 2,
        "cantidad_total": 21
    },
    {
        "libro_id": 9,
        "cantidad_minima": 2,
        "cantidad_total": 24
    },
    {
        "libro_id": 10,
        "cantidad_minima": 2,
        "cantidad_total": 27
    }
]

COTIZACIONES = [
    {
        "moneda_origen_id": 1,
        "moneda_destino_id": 2,
        "tipo_cotizacion_id": 1,
        "valor": "1000.00",
        "fecha": "2026-09-01"
    },
    {
        "moneda_origen_id": 1,
        "moneda_destino_id": 2,
        "tipo_cotizacion_id": 2,
        "valor": "1010.00",
        "fecha": "2026-09-01"
    },
    {
        "moneda_origen_id": 1,
        "moneda_destino_id": 2,
        "tipo_cotizacion_id": 3,
        "valor": "1020.00",
        "fecha": "2026-09-01"
    },
    {
        "moneda_origen_id": 1,
        "moneda_destino_id": 2,
        "tipo_cotizacion_id": 4,
        "valor": "1030.00",
        "fecha": "2026-09-01"
    },
    {
        "moneda_origen_id": 1,
        "moneda_destino_id": 2,
        "tipo_cotizacion_id": 5,
        "valor": "1040.00",
        "fecha": "2026-09-01"
    },
    {
        "moneda_origen_id": 1,
        "moneda_destino_id": 2,
        "tipo_cotizacion_id": 6,
        "valor": "1050.00",
        "fecha": "2026-09-01"
    },
    {
        "moneda_origen_id": 1,
        "moneda_destino_id": 2,
        "tipo_cotizacion_id": 7,
        "valor": "1060.00",
        "fecha": "2026-09-01"
    },
    {
        "moneda_origen_id": 1,
        "moneda_destino_id": 2,
        "tipo_cotizacion_id": 8,
        "valor": "1070.00",
        "fecha": "2026-09-01"
    },
    {
        "moneda_origen_id": 1,
        "moneda_destino_id": 2,
        "tipo_cotizacion_id": 9,
        "valor": "1080.00",
        "fecha": "2026-09-01"
    },
    {
        "moneda_origen_id": 1,
        "moneda_destino_id": 3,
        "tipo_cotizacion_id": 1,
        "valor": "1090.00",
        "fecha": "2026-09-01"
    }
]

DATOS_PRECARGA = {
    config.repositorio_editoriales: (Editorial, EDITORIALES),
    config.repositorio_generos: (Genero, GENEROS),
    config.repositorio_monedas: (Moneda, MONEDAS),
    config.repositorio_tipos_cotizacion: (TipoCotizacion, TIPOS_COTIZACION),
    config.repositorio_libros: (Libro, LIBROS),
    config.repositorio_precios: (Precio, PRECIOS),
    config.repositorio_stock: (Stock, STOCK),
    config.repositorio_cotizaciones: (Cotizacion, COTIZACIONES),
}
