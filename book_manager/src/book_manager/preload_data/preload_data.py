import csv
from datetime import date
from decimal import Decimal
from pathlib import Path
from entities.entities import (
    Cotizacion,
    Editorial,
    Genero,
    Libro,
    Moneda,
    Precio,
    Stock,
    TipoCotizacion,
)
from services.services import (
    ServicioTipoCotizacion,
    ServicoMoneda,
    ServicioEditorial,
    ServicioGenero,
    ServicioCotizacion,
    ServicioCatalogo,
    ServicioInventario,
)

class ProcesoPrecarga:
    """Importa los datos iniciales de archivos CSV mediante los servicios.

    Selecciona el importador según el nombre del archivo sin extensión y
    conserva los IDs del CSV en las entidades que tienen identificador.
    Resuelve las relaciones entre entidades antes de guardar los registros.

    Los archivos se procesan en el orden recibido: las monedas y los tipos
    deben cargarse antes que las cotizaciones; las editoriales y los géneros,
    antes que los libros; y los libros y las monedas, antes que precios y stock.
    Si una importación falla, el proceso se interrumpe sin deshacer las cargas
    anteriores.
    """

    def __init__(
        self,
        archivos: list[str],
        servicio_tipo_cotizacion: ServicioTipoCotizacion,
        servicio_moneda: ServicoMoneda,
        servicio_editorial: ServicioEditorial,
        servicio_genero: ServicioGenero,
        servicio_cotizacion: ServicioCotizacion,
        servicio_catalogo: ServicioCatalogo,
        servicio_inventario: ServicioInventario,
    ):
        """Recibe los archivos CSV y los servicios utilizados para importarlos.

        Args:
            archivos: Rutas de los CSV, ordenadas según sus dependencias.
            servicio_tipo_cotizacion: Gestiona los tipos de cotización.
            servicio_moneda: Gestiona las monedas y permite buscarlas por ID.
            servicio_editorial: Gestiona las editoriales de los libros.
            servicio_genero: Gestiona los géneros de los libros.
            servicio_cotizacion: Guarda las cotizaciones entre monedas.
            servicio_catalogo: Gestiona los libros del catálogo.
            servicio_inventario: Guarda los precios y el stock de cada libro.
        """
        self.archivos = archivos
        self.servicio_tipo_cotizacion = servicio_tipo_cotizacion
        self.servicio_moneda = servicio_moneda
        self.servicio_editorial = servicio_editorial
        self.servicio_genero = servicio_genero
        self.servicio_cotizacion = servicio_cotizacion
        self.servicio_catalogo = servicio_catalogo
        self.servicio_inventario = servicio_inventario

        self.importadores = {
            "editoriales": self._importar_editoriales,
            "generos": self._importar_generos,
            "monedas": self._importar_monedas,
            "tipos_cotizacion": self._importar_tipos_cotizacion,
            "cotizaciones": self._importar_cotizaciones,
            "libros": self._importar_libros,
            "precios": self._importar_precios,
            "stock": self._importar_stock,
        }

    def importar_datos(self) -> None:
        """Importa los archivos CSV utilizando el método correspondiente."""

        for archivo in self.archivos:
            ruta = Path(archivo)
            nombre = ruta.stem.lower()

            importador = self.importadores.get(nombre)

            if importador is None:
                raise ValueError(f"No existe importador para: {ruta.name}")

            datos = self._leer_csv(ruta)
            importador(datos)

            print(f"Archivo importado correctamente: {ruta.name}")

    @staticmethod
    def _leer_csv(archivo: Path) -> list[dict]:
        """Lee un archivo CSV y devuelve sus registros."""

        if not archivo.is_file():
            raise FileNotFoundError(f"No existe el archivo: {archivo}")

        with archivo.open(
            mode="r",
            encoding="utf-8-sig",
            newline=""
        ) as csvfile:
            return [
                fila
                for fila in csv.DictReader(csvfile)
                if any(valor and valor.strip() for valor in fila.values())
            ]

    def _importar_editoriales(self, datos: list[dict]) -> None:
        """Construye y guarda las editoriales."""

        for fila in datos:
            editorial = Editorial(
                nombre=fila["nombre"],
                grupo=fila["grupo"],
                pais_origen=fila["pais_origen"],
                telefono=fila["telefono"],
                email=fila["email"],
            )

            editorial.id = int(fila["id"])

            self.servicio_editorial.guardar(editorial)

    def _importar_generos(self, datos: list[dict]) -> None:
        """Construye y guarda los generos con los IDs del CSV."""
        for fila in datos:
            genero = Genero(
                nombre=fila["nombre"],
                descripcion=fila["descripcion"],
            )
            genero.id = int(fila["id"])
            self.servicio_genero.guardar(genero)

    def _importar_monedas(self, datos: list[dict]) -> None:
        """Construye y guarda las monedas con los IDs del CSV."""
        for fila in datos:
            moneda = Moneda(
                codigo_iso=fila["codigo_iso"],
                nombre=fila["nombre"],
                simbolo=fila["simbolo"],
            )
            moneda.id = int(fila["id"])
            self.servicio_moneda.guardar(moneda)

    def _importar_tipos_cotizacion(self, datos: list[dict]) -> None:
        """Construye y guarda los tipos de cotizacion con los IDs del CSV."""
        for fila in datos:
            tipo = TipoCotizacion(
                nombre=fila["nombre"],
                descripcion=fila["descripcion"],
            )
            tipo.id = int(fila["id"])
            self.servicio_tipo_cotizacion.guardar(tipo)

    def _importar_cotizaciones(self, datos: list[dict]) -> None:
        """Relaciona las monedas y el tipo antes de guardar cada cotizacion."""
        for fila in datos:
            origen_id = int(fila["moneda_origen_id"])
            destino_id = int(fila["moneda_destino_id"])
            tipo_id = int(fila["tipo_cotizacion_id"])

            origen = self.servicio_moneda.leer_por_id(origen_id)
            destino = self.servicio_moneda.leer_por_id(destino_id)
            tipo = self.servicio_tipo_cotizacion.leer_por_id(tipo_id)

            if origen is None:
                raise ValueError(f"No existe una moneda de origen con ID {origen_id}.")
            if destino is None:
                raise ValueError(f"No existe una moneda de destino con ID {destino_id}.")
            if tipo is None:
                raise ValueError(f"No existe un tipo de cotizacion con ID {tipo_id}.")

            cotizacion = Cotizacion(
                moneda_origen=origen,
                moneda_destino=destino,
                tipo_cotizacion=tipo,
                valor=Decimal(fila["valor"]),
                fecha=date.fromisoformat(fila["fecha"]),
            )
            self.servicio_cotizacion.guardar(cotizacion)

    def _importar_libros(self, datos: list[dict]) -> None:
        """Relaciona editorial y genero antes de guardar cada libro."""
        for fila in datos:
            editorial_id = int(fila["editorial_id"])
            genero_id = int(fila["genero_id"])

            editorial = self.servicio_editorial.leer_por_id(editorial_id)
            genero = self.servicio_genero.leer_por_id(genero_id)

            if editorial is None:
                raise ValueError(f"No existe una editorial con ID {editorial_id}.")
            if genero is None:
                raise ValueError(f"No existe un genero con ID {genero_id}.")

            libro = Libro(
                isbn=fila["isbn"],
                titulo=fila["titulo"],
                autor=fila["autor"],
                peso=float(fila["peso"]),
                dimensiones=fila["dimensiones"],
                numero_paginas=int(fila["numero_paginas"]),
                fecha_publicacion=date.fromisoformat(fila["fecha_publicacion"]),
                idioma=fila["idioma"],
                editorial=editorial,
                genero=genero,
            )
            libro.id = int(fila["id"])
            self.servicio_catalogo.guardar(libro)

    def _importar_precios(self, datos: list[dict]) -> None:
        """Construye y guarda los precios asociados a cada libro."""
        for fila in datos:
            moneda_id = int(fila["moneda_base_id"])
            moneda = self.servicio_moneda.leer_por_id(moneda_id)

            if moneda is None:
                raise ValueError(f"No existe una moneda con ID {moneda_id}.")

            precio = Precio(
                libro_id=int(fila["libro_id"]),
                moneda=moneda,
                precio_base=Decimal(fila["precio_base"]),
            )
            self.servicio_inventario.guardar_precio(precio)

    def _importar_stock(self, datos: list[dict]) -> None:
        """Construye y guarda las cantidades de stock de cada libro."""
        for fila in datos:
            stock = Stock(
                libro_id=int(fila["libro_id"]),
                cantidad_minima=int(fila["cantidad_minima"]),
                cantidad_total=int(fila["cantidad_total"]),
            )
            self.servicio_inventario.guardar_stock(stock)
