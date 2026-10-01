from entities.tipo_cotizacion import TipoCotizacion
from ui.consola_entidad import ConsolaEntidad


class ConsolaTiposCotizacion(ConsolaEntidad):
    MODELO = TipoCotizacion
    TITULO = "Gestión de Tipos de Cotización"
    NOMBRE = "Tipo de Cotización"
    CAMPOS = (
        ("nombre", "Nombre"),
        ("descripcion", "Descripción"),
    )