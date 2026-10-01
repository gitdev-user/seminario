from typing import Optional

import pandas as pd

from entities.stock import Stock
from repositories.irepositorio_stock import IRepositorioStock
from utils.manejador_csv import ManejadorCSV


class CSVArchivoRepositorioStockImpl(IRepositorioStock):
    """Repositorio CSV de stock identificado por el ID del libro."""

    def __init__(self, ruta_archivo: str = "data/stock.csv"):
        self.manejador_csv = ManejadorCSV(ruta_archivo, list(Stock.model_fields.keys()))

    def crear(self, stock: Stock) -> Stock:
        df = self.manejador_csv.cargar_dataframe()
                
        # Validamos si ya existe la clave 'libro_id' en el DataFrame
        if not df.empty and stock.libro_id in df['libro_id'].values:
            raise ValueError(f"Ya existe un registro de stock para el libro {stock.libro_id}")

        nuevo_registro = pd.DataFrame([stock.__dict__])
        df = pd.concat([df, nuevo_registro], ignore_index=True)
        self.manejador_csv.guardar_dataframe(df)
        return stock

    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        df = self.manejador_csv.cargar_dataframe()

        # Filtrado directo por la columna del libro
        registro = df[df['libro_id'] == libro_id]
        if registro.empty:
            return None
        return Stock(**registro.iloc[0].to_dict())

    def actualizar(self, stock: Stock) -> Stock:
        df = self.manejador_csv.cargar_dataframe()
                
        if df.empty or stock.libro_id not in df['libro_id'].values:
            raise ValueError(f"No se encontró un registro de stock para el libro {stock.libro_id} para actualizar.")
            
        # Actualizamos todas las columnas excepto el ID mapeando el diccionario de la entidad
        for columna in df.columns:
            if columna != 'libro_id':
                df.loc[df['libro_id'] == stock.libro_id, [columna]] = getattr(stock, columna)

        self.manejador_csv.guardar_dataframe(df)
        return stock

    def eliminar(self, libro_id: int) -> bool:
        df = self.manejador_csv.cargar_dataframe()
        tamano_inicial = len(df)
                
        # Filtro inverso para descartar la fila indicada
        df = df[df['libro_id'] != libro_id]
                
        if len(df) == tamano_inicial:
            return False  # No se alteró el DataFrame porque no existía el registro
        
        self.manejador_csv.guardar_dataframe(df)
        return True
