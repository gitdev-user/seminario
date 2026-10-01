from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


RAIZ_PROYECTO = Path(__file__).resolve().parents[3]


class Configuracion(BaseSettings):
    """Carga la configuración compartida desde book_manager/.env."""

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
        """Resuelve la carpeta respecto del proyecto, también en Colab."""
        return (RAIZ_PROYECTO / self.repositorio_carpeta).resolve()

    def ruta_repositorio(self, nombre: str) -> Path:
        return self.directorio_repositorio / nombre


config = Configuracion()
