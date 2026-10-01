"""Demostración de altas mediante servicios, con resultados por pantalla."""

from datetime import date
from decimal import Decimal

from entities.editorial import Editorial
from entities.genero import Genero
from entities.moneda import Moneda
from entities.tipo_cotizacion import TipoCotizacion
from entities.libro import Libro
from entities.precio import Precio
from entities.stock import Stock
from entities.cotizacion import Cotizacion
from services.servicio_editorial import ServicioEditorial
from services.servicio_genero import ServicioGenero
from services.servicio_moneda import ServicoMoneda
from services.servicio_tipo_cotizacion import ServicioTipoCotizacion
from services.servicio_catalogo import ServicioCatalogo
from services.servicio_inventario import ServicioInventario
from services.servicio_cotizacion import ServicioCotizacion


class ProcesoAutomatico:
    """Cada ejecución guarda datos de ejemplo en los repositorios configurados.

    Recibe los servicios para poder utilizar archivos reales o temporales.
    No borra datos ni ejecuta la precarga. Las altas generan nuevos IDs.
    """

    def __init__(
        self,
        servicio_editorial: ServicioEditorial,
        servicio_genero: ServicioGenero,
        servicio_moneda: ServicoMoneda,
        servicio_tipo: ServicioTipoCotizacion,
        servicio_catalogo: ServicioCatalogo,
        servicio_inventario: ServicioInventario,
        servicio_cotizacion: ServicioCotizacion,
    ):
        self.editoriales = servicio_editorial
        self.generos = servicio_genero
        self.monedas = servicio_moneda
        self.tipos = servicio_tipo
        self.catalogo = servicio_catalogo
        self.inventario = servicio_inventario
        self.cotizaciones = servicio_cotizacion

    @staticmethod
    def _mostrar_listado(registros) -> None:
        registros = list(registros)
        if not registros:
            print("Sin registros.")
            return
        columnas = list(type(registros[0]).model_fields)
        filas = [
            [str(registro.model_dump(mode="json")[campo]) for campo in columnas]
            for registro in registros
        ]
        anchos = [
            max(len(campo), *(len(fila[i]) for fila in filas))
            for i, campo in enumerate(columnas)
        ]
        print(" | ".join(c.ljust(a) for c, a in zip(columnas, anchos)))
        print("-+-".join("-" * a for a in anchos))
        for fila in filas:
            print(" | ".join(v.ljust(a) for v, a in zip(fila, anchos)))

    def _guardar_y_mostrar(self, titulo, entidad, listar, guardar):
        print(f"\n{'=' * 60}\n{titulo}\n{'=' * 60}")
        print("ANTES:")
        self._mostrar_listado(listar())
        print("\nREGISTRO A GUARDAR:")
        for campo, valor in entidad.model_dump(mode="json").items():
            etiqueta = campo.replace("_", " ").capitalize()
            print(f"{etiqueta}: {valor}")
        guardada = guardar(entidad)
        print("\nGuardado exitosamente.")
        if hasattr(guardada, "id"):
            print(f"ID asignado: {guardada.id}")
        print("\nDESPUÉS:")
        self._mostrar_listado(listar())
        return guardada

    def _listar_inventario(self, leer_por_libro):
        registros = []
        for libro in self.catalogo.listar_todos():
            registro = leer_por_libro(libro.id)
            if registro is not None:
                registros.append(registro)
        return registros

    def ejecutar(self) -> None:
        """Muestra antes y después de cada alta, respetando las relaciones."""
        editorial = self._guardar_y_mostrar(
            "EDITORIALES", Editorial(
                nombre="Editorial Demo", grupo="Grupo Demo",
                pais_origen="Argentina", telefono="+01140001234",
                email="demo@example.com",
            ), self.editoriales.leer_todos, self.editoriales.guardar,
        )
        genero = self._guardar_y_mostrar(
            "GÉNEROS", Genero(nombre="Narrativa Demo", descripcion="Género de ejemplo"),
            self.generos.leer_todos, self.generos.guardar,
        )
        # Dos monedas permiten demostrar la cotización incluso con archivos vacíos.
        origen = self._guardar_y_mostrar(
            "MONEDAS — ORIGEN", Moneda(codigo_iso="XAA", nombre="Moneda demo A", simbolo="A$"),
            self.monedas.leer_todos, self.monedas.guardar,
        )
        destino = self._guardar_y_mostrar(
            "MONEDAS — DESTINO", Moneda(codigo_iso="XBB", nombre="Moneda demo B", simbolo="B$"),
            self.monedas.leer_todos, self.monedas.guardar,
        )
        tipo = self._guardar_y_mostrar(
            "TIPOS DE COTIZACIÓN", TipoCotizacion(nombre="Demo", descripcion="Tipo de ejemplo"),
            self.tipos.leer_todos, self.tipos.guardar,
        )
        libro = self._guardar_y_mostrar(
            "LIBROS", Libro(
                isbn="9780000000002", titulo="Libro de ejemplo", autor="Autor Demo",
                peso=250, dimensiones="20 x 15", numero_paginas=120,
                fecha_publicacion=date(2024, 1, 1), idioma="Español",
                editorial_id=editorial.id, genero_id=genero.id,
            ), self.catalogo.listar_todos, self.catalogo.guardar,
        )
        self._guardar_y_mostrar(
            "PRECIOS", Precio(libro_id=libro.id, moneda_base_id=origen.id, precio_base=Decimal("25.50")),
            lambda: self._listar_inventario(self.inventario.leer_precio_por_libro),
            self.inventario.guardar_precio,
        )
        self._guardar_y_mostrar(
            "STOCK", Stock(libro_id=libro.id, cantidad_minima=2, cantidad_total=10),
            lambda: self._listar_inventario(self.inventario.leer_stock_por_libro),
            self.inventario.guardar_stock,
        )
        self._guardar_y_mostrar(
            f"COTIZACIONES — HISTÓRICO: tipo {tipo.id}, monedas {origen.id} → {destino.id}",
            Cotizacion(
                tipo_cotizacion_id=tipo.id, moneda_origen_id=origen.id,
                moneda_destino_id=destino.id, fecha=date.today(), valor=Decimal("10.00"),
            ),
            lambda: self.cotizaciones.leer_historico_por_tipo_moneda_origen_moneda_destino(
                tipo.id, origen.id, destino.id,
            ),
            self.cotizaciones.guardar,
        )
        print("\nProceso automático finalizado.")
