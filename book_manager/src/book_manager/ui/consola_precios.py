from entities.precio import Precio
from ui.consola_registro_inventario import ConsolaRegistroInventario


class ConsolaPrecios(ConsolaRegistroInventario):
    TITULO = "Precios"
    NOMBRE = "Precio"
    MODELO = Precio
    METODO_LEER = "leer_precio_por_libro"
    METODO_GUARDAR = "guardar_precio"
    CAMPOS = (("moneda_base_id", "ID de moneda"), ("precio_base", "Precio"))

    def _mostrar(self, registro):
        detalle = self.servicio.leer_precio_detalle_por_libro(registro.libro_id)
        if detalle is None:
            print("No hay precio registrado para ese libro.")
            return
        self._tabla(
            ["ID Libro", "ID Moneda", "Moneda", "Precio"],
            [registro.libro_id, detalle.moneda.id, detalle.moneda.codigo_iso,
             f"{detalle.precio.precio_base:.2f}"],
        )