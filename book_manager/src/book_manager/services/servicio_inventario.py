from typing import Optional

from dto.precio_detalle import PrecioDetalle
from entities.precio import Precio
from entities.stock import Stock
from repositories.irepositorio_precio import IRepositorioPrecio
from repositories.irepositorio_stock import IRepositorioStock
from repositories.impl.csv_archivo_repositorio_libro_impl import CSVArchivoRepositorioLibro
from repositories.impl.csv_archivo_repositorio_moneda_impl import CSVArchivoRepositorioMoneda


class ServicioInventario:
    """Gestiona el precio y el stock de los libros."""

    def __init__(
        self,
        repositorio_libro: CSVArchivoRepositorioLibro,
        repositorio_precio: IRepositorioPrecio,
        repositorio_stock: IRepositorioStock,
        repositorio_moneda: CSVArchivoRepositorioMoneda,
    ):
        self.repositorio_libro = repositorio_libro
        self.repositorio_precio = repositorio_precio
        self.repositorio_stock = repositorio_stock
        self.repositorio_moneda = repositorio_moneda

    def guardar_precio(self, precio: Precio) -> Precio:
        """Valida libro y moneda, y crea o actualiza el precio del libro."""
        if self.repositorio_libro.leer_por_id(precio.libro_id) is None:
            raise ValueError(f"No existe un libro con ID {precio.libro_id}")
        if self.repositorio_moneda.leer_por_id(precio.moneda_base_id) is None:
            raise ValueError(f"No existe una moneda con ID {precio.moneda_base_id}")

        existente = self.leer_precio_por_libro(precio.libro_id)
        if existente is None:
            return self.repositorio_precio.crear(precio)
        return self.repositorio_precio.actualizar(precio)

    def guardar_stock(self, stock: Stock) -> Stock:
        """Valida que exista el libro y crea o actualiza su stock."""
        if self.repositorio_libro.leer_por_id(stock.libro_id) is None:
            raise ValueError(f"No existe un libro con ID {stock.libro_id}")

        existente = self.leer_stock_por_libro(stock.libro_id)
        if existente is None:
            return self.repositorio_stock.crear(stock)
        return self.repositorio_stock.actualizar(stock)

    def leer_precio_por_libro(self, libro_id: int) -> Optional[Precio]:
        """Devuelve el precio del libro, o None si no tiene uno registrado."""
        return self.repositorio_precio.leer_por_libro(libro_id)

    def leer_stock_por_libro(self, libro_id: int) -> Optional[Stock]:
        """Devuelve el stock del libro, o None si no tiene uno registrado."""
        return self.repositorio_stock.leer_por_libro(libro_id)

    def leer_precio_detalle_por_libro(self, libro_id: int) -> Optional[PrecioDetalle]:
        """Devuelve precio y moneda, o None si no hay precio registrado.

        Lanza ValueError si la moneda referenciada no existe.
        """
        precio = self.leer_precio_por_libro(libro_id)
        if precio is None:
            return None
        moneda = self.repositorio_moneda.leer_por_id(precio.moneda_base_id)
        if moneda is None:
            raise ValueError(f"No existe una moneda con ID {precio.moneda_base_id}")
        return PrecioDetalle(precio=precio, moneda=moneda)
