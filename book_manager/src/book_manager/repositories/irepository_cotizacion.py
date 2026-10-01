import abc
from datetime import date
from typing import List, Optional

from entities.cotizacion import Cotizacion
class IRepositorioCotizacion(abc.ABC):
  """Interfaz para repositorios del tipo RepositorioCotizacion."""

  @abc.abstractmethod
  def crear(self, cotizacion: 'Cotizacion') -> 'Cotizacion':
    """Crea una nueva cotización de dólar.

    Args:
        cotizacion (CotizacionDolar): El objeto CotizacionDolar a crear.

    Returns:
        CotizacionDolar: El objeto CotizacionDolar creado.

    Raises:
        ValueError: Si ya existe una cotización para el mismo tipo y fecha.
    """
    pass

  @abc.abstractmethod
  def leer_por_tipo_moneda_origen_destino_y_fecha( self, 
                                                    tipo_id: int, 
                                                    moneda_origen_id: int, 
                                                    moneda_destino_id: int, 
                                                    fecha: date) -> Optional['Cotizacion']:
    """Lee una cotización de dólar por tipo y fecha.

    Args:
        tipo_id (int): El ID del tipo de cotización (e.g., 'Oficial', 'Blue').
        moneda_origen_id (int): El ID de la moneda de origen.
        moneda_destino_id (int): El ID de la moneda de destino.
        fecha (datetime.date): La fecha de la cotización.

    Returns:
        Optional[CotizacionDolar]: La cotización si se encuentra, None en caso contrario.
    """
    pass

  @abc.abstractmethod
  def leer_historico_por_tipo_moneda_origen_moneda_destino( self, 
                                                            tipo_id: int, 
                                                            moneda_origen_id :int, 
                                                            moneda_destino_id: int) -> List['Cotizacion']:
    """Lee el histórico de cotizaciones para un tipo específico.

    Args:
        tipo_id (int): El ID del tipo de cotización.
        moneda_origen_id (int): El ID de la moneda de origen.
        moneda_destino_id (int): El ID de la moneda de destino.

    Returns:
        List[CotizacionDolar]: Una lista de cotizaciones históricas para el tipo dado.
    """
    pass

  @abc.abstractmethod
  def actualizar(self, cotizacion: 'Cotizacion') -> 'Cotizacion':
    """Actualiza una cotización de dólar existente.

    Args:
        cotizacion (CotizacionDolar): El objeto CotizacionDolar a actualizar.

    Returns:
        CotizacionDolar: El objeto CotizacionDolar actualizado.
    """
    pass

  @abc.abstractmethod
  def eliminar(self, 
               tipo_id: int, 
               moneda_origen_id: 
               int, moneda_destino_id: 
               int, fecha: date) -> bool:
    """Elimina una cotización de dólar por tipo y fecha.

    Args:
        tipo_id (int): El ID del tipo de cotización.
        moneda_origen_id (int): El ID de la moneda de origen.
        moneda_destino_id (int): El ID de la moneda de destino.
        fecha (datetime.date): La fecha de la cotización a eliminar.

    Returns:
        bool: True si la cotización fue eliminada, False si no se encontró.
    """
    pass