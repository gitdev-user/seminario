from ui.consola import ConsolaMenu
from ui.consola_precios import ConsolaPrecios
from ui.consola_stock import ConsolaStock


class ConsolaInventario(ConsolaMenu):
    def __init__(self, precios=None, stock=None):
        precios = precios if precios is not None else ConsolaPrecios()
        stock = stock if stock is not None else ConsolaStock()
        super().__init__("Inventario", {
            "1": ("Precios", precios.ejecutar),
            "2": ("Stock", stock.ejecutar),
        })

