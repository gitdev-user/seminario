"""Define la interfaz de repositorios y sus implementaciones en memoria."""

import abc
from datetime import date
from typing import Generic, List, Optional, TypeVar

from entities.entities import (
    TipoCotizacion,
    Moneda,
    Genero,
    Editorial,
    Precio,
    Stock,
    Cotizacion,
    Libro,
)

T = TypeVar("T")

class IRepositorio(abc.ABC, Generic[T]):
  """Interfaz para repositorios que manejan entidades con operaciones CRUD básicas."""

  @abc.abstractmethod
  def crear(self, entidad: T) -> T:
    """Crea una nueva entidad en el repositorio.

    Args:
        entidad (T): La entidad a crear.

    Returns:
        T: La entidad creada.

    Raises:
        ValueError: Si ya existe una entidad con el mismo ID.
    """
    pass

  @abc.abstractmethod
  def leer_por_id(self, id: int) -> Optional[T]:
    """Lee una entidad del repositorio por su ID.

    Args:
        id (int): El ID de la entidad a leer.

    Returns:
        Optional[T]: La entidad si se encuentra, None en caso contrario.
    """
    pass

  @abc.abstractmethod
  def leer_todos(self) -> List[T]:
    """Lee todas las entidades del repositorio.

    Returns:
        List[T]: Una lista de todas las entidades.
    """
    pass

  @abc.abstractmethod
  def actualizar(self, entidad: T) -> T:
    """Actualiza una entidad existente en el repositorio.

    Args:
        entidad (T): La entidad a actualizar (debe tener un ID existente).

    Returns:
        T: La entidad actualizada.

    Raises:
        ValueError: Si no se encuentra la entidad para actualizar.
    """
    pass

  @abc.abstractmethod
  def eliminar(self, id: int) -> bool:
    """Elimina una entidad del repositorio por su ID.

    Args:
        id (int): El ID de la entidad a eliminar.

    Returns:
        bool: True si la entidad fue eliminada, False si no se encontró.
    """
    pass

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

  @abc.abstractmethod
  def existe_por_moneda(self, moneda_id: int) -> bool:
    """Indica si algún precio utiliza la moneda indicada."""
    pass


class IRepositorioStock(abc.ABC):
  """Interfaz para repositorios del tipo Stock."""

  @abc.abstractmethod
  def crear(self, stock: Stock) -> Stock:
    """Crea un nuevo registro de stock.

    Args:
        stock (Stock): El objeto Stock a crear.

    Returns:
        Stock: El objeto Stock creado.

    Raises:
        ValueError: Si ya existe un registro de stock para el mismo libro.
    """
    pass

  @abc.abstractmethod
  def leer_por_libro(self, libro_id: int) -> Optional['Stock']:
    """Lee un registro de stock por ID de libro.

    Args:
        libro_id (int): El ID del libro asociado al stock.

    Returns:
        Optional[Stock]: El objeto Stock si se encuentra, None en caso contrario.
    """
    pass

  @abc.abstractmethod
  def actualizar(self, stock: 'Stock') -> 'Stock':
    """Actualiza un registro de stock existente.

    Args:
        stock (Stock): El objeto Stock a actualizar (debe tener un libro_id existente).

    Returns:
        Stock: El objeto Stock actualizado.

    Raises:
        ValueError: Si no se encuentra el stock para actualizar.
    """
    pass

  @abc.abstractmethod
  def eliminar(self, libro_id: int) -> bool:
    """Elimina un registro de stock por ID de libro.

    Args:
        libro_id (int): El ID del libro asociado al stock a eliminar.

    Returns:
        bool: True si el stock fue eliminado, False si no se encontró.
    """
    pass

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

  @abc.abstractmethod
  def existe_por_tipo_cotizacion(self, tipo_id: int) -> bool:
    """Indica si alguna cotización utiliza el tipo identificado por tipo_id."""
    pass

  @abc.abstractmethod
  def existe_por_moneda(self, moneda_id: int) -> bool:
    """Indica si la moneda se utiliza como origen o destino en cotizaciones."""
    pass
  

class MemoriaRepositorio(IRepositorio[T]):
    """Almacena entidades en memoria y permite realizar operaciones CRUD.

    Las entidades deben tener un atributo ``id``. Los datos se conservan
    únicamente durante la vida de la instancia del repositorio.
    """

    def __init__(self, clase_entidad: type[T]):
        """Inicializa un repositorio vacío para el tipo de entidad indicado.

        Args:
            clase_entidad (type[T]): Clase de las entidades aceptadas al crear.
        """
        self.clase_modelo = clase_entidad
        self._datos: dict[int, T] = {}
        self._ultimo_id: int = 0

    def crear(self, entidad: T) -> T:
        """Guarda una entidad y asigna un ID si el actual es None o cero.

        Args:
            entidad (T): Entidad a guardar, con un atributo ``id``.

        Returns:
            T: La entidad guardada, con su ID asignado.

        Raises:
            TypeError: Si la entidad no es del tipo configurado.
            ValueError: Si ya existe una entidad con el mismo ID.
        """
        if not isinstance(entidad, self.clase_modelo):
            raise TypeError(
                f"La entidad debe ser de tipo {self.clase_modelo.__name__}."
            )

        if entidad.id is None or entidad.id == 0:
            self._ultimo_id += 1
            entidad.id = self._ultimo_id

        elif entidad.id in self._datos:
            raise ValueError(
                f"Ya existe un registro con ID {entidad.id}."
            )

        else:
            self._ultimo_id = max(self._ultimo_id, entidad.id)

        self._datos[entidad.id] = entidad

        return entidad

    def leer_por_id(self, id: int) -> Optional[T]:
        """Busca una entidad por su ID.

        Args:
            id (int): ID de la entidad buscada.

        Returns:
            Optional[T]: La entidad encontrada, o None si no existe.
        """
        return self._datos.get(id)

    def leer_todos(self) -> List[T]:
        """Obtiene todas las entidades almacenadas.

        Returns:
            List[T]: Una nueva lista con las entidades del repositorio.
        """
        return list(self._datos.values())

    def actualizar(self, entidad: T) -> T:
        """Reemplaza la entidad almacenada con el mismo ID.

        Args:
            entidad (T): Entidad con los datos actualizados y un ID existente.

        Returns:
            T: La entidad actualizada.

        Raises:
            ValueError: Si no existe una entidad con ese ID.
        """
        if entidad.id not in self._datos:
            raise ValueError(
                f"No se encontró el registro con ID {entidad.id} para actualizar."
            )

        self._datos[entidad.id] = entidad

        return entidad

    def eliminar(self, id: int) -> bool:
        """Elimina la entidad identificada por su ID.

        Args:
            id (int): ID de la entidad a eliminar.

        Returns:
            bool: True si se eliminó la entidad, o False si no existía.
        """
        if id not in self._datos:
            return False

        del self._datos[id]

        return True


class MemoriaRepositorioTipoCotizacion(MemoriaRepositorio[TipoCotizacion]):
    """Repositorio en memoria para entidades TipoCotizacion."""

    def __init__(self):
        """Inicializa un repositorio vacío de tipos de cotización."""
        super().__init__(
            clase_entidad=TipoCotizacion
        )

    def leer_por_nombre(self, nombre: str) -> Optional[TipoCotizacion]:
        """Busca un tipo de cotización por nombre, ignorando mayúsculas y espacios externos."""

        nombre = nombre.strip().casefold()

        for tipo in self._datos.values():
            if tipo.nombre.strip().casefold() == nombre:
                return tipo

        return None


class MemoriaRepositorioEditorial(MemoriaRepositorio[Editorial]):
    """Repositorio en memoria para entidades Editorial."""

    def __init__(self):
        """Inicializa un repositorio vacío de editoriales."""
        super().__init__(
            clase_entidad=Editorial
        )

    def leer_por_nombre(self, nombre: str) -> Optional[Editorial]:
        """Busca una editorial por su nombre.

        Args:
            nombre (str): Nombre, sin distinguir mayúsculas y minúsculas
                ni espacios externos.

        Returns:
            Optional[Editorial]: La editorial encontrada, o None si no existe.
        """
        nombre_normalizado = nombre.strip().casefold()

        for editorial in self._datos.values():
            if editorial.nombre.strip().casefold() == nombre_normalizado:
                return editorial

        return None


class MemoriaRepositorioGenero(MemoriaRepositorio[Genero]):
    """Repositorio en memoria para entidades Genero."""

    def __init__(self):
        """Inicializa un repositorio vacío de géneros literarios."""
        super().__init__(
            clase_entidad=Genero
        )

    def leer_por_nombre(self, nombre: str) -> Optional[Genero]:
        """Busca un género por su nombre.

        Args:
            nombre (str): Nombre, sin distinguir mayúsculas y minúsculas
                ni espacios externos.

        Returns:
            Optional[Genero]: El género encontrado, o None si no existe.
        """
        nombre_normalizado = nombre.strip().casefold()

        for genero in self._datos.values():
            if genero.nombre.strip().casefold() == nombre_normalizado:
                return genero

        return None


class MemoriaRepositorioMoneda(MemoriaRepositorio[Moneda]):
    """Repositorio en memoria para entidades Moneda."""

    def __init__(self):
        """Inicializa un repositorio vacío de monedas."""
        super().__init__(
            clase_entidad=Moneda
        )

    def leer_por_codigo_iso(self, codigo_iso: str) -> Optional[Moneda]:
        """Busca una moneda por su código ISO.

        Args:
            codigo_iso (str): Código ISO, sin distinguir mayúsculas y
                minúsculas ni espacios externos.

        Returns:
            Optional[Moneda]: La moneda encontrada, o None si no existe.
        """
        codigo_normalizado = codigo_iso.strip().upper()
        
        for moneda in self._datos.values():
            if moneda.codigo_iso.strip().upper() == codigo_normalizado:
                return moneda
        
        return None


class MemoriaRepositorioLibro(MemoriaRepositorio[Libro]):
    """Repositorio en memoria para entidades Libro."""

    def __init__(self):
        """Inicializa un repositorio vacío de libros."""
        super().__init__(
            clase_entidad=Libro
        )

    def leer_por_isbn(self, isbn: str) -> Optional[Libro]:
        """Busca un libro por su ISBN, ignorando espacios externos.

        Args:
            isbn (str): ISBN del libro buscado.

        Returns:
            Optional[Libro]: El libro encontrado, o None si no existe.
        """
        isbn_normalizado = isbn.strip()

        for libro in self._datos.values():
            if libro.isbn.strip() == isbn_normalizado:
                return libro

        return None


    def existe_por_editorial(self, editorial_id: int) -> bool:
        """Comprueba si algún libro utiliza la editorial indicada.

        Args:
            editorial_id (int): ID de la editorial buscada.

        Returns:
            bool: True si la editorial está utilizada, o False si no lo está.
        """
        for libro in self._datos.values():
            if libro.editorial.id == editorial_id:
                return True

        return False

    def existe_por_genero(self, genero_id: int) -> bool:
        """Comprueba si algún libro utiliza el género indicado.

        Args:
            genero_id (int): ID del género buscado.

        Returns:
            bool: True si el género está utilizado, o False si no lo está.
        """
        for libro in self._datos.values():
            if libro.genero.id == genero_id:
                return True

        return False


class MemoriaRepositorioPrecio(IRepositorioPrecio):
    """Repositorio de precios en memoria identificado por libro_id."""

    def __init__(self):
        """Inicializa un repositorio vacío de precios, indexado por ID de libro."""
        self._datos: dict[int, Precio] = {}

    def crear(self, precio: Precio) -> Precio:
        """Guarda y devuelve el precio recibido para su libro.

        Raises:
            ValueError: Si ya existe un precio para el mismo libro.
        """
        if precio.libro_id in self._datos:
            raise ValueError(
                f"Ya existe un registro de precio para el libro {precio.libro_id}."
            )

        self._datos[precio.libro_id] = precio
        return precio

    def leer_por_libro(self, libro_id: int) -> Optional[Precio]:
        """Devuelve el precio del libro indicado, o None si no está registrado."""
        return self._datos.get(libro_id)

    def actualizar(self, precio: Precio) -> Precio:
        """Actualiza moneda y precio base conservando la instancia almacenada.

        Returns:
            Precio actualizado, con la misma referencia que tenía el repositorio.

        Raises:
            ValueError: Si no existe un precio para el libro indicado.
        """
        if precio.libro_id not in self._datos:
            raise ValueError(
                f"No se encontró un registro de precio para el libro "
                f"{precio.libro_id} para actualizar."
            )

        # Mantener la instancia existente para conservar referencias
        precio_actual = self._datos[precio.libro_id]

        precio_actual.moneda = precio.moneda
        precio_actual.precio_base = precio.precio_base

        return precio_actual

    def eliminar(self, libro_id: int) -> bool:
        """Elimina el precio del libro y devuelve True, o False si no existía."""
        if libro_id not in self._datos:
            return False

        del self._datos[libro_id]
        return True


    def existe_por_moneda(self, moneda_id: int) -> bool:
        """Comprueba si algún precio utiliza la moneda indicada.

        Args:
            moneda_id (int): ID de la moneda buscada.

        Returns:
            bool: True si la moneda está utilizada, o False si no lo está.
        """
        for precio in self._datos.values():
            if precio.moneda.id == moneda_id:
                return True

        return False


class MemoriaRepositorioStock(IRepositorioStock):
    """Repositorio de stock en memoria identificado por libro_id."""

    def __init__(self):
        """Inicializa un repositorio vacío de stock, indexado por ID de libro."""
        self._datos: dict[int, Stock] = {}

    def crear(self, stock: Stock) -> Stock:
        """Guarda y devuelve el stock recibido para su libro.

        Raises:
            ValueError: Si ya existe stock registrado para el mismo libro.
        """
        if stock.libro_id in self._datos:
            raise ValueError(
                f"Ya existe un registro de stock para el libro {stock.libro_id}."
            )

        self._datos[stock.libro_id] = stock
        return stock

    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        """Devuelve el stock del libro indicado, o None si no está registrado."""
        return self._datos.get(libro_id)

    def actualizar(self, stock: Stock) -> Stock:
        """Actualiza las cantidades mínima y total conservando la instancia almacenada.

        Returns:
            Stock actualizado, con la misma referencia que tenía el repositorio.

        Raises:
            ValueError: Si no existe stock registrado para el libro indicado.
        """
        if stock.libro_id not in self._datos:
            raise ValueError(
                f"No se encontró un registro de stock para el libro "
                f"{stock.libro_id} para actualizar."
            )

        # Mantener la instancia existente para conservar referencias
        stock_actual = self._datos[stock.libro_id]
        stock_actual.cantidad_minima = stock.cantidad_minima
        stock_actual.cantidad_total = stock.cantidad_total

        return stock_actual

    def eliminar(self, libro_id: int) -> bool:
        """Elimina el stock del libro y devuelve True, o False si no existía."""
        if libro_id not in self._datos:
            return False

        del self._datos[libro_id]
        return True


class MemoriaRepositorioCotizacion(IRepositorioCotizacion):
    """Repositorio de cotizaciones en memoria utilizando una clave compuesta."""

    def __init__(self):
        """Inicializa las cotizaciones indexadas por tipo, monedas y fecha."""
        self._datos: dict[tuple[int, int, int, date], Cotizacion] = {}

    def _obtener_clave(self, cotizacion: Cotizacion) -> tuple[int, int, int, date]:
        """Devuelve los IDs de tipo, moneda origen y destino, seguidos de la fecha."""
        return (
            cotizacion.tipo_cotizacion.id,
            cotizacion.moneda_origen.id,
            cotizacion.moneda_destino.id,
            cotizacion.fecha
        )

    def crear(self, cotizacion: Cotizacion) -> Cotizacion:
        """Guarda y devuelve la cotización recibida usando su clave compuesta.

        Raises:
            ValueError: Si ya existe una cotización del mismo tipo, monedas y fecha.
        """
        clave = self._obtener_clave(cotizacion)

        if clave in self._datos:
            raise ValueError(
                f"Ya existe una cotización para el tipo {clave[0]}, "
                f"las monedas {clave[1]} y {clave[2]} "
                f"en la fecha {clave[3]}."
            )

        self._datos[clave] = cotizacion
        return cotizacion

    def leer_por_tipo_moneda_origen_destino_y_fecha(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int,
        fecha: date
    ) -> Optional[Cotizacion]:
        """Busca por IDs de tipo y monedas y por fecha; devuelve None si no existe."""

        clave = (
            tipo_id,
            moneda_origen_id,
            moneda_destino_id,
            fecha
        )

        return self._datos.get(clave)

    def leer_historico_por_tipo_moneda_origen_moneda_destino(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int
    ) -> List[Cotizacion]:
        """Devuelve el histórico del tipo y las monedas, ordenado por fecha ascendente.

        Si no hay coincidencias, devuelve una lista vacía.
        """

        cotizaciones = [
            cotizacion
            for clave, cotizacion in self._datos.items()
            if clave[:3] == (
                tipo_id,
                moneda_origen_id,
                moneda_destino_id
            )
        ]

        return sorted(
            cotizaciones,
            key=lambda cotizacion: cotizacion.fecha
        )

    def actualizar(self, cotizacion: Cotizacion) -> Cotizacion:
        """Actualiza el valor de una cotización conservando la instancia almacenada.

        Returns:
            Cotización actualizada, con la misma referencia que tenía el repositorio.

        Raises:
            ValueError: Si no existe la clave compuesta de la cotización recibida.
        """
        clave = self._obtener_clave(cotizacion)

        if clave not in self._datos:
            raise ValueError(
                "No se encontró la cotización para actualizar."
            )

        # Mantener la instancia existente
        cotizacion_actual = self._datos[clave]
        cotizacion_actual.valor = cotizacion.valor

        return cotizacion_actual

    def eliminar(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int,
        fecha: date
    ) -> bool:
        """Elimina por tipo, monedas y fecha; devuelve True, o False si no existía."""

        clave = (
            tipo_id,
            moneda_origen_id,
            moneda_destino_id,
            fecha
        )

        if clave not in self._datos:
            return False

        del self._datos[clave]
        return True

    def existe_por_tipo_cotizacion(self, tipo_id: int) -> bool:
        """Devuelve True si alguna cotización utiliza el tipo indicado, o False si no."""

        for cotizacion in self._datos.values():
            if cotizacion.tipo_cotizacion.id == tipo_id:
                return True
        return False

    def existe_por_moneda(self, moneda_id: int) -> bool:
        """Comprueba si alguna cotización utiliza la moneda indicada.

        Args:
            moneda_id (int): ID de la moneda de origen o destino.

        Returns:
            bool: True si la moneda está utilizada, o False si no lo está.
        """
        for cotizacion in self._datos.values():
            if (
                cotizacion.moneda_origen.id == moneda_id
                or cotizacion.moneda_destino.id == moneda_id
            ):
                return True

        return False
