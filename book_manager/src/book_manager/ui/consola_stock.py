from entities.stock import Stock
from ui.consola_registro_inventario import ConsolaRegistroInventario


class ConsolaStock(ConsolaRegistroInventario):
    TITULO = "Stock"
    NOMBRE = "Stock"
    MODELO = Stock
    METODO_LEER = "leer_stock_por_libro"
    METODO_GUARDAR = "guardar_stock"
    CAMPOS = (("cantidad_minima", "Cantidad mínima"), ("cantidad_total", "Cantidad total"))