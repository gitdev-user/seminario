from ui.consola import ConsolaMenu
from ui.consola_gestion_cotizaciones import ConsolaGestionCotizaciones
from ui.consola_tipos_cotizacion import ConsolaTiposCotizacion


class ConsolaCotizaciones(ConsolaMenu):
    def __init__(self, cotizaciones=None, tipos=None):
        cotizaciones = cotizaciones if cotizaciones is not None else ConsolaGestionCotizaciones()
        tipos = tipos if tipos is not None else ConsolaTiposCotizacion()
        super().__init__("Cotizaciones", {
            "1": ("Gestión de Cotizaciones", cotizaciones.ejecutar),
            "2": ("Gestión de Tipos de Cotización", tipos.ejecutar),
        })

