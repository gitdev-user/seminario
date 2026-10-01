from entities.genero import Genero
from ui.consola_entidad import ConsolaEntidad


class ConsolaGeneros(ConsolaEntidad):
    MODELO = Genero
    TITULO = "Gestión de Géneros"
    NOMBRE = "Género"
    CAMPOS = (
        ("nombre", "Nombre"),
        ("descripcion", "Descripción"),
    )