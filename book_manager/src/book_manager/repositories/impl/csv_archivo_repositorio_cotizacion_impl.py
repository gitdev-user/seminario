from datetime import date
from typing import List, Optional

import pandas as pd

from entities.cotizacion import Cotizacion
from repositories.irepository_cotizacion import IRepositorioCotizacion
from utils.manejador_csv import ManejadorCSV


class CSVArchivoRepositorioCotizacion(IRepositorioCotizacion):
    """Persiste cotizaciones por tipo, monedas de origen y destino, y fecha."""

    def __init__(self, ruta_archivo: str):
        self.manejador_csv = ManejadorCSV(ruta_archivo, list(Cotizacion.model_fields.keys()))

    def crear(self, cotizacion: Cotizacion) -> Cotizacion:
        df = self.manejador_csv.cargar_dataframe()
        fecha_str = str(cotizacion.fecha)

        filtro = (
            (df['tipo_cotizacion_id'] == cotizacion.tipo_cotizacion_id)
            & (df['moneda_origen_id'] == cotizacion.moneda_origen_id)
            & (df['moneda_destino_id'] == cotizacion.moneda_destino_id)
            & (df['fecha'] == fecha_str)
        )
        if filtro.any():
            raise ValueError(
                f"Ya existe una cotización para el tipo {cotizacion.tipo_cotizacion_id}, "
                f"las monedas {cotizacion.moneda_origen_id} y "
                f"{cotizacion.moneda_destino_id} en la fecha {fecha_str}"
            )

        # Serializamos la fecha y el valor decimal para guardarlos en el CSV.
        nuevo_registro = pd.DataFrame([cotizacion.model_dump(mode='json')])
        df = nuevo_registro if df.empty else pd.concat(
            [df, nuevo_registro], ignore_index=True
        )
        self.manejador_csv.guardar_dataframe(df)
        return cotizacion

    def leer_por_tipo_moneda_origen_destino_y_fecha(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int,
        fecha: date,
    ) -> Optional[Cotizacion]:
        
        df = self.manejador_csv.cargar_dataframe()
        filtro = (
            (df['tipo_cotizacion_id'] == tipo_id)
            & (df['moneda_origen_id'] == moneda_origen_id)
            & (df['moneda_destino_id'] == moneda_destino_id)
            & (df['fecha'] == str(fecha))
        )
        registro = df[filtro]
        if registro.empty:
            return None

        datos = registro.iloc[0].to_dict()
        datos['fecha'] = date.fromisoformat(str(datos['fecha']))
        return Cotizacion(**datos)

    def leer_historico_por_tipo_moneda_origen_moneda_destino(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int,
    ) -> List[Cotizacion]:
        
        df = self.manejador_csv.cargar_dataframe()
        filtro = (
            (df['tipo_cotizacion_id'] == tipo_id)
            & (df['moneda_origen_id'] == moneda_origen_id)
            & (df['moneda_destino_id'] == moneda_destino_id)
        )
        registros = df[filtro]
        lista_registros = []
        for _, registro in registros.iterrows():
            datos = registro.to_dict()
            datos['fecha'] = date.fromisoformat(str(datos['fecha']))
            lista_registros.append(Cotizacion(**datos))
        return lista_registros

    def actualizar(self, cotizacion: Cotizacion) -> Cotizacion:
        df = self.manejador_csv.cargar_dataframe()
        filtro = (
            (df['tipo_cotizacion_id'] == cotizacion.tipo_cotizacion_id)
            & (df['moneda_origen_id'] == cotizacion.moneda_origen_id)
            & (df['moneda_destino_id'] == cotizacion.moneda_destino_id)
            & (df['fecha'] == str(cotizacion.fecha))
        )
        if not filtro.any():
            raise ValueError('No se encontró la cotización para actualizar.')

        # Actualizamos todas las columnas excepto el ID mapeando el diccionario de la entidad
        for columna in df.columns:
            if columna not in ['moneda_origen_id', 'moneda_destino_id', 'tipo_cotizacion_id', 'fecha']:
                df[columna] = df[columna].astype(object)
                df.loc[filtro, columna] = cotizacion.model_dump(mode="json")[columna]
        
        self.manejador_csv.guardar_dataframe(df)
        return cotizacion

    def eliminar(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int,
        fecha: date,
    ) -> bool:
        df = self.manejador_csv.cargar_dataframe()
        filtro_a_eliminar = (
            (df['tipo_cotizacion_id'] == tipo_id)
            & (df['moneda_origen_id'] == moneda_origen_id)
            & (df['moneda_destino_id'] == moneda_destino_id)
            & (df['fecha'] == str(fecha))
        )
        if not filtro_a_eliminar.any():
            return False

        df = df[~filtro_a_eliminar]
        self.manejador_csv.guardar_dataframe(df)
        return True
