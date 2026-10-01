import abc 
from typing import Optional

from entities.precio import Precio

class IRepositorioPrecio(abc.ABC):
  """Interfaz para repositorios del tipo Precio."""

  @abc.abstractmethod
  def crear(self, precio: Precio) -> Precio:
    """Crea un nuevo registro de precio para un libro.

    Args:
        precio (Precio): El objeto Precio a crear.

    Returns:
        Precio: El objeto Precio creado.

    Raises:
        ValueError: Si ya existe un precio asignado a ese mismo libro.
    """
    pass

  @abc.abstractmethod
  def leer_por_libro(self, libro_id: int) -> Optional[Precio]:
    """Lee el precio de un libro por su ID de libro.

    Args:
        libro_id (int): El ID del libro asociado al precio.

    Returns:
        Optional[Precio]: El objeto Precio si se encuentra, None en caso contrario.
    """
    pass

  @abc.abstractmethod
  def actualizar(self, precio: Precio) -> Precio:
    """Actualiza un registro de precio existente.

    Args:
        precio (Precio): El objeto Precio a actualizar.

    Returns:
        Precio: El objeto Precio actualizado.

    Raises:
        ValueError: Si no se encuentra el precio para actualizar.
    """
    pass

  @abc.abstractmethod
  def eliminar(self, libro_id: int) -> bool:
    """Elimina el registro de precio de un libro por su ID de libro.

    Args:
        libro_id (int): El ID del libro asociado al precio a eliminar.

    Returns:
        bool: True si el precio fue eliminado, False si no se encontró.
    """
    pass