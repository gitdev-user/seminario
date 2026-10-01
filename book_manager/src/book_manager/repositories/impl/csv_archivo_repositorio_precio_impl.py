from typing import Optional

import pandas as pd


from entities.precio import Precio
from repositories.irepositorio_precio import IRepositorioPrecio

from utils.manejador_csv import ManejadorCSV


class CSVArchivoRepositorioPrecioImpl(IRepositorioPrecio):
    """Repositorio CSV de precio identificado por el ID del libro."""

    def __init__(self, ruta_archivo: str = "data/precios.csv"):
        self.manejador_csv = ManejadorCSV(ruta_archivo, list(Precio.model_fields.keys()))

    def crear(self, precio: Precio) -> Precio:
        df = self.manejador_csv.cargar_dataframe()
                
        # Validamos si ya existe la clave 'libro_id' en el DataFrame
        if not df.empty and precio.libro_id in df['libro_id'].values:
            raise ValueError(f"Ya existe un registro de precio para el libro {precio.libro_id}")

        nuevo_registro = pd.DataFrame([precio.model_dump(mode="json")])
        df = pd.concat([df, nuevo_registro], ignore_index=True)
        self.manejador_csv.guardar_dataframe(df)
        return precio

    def leer_por_libro(self, libro_id: int) -> Optional[Precio]:
        df = self.manejador_csv.cargar_dataframe()

        # Filtrado directo por la columna del libro
        registro = df[df['libro_id'] == libro_id]
        if registro.empty:
            return None
        return Precio(**registro.iloc[0].to_dict())

    def actualizar(self, precio: Precio) -> Precio:
        df = self.manejador_csv.cargar_dataframe()
                
        if df.empty or precio.libro_id not in df['libro_id'].values:
            raise ValueError(f"No se encontró un registro de precio para el libro {precio.libro_id} para actualizar.")
            
        # Actualizamos todas las columnas excepto el ID mapeando el diccionario de la entidad
        for columna in df.columns:
            if columna != 'libro_id':
                df[columna] = df[columna].astype(object)
                df.loc[df['libro_id'] == precio.libro_id, columna] = precio.model_dump(mode='json')[columna]

        self.manejador_csv.guardar_dataframe(df)
        return precio

    def eliminar(self, libro_id: int) -> bool:
        df = self.manejador_csv.cargar_dataframe()
        tamano_inicial = len(df)
                
        # Filtro inverso para descartar la fila indicada
        df = df[df['libro_id'] != libro_id]
                
        if len(df) == tamano_inicial:
            return False  # No se alteró el DataFrame porque no existía el registro
        
        self.manejador_csv.guardar_dataframe(df)
        return True
