from ui.consola import ConsolaMenu
from ui.consola_catalogo import ConsolaCatalogo
from ui.consola_inventario import ConsolaInventario
from ui.consola_editoriales import ConsolaEditoriales
from ui.consola_generos import ConsolaGeneros
from ui.consola_monedas import ConsolaMonedas
from ui.consola_cotizaciones import ConsolaCotizaciones


class ConsolaPrincipal(ConsolaMenu):
    def __init__(self, catalogo=None, inventario=None, editoriales=None,
                 generos=None, monedas=None, cotizaciones=None):
        secciones = [
            ("Catálogo de Libros", catalogo if catalogo is not None else ConsolaCatalogo()),
            ("Inventario", inventario if inventario is not None else ConsolaInventario()),
            ("Gestión de Editoriales", editoriales if editoriales is not None else ConsolaEditoriales()),
            ("Gestión de Géneros", generos if generos is not None else ConsolaGeneros()),
            ("Gestión de Monedas", monedas if monedas is not None else ConsolaMonedas()),
            ("Cotizaciones", cotizaciones if cotizaciones is not None else ConsolaCotizaciones()),
        ]
        super().__init__("MENÚ PRINCIPAL", {
            str(numero): (titulo, consola.ejecutar)
            for numero, (titulo, consola) in enumerate(secciones, start=1)
        }, salida="Salir")
