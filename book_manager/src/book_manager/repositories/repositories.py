"""Repositorios que persisten entidades mediante SQLAlchemy."""

from decimal import Decimal
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database.connection import ContextManager
from entities.entities import Cotizacion, Editorial, Genero, Libro, Moneda, Precio, Stock, TipoCotizacion
from models.models import (
    EditorialModel, GeneroModel, LibroModel, MonedaModel,
    PrecioModel, StockModel, TipoCotizacionModel, CotizacionModel,
)

class RepositorioEditorial():
    """Persiste editoriales y administra las sesiones con ContextManager."""

    def __init__(self, contexto: ContextManager):
        """Recibe el administrador de transacciones de la base de datos."""
        self.contexto = contexto

    @staticmethod
    def _a_entidad(modelo: EditorialModel) -> Editorial:
        """Convierte un registro SQLAlchemy en una entidad Editorial."""
        editorial = Editorial(
            nombre=modelo.nombre,
            grupo=modelo.grupo,
            pais_origen=modelo.pais_origen,
            telefono=modelo.telefono,
            email=modelo.email,
        )
        editorial.id = modelo.id
        return editorial

    def crear(self, entidad: Editorial) -> Editorial:
        """Guarda una editorial y asigna su ID después de confirmar los cambios.

        Raises:
            TypeError: Si la entidad no es una Editorial.
            ValueError: Si ya existe una editorial con el ID indicado.
        """
        if not isinstance(entidad, Editorial):
            raise TypeError("La entidad debe ser de tipo Editorial.")

        with self.contexto.transaction() as session:
            if entidad.id is not None and session.get(EditorialModel, entidad.id):
                raise ValueError(f"Ya existe un registro con ID {entidad.id}.")

            modelo = EditorialModel(
                nombre=entidad.nombre,
                grupo=entidad.grupo,
                pais_origen=entidad.pais_origen,
                telefono=entidad.telefono,
                email=entidad.email,
            )
            if entidad.id is not None:
                modelo.id = entidad.id

            session.add(modelo)
            session.flush()
            nuevo_id = modelo.id

        entidad.id = nuevo_id
        return entidad

    def leer_por_id(self, id: int) -> Editorial | None:
        """Obtiene una editorial por ID o devuelve None si no existe."""
        with self.contexto.transaction() as session:
            modelo = session.get(EditorialModel, id)
            return self._a_entidad(modelo) if modelo is not None else None

    def leer_todos(self) -> list[Editorial]:
        """Obtiene las editoriales ordenadas por ID como entidades de dominio."""
        with self.contexto.transaction() as session:
            modelos = session.scalars(select(EditorialModel).order_by(EditorialModel.id))
            return [self._a_entidad(modelo) for modelo in modelos]

    def leer_por_nombre(self, nombre: str) -> Editorial | None:
        """Busca por nombre ignorando mayúsculas y espacios externos.

        Conserva la normalización con casefold del repositorio en memoria.
        """
        nombre_normalizado = nombre.strip().casefold()
        with self.contexto.transaction() as session:
            modelos = session.scalars(select(EditorialModel).order_by(EditorialModel.id))
            for modelo in modelos:
                if modelo.nombre.strip().casefold() == nombre_normalizado:
                    return self._a_entidad(modelo)
            return None

    def actualizar(self, entidad: Editorial) -> Editorial:
        """Actualiza una editorial existente y devuelve la entidad recibida.

        Raises:
            ValueError: Si no existe una editorial con el ID indicado.
        """
        with self.contexto.transaction() as session:
            modelo = session.get(EditorialModel, entidad.id) if entidad.id is not None else None
            if modelo is None:
                raise ValueError(
                    f"No se encontró el registro con ID {entidad.id} para actualizar."
                )

            modelo.nombre = entidad.nombre
            modelo.grupo = entidad.grupo
            modelo.pais_origen = entidad.pais_origen
            modelo.telefono = entidad.telefono
            modelo.email = entidad.email

        return entidad

    def eliminar(self, id: int) -> bool:
        """Elimina una editorial; devuelve False si el ID no existe."""
        with self.contexto.transaction() as session:
            modelo = session.get(EditorialModel, id)
            if modelo is None:
                return False

            session.delete(modelo)
            return True


class RepositorioGenero:
    """Persiste géneros y administra las sesiones con ContextManager."""

    def __init__(self, contexto: ContextManager):
        """Recibe el administrador de transacciones de la base de datos."""
        self.contexto = contexto

    @staticmethod
    def _a_entidad(modelo: GeneroModel) -> Genero:
        """Convierte un registro SQLAlchemy en una entidad Genero."""
        genero = Genero(nombre=modelo.nombre, descripcion=modelo.descripcion)
        genero.id = modelo.id
        return genero

    def crear(self, entidad: Genero) -> Genero:
        """Guarda un género y asigna su ID después de confirmar los cambios.

        Raises:
            TypeError: Si la entidad no es un Genero.
            ValueError: Si ya existe un género con el ID indicado.
        """
        if not isinstance(entidad, Genero):
            raise TypeError("La entidad debe ser de tipo Genero.")

        with self.contexto.transaction() as session:
            if entidad.id is not None and session.get(GeneroModel, entidad.id):
                raise ValueError(f"Ya existe un registro con ID {entidad.id}.")

            modelo = GeneroModel(nombre=entidad.nombre, descripcion=entidad.descripcion)
            if entidad.id is not None:
                modelo.id = entidad.id

            session.add(modelo)
            session.flush()
            nuevo_id = modelo.id

        entidad.id = nuevo_id
        return entidad

    def leer_por_id(self, id: int) -> Genero | None:
        """Obtiene un género por ID o devuelve None si no existe."""
        with self.contexto.transaction() as session:
            modelo = session.get(GeneroModel, id)
            return self._a_entidad(modelo) if modelo is not None else None

    def leer_todos(self) -> list[Genero]:
        """Obtiene los géneros ordenados por ID como entidades de dominio."""
        with self.contexto.transaction() as session:
            modelos = session.scalars(select(GeneroModel).order_by(GeneroModel.id))
            return [self._a_entidad(modelo) for modelo in modelos]

    def leer_por_nombre(self, nombre: str) -> Genero | None:
        """Busca por nombre ignorando mayúsculas y espacios externos.

        Conserva la normalización con casefold del repositorio en memoria.
        """
        nombre_normalizado = nombre.strip().casefold()
        with self.contexto.transaction() as session:
            modelos = session.scalars(select(GeneroModel).order_by(GeneroModel.id))
            for modelo in modelos:
                if modelo.nombre.strip().casefold() == nombre_normalizado:
                    return self._a_entidad(modelo)
            return None

    def actualizar(self, entidad: Genero) -> Genero:
        """Actualiza un género existente y devuelve la entidad recibida.

        Raises:
            ValueError: Si no existe un género con el ID indicado.
        """
        with self.contexto.transaction() as session:
            modelo = session.get(GeneroModel, entidad.id) if entidad.id is not None else None
            if modelo is None:
                raise ValueError(
                    f"No se encontró el registro con ID {entidad.id} para actualizar."
                )

            modelo.nombre = entidad.nombre
            modelo.descripcion = entidad.descripcion

        return entidad

    def eliminar(self, id: int) -> bool:
        """Elimina un género; devuelve False si el ID no existe."""
        with self.contexto.transaction() as session:
            modelo = session.get(GeneroModel, id)
            if modelo is None:
                return False

            session.delete(modelo)
            return True


class RepositorioMoneda:
    """Persiste monedas y administra las sesiones con ContextManager."""

    def __init__(self, contexto: ContextManager):
        """Recibe el administrador de transacciones de la base de datos."""
        self.contexto = contexto

    @staticmethod
    def _a_entidad(modelo: MonedaModel) -> Moneda:
        """Convierte un registro SQLAlchemy en una entidad Moneda."""
        moneda = Moneda(
            codigo_iso=modelo.codigo_iso,
            nombre=modelo.nombre,
            simbolo=modelo.simbolo,
        )
        moneda.id = modelo.id
        return moneda

    def crear(self, entidad: Moneda) -> Moneda:
        """Guarda una moneda y asigna su ID después de confirmar los cambios.

        Raises:
            TypeError: Si la entidad no es una Moneda.
            ValueError: Si ya existe una moneda con el ID indicado.
        """
        if not isinstance(entidad, Moneda):
            raise TypeError("La entidad debe ser de tipo Moneda.")

        with self.contexto.transaction() as session:
            if entidad.id is not None and session.get(MonedaModel, entidad.id):
                raise ValueError(f"Ya existe un registro con ID {entidad.id}.")

            modelo = MonedaModel(
                codigo_iso=entidad.codigo_iso,
                nombre=entidad.nombre,
                simbolo=entidad.simbolo,
            )
            if entidad.id is not None:
                modelo.id = entidad.id

            session.add(modelo)
            session.flush()
            nuevo_id = modelo.id

        entidad.id = nuevo_id
        return entidad

    def leer_por_id(self, id: int) -> Moneda | None:
        """Obtiene una moneda por ID o devuelve None si no existe."""
        with self.contexto.transaction() as session:
            modelo = session.get(MonedaModel, id)
            return self._a_entidad(modelo) if modelo is not None else None

    def leer_todos(self) -> list[Moneda]:
        """Obtiene las monedas ordenadas por ID como entidades de dominio."""
        with self.contexto.transaction() as session:
            modelos = session.scalars(select(MonedaModel).order_by(MonedaModel.id))
            return [self._a_entidad(modelo) for modelo in modelos]

    def leer_por_codigo_iso(self, codigo_iso: str) -> Moneda | None:
        """Busca por código ISO ignorando mayúsculas y espacios externos."""
        codigo_normalizado = codigo_iso.strip().upper()
        with self.contexto.transaction() as session:
            modelos = session.scalars(select(MonedaModel).order_by(MonedaModel.id))
            for modelo in modelos:
                if modelo.codigo_iso.strip().upper() == codigo_normalizado:
                    return self._a_entidad(modelo)
            return None

    def actualizar(self, entidad: Moneda) -> Moneda:
        """Actualiza una moneda existente y devuelve la entidad recibida.

        Raises:
            ValueError: Si no existe una moneda con el ID indicado.
        """
        with self.contexto.transaction() as session:
            modelo = session.get(MonedaModel, entidad.id) if entidad.id is not None else None
            if modelo is None:
                raise ValueError(
                    f"No se encontró el registro con ID {entidad.id} para actualizar."
                )

            modelo.codigo_iso = entidad.codigo_iso
            modelo.nombre = entidad.nombre
            modelo.simbolo = entidad.simbolo

        return entidad

    def eliminar(self, id: int) -> bool:
        """Elimina una moneda; devuelve False si el ID no existe."""
        with self.contexto.transaction() as session:
            modelo = session.get(MonedaModel, id)
            if modelo is None:
                return False

            session.delete(modelo)
            return True


class RepositorioTipoCotizacion:
    """Persiste tipos de cotización y administra sesiones con ContextManager."""

    def __init__(self, contexto: ContextManager):
        """Recibe el administrador de transacciones de la base de datos."""
        self.contexto = contexto

    @staticmethod
    def _a_entidad(modelo: TipoCotizacionModel) -> TipoCotizacion:
        """Convierte un registro SQLAlchemy en una entidad TipoCotizacion."""
        tipo = TipoCotizacion(nombre=modelo.nombre, descripcion=modelo.descripcion)
        tipo.id = modelo.id
        return tipo

    def crear(self, entidad: TipoCotizacion) -> TipoCotizacion:
        """Guarda un tipo de cotización y asigna su ID después del commit.

        Raises:
            TypeError: Si la entidad no es un TipoCotizacion.
            ValueError: Si ya existe un registro con el ID indicado.
        """
        if not isinstance(entidad, TipoCotizacion):
            raise TypeError("La entidad debe ser de tipo TipoCotizacion.")

        with self.contexto.transaction() as session:
            if entidad.id is not None and session.get(TipoCotizacionModel, entidad.id):
                raise ValueError(f"Ya existe un registro con ID {entidad.id}.")

            modelo = TipoCotizacionModel(
                nombre=entidad.nombre,
                descripcion=entidad.descripcion,
            )
            if entidad.id is not None:
                modelo.id = entidad.id

            session.add(modelo)
            session.flush()
            nuevo_id = modelo.id

        entidad.id = nuevo_id
        return entidad

    def leer_por_id(self, id: int) -> TipoCotizacion | None:
        """Obtiene un tipo de cotización por ID o None si no existe."""
        with self.contexto.transaction() as session:
            modelo = session.get(TipoCotizacionModel, id)
            return self._a_entidad(modelo) if modelo is not None else None

    def leer_todos(self) -> list[TipoCotizacion]:
        """Obtiene los tipos de cotización ordenados por ID."""
        with self.contexto.transaction() as session:
            modelos = session.scalars(
                select(TipoCotizacionModel).order_by(TipoCotizacionModel.id)
            )
            return [self._a_entidad(modelo) for modelo in modelos]

    def leer_por_nombre(self, nombre: str) -> TipoCotizacion | None:
        """Busca por nombre ignorando mayúsculas y espacios externos.

        Conserva la normalización con casefold del repositorio en memoria.
        """
        nombre_normalizado = nombre.strip().casefold()
        with self.contexto.transaction() as session:
            modelos = session.scalars(
                select(TipoCotizacionModel).order_by(TipoCotizacionModel.id)
            )
            for modelo in modelos:
                if modelo.nombre.strip().casefold() == nombre_normalizado:
                    return self._a_entidad(modelo)
            return None

    def actualizar(self, entidad: TipoCotizacion) -> TipoCotizacion:
        """Actualiza un tipo de cotización y devuelve la entidad recibida.

        Raises:
            ValueError: Si no existe un registro con el ID indicado.
        """
        with self.contexto.transaction() as session:
            modelo = (
                session.get(TipoCotizacionModel, entidad.id)
                if entidad.id is not None else None
            )
            if modelo is None:
                raise ValueError(
                    f"No se encontró el registro con ID {entidad.id} para actualizar."
                )

            modelo.nombre = entidad.nombre
            modelo.descripcion = entidad.descripcion

        return entidad

    def eliminar(self, id: int) -> bool:
        """Elimina un tipo de cotización; devuelve False si el ID no existe."""
        with self.contexto.transaction() as session:
            modelo = session.get(TipoCotizacionModel, id)
            if modelo is None:
                return False

            session.delete(modelo)
            return True


class RepositorioLibro:
    """Persiste libros con sus relaciones usando ContextManager."""

    def __init__(self, contexto: ContextManager):
        """Recibe el administrador de transacciones de la base de datos."""
        self.contexto = contexto

    @staticmethod
    def _a_entidad(modelo: LibroModel) -> Libro:
        """Convierte el libro y sus relaciones mientras la sesión está abierta."""
        precio = (
            RepositorioPrecio._a_entidad(modelo.precio)
            if modelo.precio is not None else None
        )
        stock = (
            RepositorioStock._a_entidad(modelo.stock)
            if modelo.stock is not None else None
        )

        libro = Libro(
            isbn=modelo.isbn,
            titulo=modelo.titulo,
            autor=modelo.autor,
            peso=modelo.peso,
            dimensiones=modelo.dimensiones,
            numero_paginas=modelo.numero_paginas,
            fecha_publicacion=modelo.fecha_publicacion,
            idioma=modelo.idioma,
            editorial=RepositorioEditorial._a_entidad(modelo.editorial),
            genero=RepositorioGenero._a_entidad(modelo.genero),
            precio=precio,
            stock=stock,
        )
        libro.id = modelo.id
        return libro

    @staticmethod
    def _copiar_datos(modelo: LibroModel, entidad: Libro) -> None:
        """Copia los campos y persiste solo precios y stock completos.

        Si la entidad no incluye precio o stock, elimina esa relación
        mediante la cascada delete-orphan definida en LibroModel.
        """
        if entidad.editorial.id is None or entidad.genero.id is None:
            raise ValueError("La editorial y el género deben estar guardados previamente.")
        if entidad.precio is not None and entidad.precio.moneda.id is None:
            raise ValueError("La moneda del precio debe estar guardada previamente.")

        modelo.isbn = entidad.isbn
        modelo.titulo = entidad.titulo
        modelo.autor = entidad.autor
        modelo.peso = entidad.peso
        modelo.dimensiones = entidad.dimensiones
        modelo.numero_paginas = entidad.numero_paginas
        modelo.fecha_publicacion = entidad.fecha_publicacion
        modelo.idioma = entidad.idioma
        modelo.editorial_id = entidad.editorial.id
        modelo.genero_id = entidad.genero.id

        if entidad.precio is None:
            modelo.precio = None
        else:
            if modelo.precio is None:
                modelo.precio = PrecioModel()
            RepositorioPrecio._copiar_datos(modelo.precio, entidad.precio)

        if entidad.stock is None:
            modelo.stock = None
        else:
            if modelo.stock is None:
                modelo.stock = StockModel()
            modelo.stock.cantidad_minima = entidad.stock.cantidad_minima
            modelo.stock.cantidad_total = entidad.stock.cantidad_total

    def crear(self, entidad: Libro) -> Libro:
        """Guarda el libro y, si se proporcionan, su precio y stock completos.

        Raises:
            TypeError: Si la entidad no es un Libro.
            ValueError: Si el ID ya existe o faltan IDs de sus relaciones.
        """
        if not isinstance(entidad, Libro):
            raise TypeError("La entidad debe ser de tipo Libro.")

        with self.contexto.transaction() as session:
            entidad_id = getattr(entidad, "id", None)
            if entidad_id is not None and session.get(LibroModel, entidad_id):
                raise ValueError(f"Ya existe un registro con ID {entidad_id}.")

            modelo = LibroModel()
            if entidad_id is not None:
                modelo.id = entidad_id
            self._copiar_datos(modelo, entidad)
            session.add(modelo)
            session.flush()
            nuevo_id = modelo.id

        entidad.id = nuevo_id
        if entidad.precio is not None:
            entidad.precio.libro_id = nuevo_id
        if entidad.stock is not None:
            entidad.stock.libro_id = nuevo_id
        return entidad

    def leer_por_id(self, id: int) -> Libro | None:
        """Obtiene un libro por ID o None si no existe."""
        with self.contexto.transaction() as session:
            modelo = session.get(LibroModel, id)
            return self._a_entidad(modelo) if modelo is not None else None

    def leer_todos(self) -> list[Libro]:
        """Obtiene los libros y sus relaciones ordenados por ID."""
        with self.contexto.transaction() as session:
            modelos = session.scalars(select(LibroModel).order_by(LibroModel.id))
            return [self._a_entidad(modelo) for modelo in modelos]

    def leer_por_isbn(self, isbn: str) -> Libro | None:
        """Busca un libro por ISBN ignorando espacios externos."""
        with self.contexto.transaction() as session:
            consulta = select(LibroModel).where(func.trim(LibroModel.isbn) == isbn.strip())
            modelo = session.scalars(consulta).first()
            return self._a_entidad(modelo) if modelo is not None else None

    def existe_por_editorial(self, editorial_id: int) -> bool:
        """Comprueba si algún libro utiliza la editorial indicada."""
        with self.contexto.transaction() as session:
            consulta = select(LibroModel.id).where(LibroModel.editorial_id == editorial_id).limit(1)
            return session.scalar(consulta) is not None

    def existe_por_genero(self, genero_id: int) -> bool:
        """Comprueba si algún libro utiliza el género indicado."""
        with self.contexto.transaction() as session:
            consulta = select(LibroModel.id).where(LibroModel.genero_id == genero_id).limit(1)
            return session.scalar(consulta) is not None

    def actualizar(self, entidad: Libro) -> Libro:
        """Actualiza el libro, precio y stock; falla si el ID no existe."""
        with self.contexto.transaction() as session:
            entidad_id = getattr(entidad, "id", None)
            modelo = session.get(LibroModel, entidad_id) if entidad_id is not None else None
            if modelo is None:
                raise ValueError(
                    f"No se encontró el registro con ID {entidad_id} para actualizar."
                )
            self._copiar_datos(modelo, entidad)

        if entidad.precio is not None:
            entidad.precio.libro_id = entidad_id
        if entidad.stock is not None:
            entidad.stock.libro_id = entidad_id
        return entidad

    def eliminar(self, id: int) -> bool:
        """Elimina el libro, precio y stock; devuelve False si no existe."""
        with self.contexto.transaction() as session:
            modelo = session.get(LibroModel, id)
            if modelo is None:
                return False
            session.delete(modelo)
            return True


class RepositorioPrecio:
    """Persiste precios identificados por libro_id usando ContextManager."""

    def __init__(self, contexto: ContextManager):
        """Recibe el administrador de transacciones de la base de datos."""
        self.contexto = contexto

    @staticmethod
    def _a_entidad(modelo: PrecioModel) -> Precio:
        """Convierte un registro de precio con sus campos obligatorios."""
        return Precio(
            libro_id=modelo.libro_id,
            moneda=RepositorioMoneda._a_entidad(modelo.moneda),
            precio_base=Decimal(str(modelo.precio_base)),
        )

    @staticmethod
    def _copiar_datos(modelo: PrecioModel, precio: Precio) -> None:
        """Copia la moneda y el importe del precio al registro SQLAlchemy."""
        if precio.moneda.id is None:
            raise ValueError("La moneda del precio debe estar guardada previamente.")
        modelo.moneda_id = precio.moneda.id
        modelo.precio_base = float(precio.precio_base)

    def crear(self, precio: Precio) -> Precio:
        """Guarda un precio para un libro existente.

        Raises:
            ValueError: Si ya existe un registro de precio para el libro o
                la moneda no tiene ID.
        """
        with self.contexto.transaction() as session:
            if session.get(PrecioModel, precio.libro_id) is not None:
                raise ValueError(
                    f"Ya existe un registro de precio para el libro {precio.libro_id}."
                )

            modelo = PrecioModel(libro_id=precio.libro_id)
            self._copiar_datos(modelo, precio)
            session.add(modelo)

        return precio

    def leer_por_libro(self, libro_id: int) -> Precio | None:
        """Obtiene el precio del libro o None si no existe un registro."""
        with self.contexto.transaction() as session:
            modelo = session.get(PrecioModel, libro_id)
            return self._a_entidad(modelo) if modelo is not None else None

    def actualizar(self, precio: Precio) -> Precio:
        """Actualiza la moneda y el importe de un precio existente.

        Raises:
            ValueError: Si no existe un registro para el libro indicado o
                la moneda no tiene ID.
        """
        with self.contexto.transaction() as session:
            modelo = session.get(PrecioModel, precio.libro_id)
            if modelo is None:
                raise ValueError(
                    f"No se encontró un registro de precio para el libro "
                    f"{precio.libro_id} para actualizar."
                )
            self._copiar_datos(modelo, precio)

        return precio

    def eliminar(self, libro_id: int) -> bool:
        """Elimina el precio del libro; devuelve False si no existe."""
        with self.contexto.transaction() as session:
            modelo = session.get(PrecioModel, libro_id)
            if modelo is None:
                return False
            session.delete(modelo)
            return True

    def existe_por_moneda(self, moneda_id: int) -> bool:
        """Comprueba si algún precio utiliza la moneda indicada."""
        with self.contexto.transaction() as session:
            consulta = (
                select(PrecioModel.libro_id)
                .where(PrecioModel.moneda_id == moneda_id)
                .limit(1)
            )
            return session.scalar(consulta) is not None


class RepositorioStock:
    """Persiste stock identificado por libro_id usando ContextManager."""

    def __init__(self, contexto: ContextManager):
        """Recibe el administrador de transacciones de la base de datos."""
        self.contexto = contexto

    @staticmethod
    def _a_entidad(modelo: StockModel) -> Stock:
        """Convierte un registro de stock con sus cantidades obligatorias."""
        return Stock(
            libro_id=modelo.libro_id,
            cantidad_minima=modelo.cantidad_minima,
            cantidad_total=modelo.cantidad_total,
        )

    def crear(self, stock: Stock) -> Stock:
        """Guarda el stock para un libro existente.

        Raises:
            ValueError: Si ya existe un registro de stock para el libro.
        """
        with self.contexto.transaction() as session:
            if session.get(StockModel, stock.libro_id) is not None:
                raise ValueError(
                    f"Ya existe un registro de stock para el libro {stock.libro_id}."
                )

            modelo = StockModel(
                libro_id=stock.libro_id,
                cantidad_minima=stock.cantidad_minima,
                cantidad_total=stock.cantidad_total,
            )
            session.add(modelo)

        return stock

    def leer_por_libro(self, libro_id: int) -> Stock | None:
        """Obtiene el stock del libro o None si no existe un registro."""
        with self.contexto.transaction() as session:
            modelo = session.get(StockModel, libro_id)
            return self._a_entidad(modelo) if modelo is not None else None

    def actualizar(self, stock: Stock) -> Stock:
        """Actualiza las cantidades de un registro de stock existente.

        Raises:
            ValueError: Si no existe un registro de stock para el libro.
        """
        with self.contexto.transaction() as session:
            modelo = session.get(StockModel, stock.libro_id)
            if modelo is None:
                raise ValueError(
                    f"No se encontró un registro de stock para el libro "
                    f"{stock.libro_id} para actualizar."
                )

            modelo.cantidad_minima = stock.cantidad_minima
            modelo.cantidad_total = stock.cantidad_total

        return stock

    def eliminar(self, libro_id: int) -> bool:
        """Elimina el stock del libro; devuelve False si no existe."""
        with self.contexto.transaction() as session:
            modelo = session.get(StockModel, libro_id)
            if modelo is None:
                return False
            session.delete(modelo)
            return True


class RepositorioCotizacion:
    """Persiste cotizaciones con ID propio y combinación única de tipo, monedas y fecha."""

    def __init__(self, contexto: ContextManager):
        """Recibe el administrador de transacciones de la base de datos."""
        self.contexto = contexto

    @staticmethod
    def _obtener_clave(cotizacion: Cotizacion) -> tuple[int, int, int, date]:
        """Obtiene los IDs del tipo y las monedas, seguidos de la fecha."""
        clave = (
            cotizacion.tipo_cotizacion.id,
            cotizacion.moneda_origen.id,
            cotizacion.moneda_destino.id,
            cotizacion.fecha,
        )
        if any(id_relacion is None for id_relacion in clave[:3]):
            raise ValueError("El tipo de cotización y las monedas deben estar guardados previamente.")
        return clave

    @staticmethod
    def _buscar_modelo(
        session: Session, clave: tuple[int, int, int, date],
    ) -> CotizacionModel | None:
        """Busca por la combinación única de tipo, monedas y fecha."""
        consulta = select(CotizacionModel).where(
            CotizacionModel.tipo_cotizacion_id == clave[0],
            CotizacionModel.moneda_origen_id == clave[1],
            CotizacionModel.moneda_destino_id == clave[2],
            CotizacionModel.fecha == clave[3],
        )
        return session.scalars(consulta).one_or_none()

    @staticmethod
    def _a_entidad(modelo: CotizacionModel) -> Cotizacion:
        """Convierte la cotización y sus relaciones en entidades de dominio."""
        cotizacion = Cotizacion(
            moneda_origen=RepositorioMoneda._a_entidad(modelo.moneda_origen),
            moneda_destino=RepositorioMoneda._a_entidad(modelo.moneda_destino),
            tipo_cotizacion=RepositorioTipoCotizacion._a_entidad(modelo.tipo_cotizacion),
            valor=Decimal(str(modelo.valor)),
            fecha=modelo.fecha,
        )
        cotizacion.id = modelo.id
        return cotizacion

    def crear(self, cotizacion: Cotizacion) -> Cotizacion:
        """Guarda una cotización y asigna su ID después de confirmar los cambios."""
        clave = self._obtener_clave(cotizacion)
        with self.contexto.transaction() as session:
            if self._buscar_modelo(session, clave) is not None:
                raise ValueError(
                    f"Ya existe una cotización para el tipo {clave[0]}, "
                    f"las monedas {clave[1]} y {clave[2]} "
                    f"en la fecha {clave[3]}."
                )
            modelo = CotizacionModel(
                tipo_cotizacion_id=clave[0],
                moneda_origen_id=clave[1],
                moneda_destino_id=clave[2],
                fecha=clave[3],
                valor=float(cotizacion.valor),
            )
            session.add(modelo)
            session.flush()
            nuevo_id = modelo.id
        cotizacion.id = nuevo_id
        return cotizacion

    def leer_por_tipo_moneda_origen_destino_y_fecha(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int,
        fecha: date,
    ) -> Cotizacion | None:
        """Obtiene una cotización por su clave o None si no existe."""
        clave = (tipo_id, moneda_origen_id, moneda_destino_id, fecha)
        with self.contexto.transaction() as session:
            modelo = self._buscar_modelo(session, clave)
            return self._a_entidad(modelo) if modelo is not None else None

    def leer_historico_por_tipo_moneda_origen_moneda_destino(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int,
    ) -> list[Cotizacion]:
        """Obtiene el histórico por tipo y monedas, ordenado por fecha ascendente."""
        with self.contexto.transaction() as session:
            consulta = (
                select(CotizacionModel)
                .where(
                    CotizacionModel.tipo_cotizacion_id == tipo_id,
                    CotizacionModel.moneda_origen_id == moneda_origen_id,
                    CotizacionModel.moneda_destino_id == moneda_destino_id,
                )
                .order_by(CotizacionModel.fecha)
            )
            return [self._a_entidad(modelo) for modelo in session.scalars(consulta)]

    def actualizar(self, cotizacion: Cotizacion) -> Cotizacion:
        """Actualiza el valor; falla si no existe la clave compuesta recibida."""
        clave = self._obtener_clave(cotizacion)
        with self.contexto.transaction() as session:
            modelo = self._buscar_modelo(session, clave)
            if modelo is None:
                raise ValueError("No se encontró la cotización para actualizar.")
            modelo.valor = float(cotizacion.valor)
            cotizacion_id = modelo.id
        cotizacion.id = cotizacion_id
        return cotizacion

    def eliminar(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int,
        fecha: date,
    ) -> bool:
        """Elimina por clave compuesta; devuelve False si no existe."""
        clave = (tipo_id, moneda_origen_id, moneda_destino_id, fecha)
        with self.contexto.transaction() as session:
            modelo = self._buscar_modelo(session, clave)
            if modelo is None:
                return False
            session.delete(modelo)
            return True

    def existe_por_tipo_cotizacion(self, tipo_id: int) -> bool:
        """Comprueba si alguna cotización utiliza el tipo indicado."""
        with self.contexto.transaction() as session:
            consulta = (
                select(CotizacionModel.tipo_cotizacion_id)
                .where(CotizacionModel.tipo_cotizacion_id == tipo_id)
                .limit(1)
            )
            return session.scalar(consulta) is not None

    def existe_por_moneda(self, moneda_id: int) -> bool:
        """Comprueba si la moneda se utiliza como origen o destino."""
        with self.contexto.transaction() as session:
            consulta = (
                select(CotizacionModel.tipo_cotizacion_id)
                .where(
                    (CotizacionModel.moneda_origen_id == moneda_id)
                    | (CotizacionModel.moneda_destino_id == moneda_id)
                )
                .limit(1)
            )
            return session.scalar(consulta) is not None
