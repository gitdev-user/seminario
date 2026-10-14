"""Servicios de negocio que utilizan los repositorios SQLAlchemy de la aplicación."""

from datetime import date
from typing import List, Optional

from entities.entities import Cotizacion, Editorial, Genero, Libro, Moneda, Precio, Stock, TipoCotizacion
from repositories.repositories import (
    RepositorioCotizacion,
    RepositorioEditorial,
    RepositorioGenero,
    RepositorioLibro,
    RepositorioMoneda,
    RepositorioPrecio,
    RepositorioStock,
    RepositorioTipoCotizacion,
)

class ServicioInventario:
    """Gestiona precios y stock asociados a libros mediante claves foráneas."""

    def __init__(
        self,
        repositorio_libro: RepositorioLibro,
        repositorio_precio: RepositorioPrecio,
        repositorio_stock: RepositorioStock,
        repositorio_moneda: RepositorioMoneda,
    ):
        """Recibe los repositorios de libros, precios, stock y monedas."""
        self.repositorio_libro = repositorio_libro
        self.repositorio_precio = repositorio_precio
        self.repositorio_stock = repositorio_stock
        self.repositorio_moneda = repositorio_moneda

    def guardar_precio(self, precio: Precio) -> Precio:
        """Valida libro y moneda y guarda el precio identificado por libro_id."""
        libro = self.repositorio_libro.leer_por_id(precio.libro_id)
        if libro is None:
            raise ValueError(f"No existe un libro con ID {precio.libro_id}.")

        moneda = self.repositorio_moneda.leer_por_id(precio.moneda.id)
        if moneda is None:
            raise ValueError(f"No existe una moneda con ID {precio.moneda.id}.")

        precio.moneda = moneda
        if self.repositorio_precio.leer_por_libro(precio.libro_id) is None:
            guardado = self.repositorio_precio.crear(precio)
        else:
            guardado = self.repositorio_precio.actualizar(precio)

        return guardado

    def guardar_stock(self, stock: Stock) -> Stock:
        """Valida el libro y guarda el stock identificado por libro_id."""
        libro = self.repositorio_libro.leer_por_id(stock.libro_id)
        if libro is None:
            raise ValueError(f"No existe un libro con ID {stock.libro_id}.")

        if self.repositorio_stock.leer_por_libro(stock.libro_id) is None:
            guardado = self.repositorio_stock.crear(stock)
        else:
            guardado = self.repositorio_stock.actualizar(stock)

        return guardado

    def leer_precio_por_libro(self, libro_id: int) -> Optional[Precio]:
        """Devuelve el precio registrado para el libro, o None si no existe."""
        return self.repositorio_precio.leer_por_libro(libro_id)

    def leer_stock_por_libro(self, libro_id: int) -> Optional[Stock]:
        """Devuelve el stock registrado para el libro, o None si no existe."""
        return self.repositorio_stock.leer_por_libro(libro_id)

    def eliminar_precio_por_libro(self, libro_id: int) -> bool:
        """Elimina el registro de precio; el libro permanece guardado."""
        return self.repositorio_precio.eliminar(libro_id)

    def eliminar_stock_por_libro(self, libro_id: int) -> bool:
        """Elimina el registro de stock; el libro permanece guardado."""
        return self.repositorio_stock.eliminar(libro_id)


class ServicioCotizacion:
    """Gestiona cotizaciones identificadas por tipo, monedas y fecha."""

    def __init__(self, repositorio: RepositorioCotizacion):
        """Recibe el repositorio de cotizaciones de la aplicación."""
        self.repositorio = repositorio

    def guardar(self, cotizacion: Cotizacion) -> Cotizacion:
        """Crea la cotización o actualiza su valor si ya existe su clave."""
        existente = self.repositorio.leer_por_tipo_moneda_origen_destino_y_fecha(
            cotizacion.tipo_cotizacion.id,
            cotizacion.moneda_origen.id,
            cotizacion.moneda_destino.id,
            cotizacion.fecha,
        )

        if existente is None:
            return self.repositorio.crear(cotizacion)

        return self.repositorio.actualizar(cotizacion)

    def eliminar(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int,
        fecha: date,
    ) -> bool:
        """Elimina la cotización indicada; devuelve False si no existe."""
        return self.repositorio.eliminar(
            tipo_id, moneda_origen_id, moneda_destino_id, fecha
        )

    def leer_por_tipo_moneda_origen_destino_y_fecha(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int,
        fecha: date,
    ) -> Optional[Cotizacion]:
        """Devuelve la cotización indicada, o None si no existe."""
        return self.repositorio.leer_por_tipo_moneda_origen_destino_y_fecha(
            tipo_id, moneda_origen_id, moneda_destino_id, fecha
        )

    def leer_historico_por_tipo_moneda_origen_moneda_destino(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int,
    ) -> List[Cotizacion]:
        """Devuelve el histórico del tipo y las monedas, ordenado por fecha."""
        return self.repositorio.leer_historico_por_tipo_moneda_origen_moneda_destino(
            tipo_id, moneda_origen_id, moneda_destino_id
        )


class ServicioCatalogo:
    """Gestiona las operaciones CRUD de libros, evitando ISBN duplicados."""

    def __init__(
        self,
        repositorio: RepositorioLibro,
        repositorio_editorial: RepositorioEditorial,
        repositorio_genero: RepositorioGenero,
        repositorio_precio: RepositorioPrecio,
        repositorio_stock: RepositorioStock,
    ):
        """Recibe los repositorios de libros y sus entidades relacionadas."""
        self.repositorio = repositorio
        self.repositorio_editorial = repositorio_editorial
        self.repositorio_genero = repositorio_genero
        self.repositorio_precio = repositorio_precio
        self.repositorio_stock = repositorio_stock

    def guardar(self, libro: Libro) -> Libro:
        """Valida editorial, género e ISBN único antes de crear o actualizar.

        Raises:
            ValueError: Si la editorial o el género no existen, o si otro
                libro tiene el mismo ISBN.
        """

        libro_id = getattr(libro, "id", None)
        existente = self.repositorio.leer_por_isbn(libro.isbn)

        if existente is not None and existente.id != libro_id:
            raise ValueError(
                f"Ya existe un libro con ISBN '{libro.isbn}'."
            )

        if self.repositorio_editorial.leer_por_id(libro.editorial.id) is None:
            raise ValueError(
                f"No existe una editorial asignada con ID {libro.editorial.id}."
            )
        
        if self.repositorio_genero.leer_por_id(libro.genero.id) is None:
            raise ValueError(
                f"No existe un género asignado con ID {libro.genero.id}."
            )

        if libro_id is None or self.repositorio.leer_por_id(libro_id) is None:
            return self.repositorio.crear(libro)

        return self.repositorio.actualizar(libro)

    def eliminar(self, id: int) -> bool:
        """Elimina el libro y sus relaciones mediante la cascada del repositorio.

        Devuelve False si el libro no existe.
        """
        return self.repositorio.eliminar(id)

    def leer_por_id(self, id: int) -> Optional[Libro]:
        """Devuelve el libro con el ID indicado, o None si no existe."""
        return self.repositorio.leer_por_id(id)

    def listar_todos(self) -> List[Libro]:
        """Devuelve todos los libros del repositorio."""
        return self.repositorio.leer_todos()


class ServicioEditorial:
    """Gestiona editoriales, evitando nombres duplicados y eliminaciones en uso."""

    def __init__(
        self,
        repositorio: RepositorioEditorial,
        repositorio_libro: RepositorioLibro,
    ):
        """Recibe los repositorios de editoriales y libros de la aplicación."""
        self.repositorio = repositorio
        self.repositorio_libro = repositorio_libro

    def guardar(self, editorial: Editorial) -> Editorial:
        """Crea o actualiza la editorial, evitando nombres duplicados."""
        existente = self.repositorio.leer_por_nombre(editorial.nombre)

        if existente is not None and existente.id != editorial.id:
            raise ValueError(
                f"Ya existe una editorial con nombre '{editorial.nombre}'."
            )

        if editorial.id is None or self.repositorio.leer_por_id(editorial.id) is None:
            return self.repositorio.crear(editorial)

        return self.repositorio.actualizar(editorial)

    def leer_por_id(self, id: int) -> Optional[Editorial]:
        """Devuelve la editorial con el ID indicado, o None si no existe."""
        return self.repositorio.leer_por_id(id)

    def leer_todos(self) -> List[Editorial]:
        """Devuelve todas las editoriales del repositorio."""
        return self.repositorio.leer_todos()

    def eliminar(self, id: int) -> bool:
        """Elimina la editorial si no está en uso; devuelve False si no existe."""

        if self.repositorio_libro.existe_por_editorial(id):
            raise ValueError(
                f"No se puede eliminar la editorial con ID {id} "
                "porque está utilizada en libros."
            )

        return self.repositorio.eliminar(id)


class ServicioGenero:
    """Gestiona géneros, evitando nombres duplicados y eliminaciones en uso."""

    def __init__(
        self,
        repositorio: RepositorioGenero,
        repositorio_libro: RepositorioLibro,
    ):
        """Recibe los repositorios de géneros y libros de la aplicación."""
        self.repositorio = repositorio
        self.repositorio_libro = repositorio_libro

    def guardar(self, genero: Genero) -> Genero:
        """Crea o actualiza el género, evitando nombres duplicados."""
        existente = self.repositorio.leer_por_nombre(genero.nombre)

        if existente is not None and existente.id != genero.id:
            raise ValueError(
                f"Ya existe un género con nombre '{genero.nombre}'."
            )

        if genero.id is None or self.repositorio.leer_por_id(genero.id) is None:
            return self.repositorio.crear(genero)

        return self.repositorio.actualizar(genero)

    def leer_por_id(self, id: int) -> Optional[Genero]:
        """Devuelve el género con el ID indicado, o None si no existe."""
        return self.repositorio.leer_por_id(id)

    def leer_todos(self) -> List[Genero]:
        """Devuelve todos los géneros del repositorio."""
        return self.repositorio.leer_todos()

    def eliminar(self, id: int) -> bool:
        """Elimina el género si no está en uso; devuelve False si no existe."""

        if self.repositorio_libro.existe_por_genero(id):
            raise ValueError(
                f"No se puede eliminar el género con ID {id} "
                "porque está utilizado en libros."
            )

        return self.repositorio.eliminar(id)


class ServicioTipoCotizacion:
    """Gestiona las operaciones CRUD de tipos de cotización."""

    def __init__(
            self, 
            repositorio: RepositorioTipoCotizacion,
            repositorio_cotizacion: RepositorioCotizacion
            ):
        """Recibe los repositorios de tipos de cotización y cotizaciones."""
        self.repositorio = repositorio
        self.repositorio_cotizacion = repositorio_cotizacion

    def guardar(self, tipo_cotizacion: TipoCotizacion) -> TipoCotizacion:
        """Crea o actualiza un tipo de cotización, evitando nombres duplicados."""

        # Buscar si existe otro registro con el mismo nombre
        existente_nombre = self.repositorio.leer_por_nombre(
            tipo_cotizacion.nombre
        )

        if (
            existente_nombre is not None
            and existente_nombre.id != tipo_cotizacion.id
        ):
            raise ValueError(
                f"Ya existe un tipo de cotización con nombre '{tipo_cotizacion.nombre}'."
            )

        # Crear si no tiene ID o no existe
        if (
            tipo_cotizacion.id is None
            or self.repositorio.leer_por_id(tipo_cotizacion.id) is None
        ):
            return self.repositorio.crear(tipo_cotizacion)

        # Actualizar si existe
        return self.repositorio.actualizar(tipo_cotizacion)

    def leer_por_id(self, id: int) -> Optional[TipoCotizacion]:
        """Devuelve el tipo de cotización con el ID indicado, o None si no existe."""
        return self.repositorio.leer_por_id(id)

    def leer_todos(self) -> List[TipoCotizacion]:
        """Devuelve la lista de tipos de cotización del repositorio."""
        return self.repositorio.leer_todos()

    def eliminar(self, id: int) -> bool:
        """Elimina el tipo de cotización con el ID indicado, si no está en uso."""
        
        # Verificar si hay cotizaciones que usan este tipo de cotización
        if self.repositorio_cotizacion.existe_por_tipo_cotizacion(id):
            raise ValueError(
            f"No se puede eliminar el tipo de cotización con ID {id} "
            "porque está utilizado en cotizaciones."
        )
        return self.repositorio.eliminar(id)

class ServicoMoneda:
    """Gestiona las operaciones CRUD de monedas."""

    def __init__(self, 
                 repositorio: RepositorioMoneda,
                 repositorio_cotizacion: RepositorioCotizacion,
                 repositorio_precio: RepositorioPrecio):
        """Recibe los repositorios de monedas, cotizaciones y precios."""
        self.repositorio = repositorio
        self.repositorio_cotizacion = repositorio_cotizacion
        self.repositorio_precio = repositorio_precio

    def guardar(self, moneda: Moneda) -> Moneda:
        """Crea o actualiza la moneda, evitando códigos ISO duplicados."""
        existente = self.repositorio.leer_por_codigo_iso(moneda.codigo_iso)

        if existente is not None and existente.id != moneda.id:
            raise ValueError(
                f"Ya existe una moneda con código ISO '{moneda.codigo_iso}'."
            )

        if (moneda.id is None or self.repositorio.leer_por_id(moneda.id) is None):
            return self.repositorio.crear(moneda)
        
        return self.repositorio.actualizar(moneda)

    def leer_por_id(self, id: int) -> Optional[Moneda]:
        """Devuelve la moneda con el ID indicado, o None si no existe."""
        return self.repositorio.leer_por_id(id)

    def leer_todos(self) -> List[Moneda]:
        """Devuelve la lista de monedas del repositorio."""
        return self.repositorio.leer_todos()

    def eliminar(self, id: int) -> bool:
        """Elimina la moneda si no está utilizada en cotizaciones ni precios."""
        if self.repositorio_cotizacion.existe_por_moneda(id):
            raise ValueError(
                f"No se puede eliminar la moneda con ID {id} "
                "porque está utilizada en cotizaciones."
            )

        if self.repositorio_precio.existe_por_moneda(id):
            raise ValueError(
                f"No se puede eliminar la moneda con ID {id} "
                "porque está utilizada en precio del libro"
            )

        return self.repositorio.eliminar(id)
