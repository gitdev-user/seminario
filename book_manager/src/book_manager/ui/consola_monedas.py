from entities.moneda import Moneda
from ui.consola_entidad import ConsolaEntidad


class ConsolaMonedas(ConsolaEntidad):
    MODELO = Moneda
    TITULO = "Gestión de Monedas"
    NOMBRE = "Moneda"
    CAMPOS = (
        ("codigo_iso", "Código ISO"),
        ("nombre", "Nombre"),
        ("simbolo", "Símbolo"),
    )