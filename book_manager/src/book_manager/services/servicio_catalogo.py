from typing import List, Optional

from dto.libro_detalle import LibroDetalle
from entities.libro import Libro
from repositories.irepositorio_precio import IRepositorioPrecio
from repositories.irepositorio_stock import IRepositorioStock
from repositories.impl.csv_archivo_repositorio_libro_impl import (
    CSVArchivoRepositorioLibro,
)
from services.servicio_editorial import ServicioEditorial
from services.servicio_genero import ServicioGenero
from services.servicio_inventario import ServicioInventario


class ServicioCatalogo:
    """Gestiona el CRUD de libros y sus consultas de detalle."""

    def __init__(
        self,
        repositorio: CSVArchivoRepositorioLibro,
        servicio_editorial: ServicioEditorial,
        servicio_genero: ServicioGenero,
        servicio_inventario: ServicioInventario,
        repositorio_precio: IRepositorioPrecio,
        repositorio_stock: IRepositorioStock,
    ):
        self.repositorio = repositorio
        self.servicio_editorial = servicio_editorial
        self.servicio_genero = servicio_genero
        self.servicio_inventario = servicio_inventario
        self.repositorio_precio = repositorio_precio
        self.repositorio_stock = repositorio_stock

    def guardar(self, libro: Libro) -> Libro:
        """Valida editorial y género, y crea o actualiza el libro según exista o no su ID.

        Raises:
            ValueError: Si la editorial o el género indicados no existen.
        """
        editorial = self.servicio_editorial.leer_por_id(libro.editorial_id)
        if editorial is None:
            raise ValueError(
                f"No existe una editorial con ID {libro.editorial_id}"
            )

        genero = self.servicio_genero.leer_por_id(libro.genero_id)
        if genero is None:
            raise ValueError(f"No existe un género con ID {libro.genero_id}")

        if self.repositorio.leer_por_id(libro.id) is None:
            return self.repositorio.crear(libro)
        return self.repositorio.actualizar(libro)

    def eliminar(self, id: int) -> bool:
        """Elimina precio y stock asociados antes de eliminar el libro.

        Devuelve False si el libro no existe. Los errores de escritura se
        propagan; la eliminación en varios CSV no es una transacción atómica.
        """
        if self.repositorio.leer_por_id(id) is None:
            return False
        self.repositorio_precio.eliminar(id)
        self.repositorio_stock.eliminar(id)
        return self.repositorio.eliminar(id)

    def leer_por_id(self, id: int) -> Optional[Libro]:
        """Devuelve el libro con el ID indicado, o None si no existe."""
        return self.repositorio.leer_por_id(id)

    def listar_todos(self) -> List[Libro]:
        """Devuelve la lista de libros del repositorio."""
        return self.repositorio.leer_todos()

    def leer_detalle_por_id(self, id: int) -> Optional[LibroDetalle]:
        """Reúne el libro y sus relaciones; devuelve None si el libro no existe.

        Precio y stock pueden estar ausentes. Una editorial, género o moneda
        referenciados que no existan producen un ValueError.
        """
        libro = self.repositorio.leer_por_id(id)
        if libro is None:
            return None

        editorial = self.servicio_editorial.leer_por_id(libro.editorial_id)
        if editorial is None:
            raise ValueError(
                f"No existe una editorial con ID {libro.editorial_id}"
            )

        genero = self.servicio_genero.leer_por_id(libro.genero_id)
        if genero is None:
            raise ValueError(f"No existe un género con ID {libro.genero_id}")

        precio_detalle = self.servicio_inventario.leer_precio_detalle_por_libro(libro.id)
        stock = self.servicio_inventario.leer_stock_por_libro(libro.id)
        return LibroDetalle(
            libro=libro,
            editorial=editorial,
            genero=genero,
            precio=precio_detalle,
            stock=stock,
        )
