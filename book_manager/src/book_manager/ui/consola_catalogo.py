from entities.libro import Libro
from ui.consola_entidad import ConsolaEntidad
from ui.consola_registro_inventario import ConsolaRegistroInventario


class ConsolaCatalogo(ConsolaEntidad):
    MODELO = Libro
    TITULO = "Catálogo de Libros"
    NOMBRE = "Libro"
    CAMPOS = (
        ("isbn", "ISBN"), ("titulo", "Título"), ("autor", "Autor"),
        ("peso", "Peso en gramos"), ("dimensiones", "Dimensiones"),
        ("numero_paginas", "Número de páginas"),
        ("fecha_publicacion", "Fecha de publicación (AAAA-MM-DD)"),
        ("idioma", "Idioma"), ("editorial_id", "ID de editorial"),
        ("genero_id", "ID de género"),
    )

    def listado(self) -> None:
        libros = self.servicio.listar_todos()
        if not libros:
            print("No hay libros registrados.")
            return
        self._mostrar_listado(libros)

    def buscar(self) -> None:
        detalle = self.servicio.leer_detalle_por_id(self._pedir_id())
        if detalle is None:
            print("No se encontró el libro.")
            return
        self._mostrar_listado([detalle.libro])
        ConsolaRegistroInventario._tabla(
            ["Editorial", "Género", "Precio", "Moneda", "Stock total", "Stock mínimo"],
            [detalle.editorial.nombre, detalle.genero.nombre,
             f"{detalle.precio.precio.precio_base:.2f}" if detalle.precio is not None else "Sin precio",
             detalle.precio.moneda.codigo_iso if detalle.precio is not None else "-",
             detalle.stock.cantidad_total if detalle.stock is not None else "Sin stock registrado",
             detalle.stock.cantidad_minima if detalle.stock is not None else "-"],
        )

    def baja(self) -> None:
        id = self._pedir_id()
        libro = self.servicio.leer_por_id(id)
        if libro is None:
            print("No se encontró el libro.")
            return
        self._mostrar_listado([libro])
        print("Se eliminarán el libro y sus registros de precio y stock, si existen.")
        if input("¿Confirma la baja? [s/N]: ").strip().lower() not in ("s", "si", "sí"):
            print("Baja cancelada.")
            return
        if self.servicio.eliminar(id):
            print("Libro eliminado exitosamente.")
        else:
            print("No se encontró el libro.")