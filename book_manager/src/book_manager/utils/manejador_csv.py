import pandas as pd
from pathlib import Path

class ManejadorCSV:
    """Clase base encargada puramente de la persistencia con Pandas."""
    
    def __init__(self, ruta_archivo: str, columnas: list):
        self.ruta_archivo = ruta_archivo
        self.columnas = columnas

    def cargar_dataframe(self) -> pd.DataFrame:
        """Lee el archivo CSV retornando un DataFrame de Pandas."""
        try:
            return pd.read_csv(
                self.ruta_archivo,
                dtype={"telefono": str, "isbn": str},
                keep_default_na=False,
            )
        except FileNotFoundError:
            # Si no existe, inicializa las columnas basadas en las anotaciones del modelo
            return pd.DataFrame(columns=self.columnas)

    def guardar_dataframe(self, df: pd.DataFrame) -> None:
        """Persiste las mutaciones del DataFrame de vuelta al archivo CSV."""
        Path(self.ruta_archivo).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.ruta_archivo, index=False)
