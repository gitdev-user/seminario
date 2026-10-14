"""Define la configuración de la aplicación y las rutas de sus repositorios CSV."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


RAIZ_PROYECTO = Path(__file__).resolve().parents[3]


class Configuracion(BaseSettings):
    """Centraliza las opciones de la aplicación y de los repositorios CSV.

    Utiliza valores predeterminados que pueden sobrescribirse mediante el
    archivo ``book_manager/.env`` o variables de entorno. Las variables de
    entorno tienen prioridad sobre los valores del archivo.
    """

    model_config = SettingsConfigDict(
        env_file=RAIZ_PROYECTO / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_nombre: str = "SISTEMA GESTION DE LIBRERIA"
    app_debug: bool = False

    repositorio_carpeta: Path = Path("src/book_manager/migrations/csv")
    repositorio_editoriales: str = "editoriales.csv"
    repositorio_generos: str = "generos.csv"
    repositorio_libros: str = "libros.csv"
    repositorio_monedas: str = "monedas.csv"
    repositorio_tipos_cotizacion: str = "tipos_cotizacion.csv"
    repositorio_precios: str = "precios.csv"
    repositorio_stock: str = "stock.csv"
    repositorio_cotizaciones: str = "cotizaciones.csv"

    @property
    def directorio_repositorio(self) -> Path:
        """Devuelve la ruta absoluta de la carpeta de repositorios CSV.

        Si ``repositorio_carpeta`` es relativa, se resuelve respecto de la raíz
        de ``book_manager``; si es absoluta, se utiliza esa ubicación.
        """
        return (RAIZ_PROYECTO / self.repositorio_carpeta).resolve()

    def ruta_repositorio(self, nombre: str) -> Path:
        """Construye la ruta de un archivo dentro de la carpeta de repositorios.

        Args:
            nombre: Nombre del archivo CSV, por ejemplo ``editoriales.csv``.

        Returns:
            Ruta del archivo, sin comprobar su existencia ni crearlo.
        """
        return self.directorio_repositorio / nombre


config = Configuracion()
