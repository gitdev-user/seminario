import pandas as pd
from typing import TypeVar, List, Optional

from entities.entidad_base import EntidadBase
from repositories.irepositorio import IRepositorio
from utils.manejador_csv import ManejadorCSV

T = TypeVar('T', bound=EntidadBase)

class CSVArchivoRepositorioImpl(IRepositorio[T]):
    """Implementación genérica de operaciones CRUD para entidades con campo 'id'."""
    
    def __init__(self, ruta_archivo: str, clase_entidad: type[T]):
        self.clase_modelo = clase_entidad
        self.manejador_csv = ManejadorCSV(
            ruta_archivo, list(clase_entidad.model_fields)
        )

    def crear(self, entidad: T) -> T:
        df = self.manejador_csv.cargar_dataframe()
        if not df.empty and entidad.id in df['id'].values:
            raise ValueError(f"Ya existe un registro con ID {entidad.id}.")

        if entidad.id == 0:
            entidad.id = 1 if df.empty else int(df["id"].max()) + 1

        nuevo_registro = pd.DataFrame([entidad.model_dump(mode="json")])
        if df.empty:
            df = nuevo_registro
        else:
            df = pd.concat([df, nuevo_registro], ignore_index=True)
        self.manejador_csv.guardar_dataframe(df)
        return entidad

    def leer_por_id(self, id: int) -> Optional[T]:
        df = self.manejador_csv.cargar_dataframe()
        registro = df[df['id'] == id]
        if registro.empty:
            return None
        return self.clase_modelo(**registro.iloc[0].to_dict())

    def leer_todos(self) -> List[T]:
        df = self.manejador_csv.cargar_dataframe()
        return [self.clase_modelo(**registro.to_dict()) for _, registro in df.iterrows()]

    def actualizar(self, entidad: T) -> T:
        df = self.manejador_csv.cargar_dataframe()
        if df.empty or entidad.id not in df['id'].values:
            raise ValueError(f"No se encontró el registro con ID {entidad.id} para actualizar.")
            
        # Actualizamos todas las columnas excepto el ID mapeando el diccionario de la entidad
        for columna in df.columns:
            if columna != 'id':
                df.loc[df['id'] == entidad.id, [columna]] = getattr(entidad, columna)
                
        self.manejador_csv.guardar_dataframe(df)

        return entidad

    def eliminar(self, id: int) -> bool:
        df = self.manejador_csv.cargar_dataframe()
        tamano_inicial = len(df)
        df = df[df['id'] != id]
        
        if len(df) == tamano_inicial:
            return False
            
        self.manejador_csv.guardar_dataframe(df)
        return True
