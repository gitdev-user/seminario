"""Servicios de negocio que utilizan los repositorios SQLAlchemy de la aplicación."""

import json
import os
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from functools import wraps
from pathlib import Path
from typing import List, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import dotenv_values


from entities.entities import Auditoria, Cotizacion, Editorial, Genero, Libro, Moneda, Precio, Stock, TipoCotizacion
from repositories.repositories import (
    IRepositorioAuditoria,
    RepositorioCotizacion,
    RepositorioEditorial,
    RepositorioGenero,
    RepositorioLibro,
    RepositorioMoneda,
    RepositorioPrecio,
    RepositorioStock,
    RepositorioTipoCotizacion,
)

class ServicioAuditoria:
    """Registra acciones y proporciona el decorador de auditoría."""

    def __init__(self, repositorio: IRepositorioAuditoria):
        self.repositorio = repositorio

    def leer_todos(self) -> list[Auditoria]:
        """Devuelve todas las auditorías registradas."""
        return self.repositorio.leer_todos()

    @staticmethod
    def auditar(metodo):
        """Registra el resultado de un método síncrono mediante el repositorio."""
        @wraps(metodo)
        def wrapper(servicio, *args, **kwargs):
            accion = f"{type(servicio).__name__}.{metodo.__name__}"

            try:
                resultado = metodo(servicio, *args, **kwargs)
            except Exception as error:
                try:
                    servicio.servicio_auditoria.repositorio.crear(
                        Auditoria(
                            accion=accion,
                            detalles=f"ERROR: {type(error).__name__}: {error}",
                            fecha=datetime.now(timezone.utc),
                        )
                    )
                except Exception as error_auditoria:
                    # Conserva el error original si falla la auditoría.
                    raise error from error_auditoria
                raise

            servicio.servicio_auditoria.repositorio.crear(
                Auditoria(
                    accion=accion,
                    detalles="Operación completada.",
                    fecha=datetime.now(timezone.utc),
                )
            )
            return resultado

        return wrapper


class ServicioInventario:
    """Gestiona precios y stock asociados a libros mediante claves foráneas."""

    def __init__(
        self,
        repositorio_libro: RepositorioLibro,
        repositorio_precio: RepositorioPrecio,
        repositorio_stock: RepositorioStock,
        repositorio_moneda: RepositorioMoneda,
        servicio_auditoria: ServicioAuditoria,
    ):
        """Recibe los repositorios de libros, precios, stock y monedas."""
        self.repositorio_libro = repositorio_libro
        self.repositorio_precio = repositorio_precio
        self.repositorio_stock = repositorio_stock
        self.repositorio_moneda = repositorio_moneda
        self.servicio_auditoria = servicio_auditoria

    @ServicioAuditoria.auditar
    def crear_precio(self, precio: Precio) -> Precio:
        """Crea un precio y rechaza una combinación de libro y moneda existente."""
        libro = self.repositorio_libro.leer_por_id(precio.libro_id)
        if libro is None:
            raise ValueError(f"No existe un libro con ID {precio.libro_id}.")

        moneda = self.repositorio_moneda.leer_por_id(precio.moneda.id)
        if moneda is None:
            raise ValueError(f"No existe una moneda con ID {precio.moneda.id}.")

        precio.moneda = moneda

        existente = self.repositorio_precio.leer_por_libro_y_moneda(
            precio.libro_id, precio.moneda.id
        )

        if existente is not None:
            raise ValueError(
                f"Ya existe un precio para el libro {precio.libro_id} "
                f"en {precio.moneda.codigo_iso}."
            )

        return self.repositorio_precio.crear(precio)

    @ServicioAuditoria.auditar
    def actualizar_precio(self, precio: Precio) -> Precio:
        """Actualiza un precio existente para el libro y la moneda."""
        libro = self.repositorio_libro.leer_por_id(precio.libro_id)
        if libro is None:
            raise ValueError(f"No existe un libro con ID {precio.libro_id}.")

        moneda = self.repositorio_moneda.leer_por_id(precio.moneda.id)
        if moneda is None:
            raise ValueError(f"No existe una moneda con ID {precio.moneda.id}.")

        precio.moneda = moneda

        existente = self.repositorio_precio.leer_por_libro_y_moneda(
            precio.libro_id, precio.moneda.id
        )

        if existente is None:
            raise ValueError(
                f"No existe un precio para el libro {precio.libro_id} "
                f"en {precio.moneda.codigo_iso}."
            )

        return self.repositorio_precio.actualizar(precio)

    @ServicioAuditoria.auditar
    def crear_stock(self, stock: Stock) -> Stock:
        """Crea el stock de un libro que todavía no tiene uno registrado."""
        libro = self.repositorio_libro.leer_por_id(stock.libro_id)
        if libro is None:
            raise ValueError(f"No existe un libro con ID {stock.libro_id}.")

        existente = self.repositorio_stock.leer_por_libro(stock.libro_id)

        if existente is not None:
            raise ValueError(
                f"Ya existe un registro de stock para el libro {stock.libro_id}."
            )

        return self.repositorio_stock.crear(stock)

    @ServicioAuditoria.auditar
    def actualizar_stock(self, stock: Stock) -> Stock:
        """Actualiza el stock existente de un libro."""
        libro = self.repositorio_libro.leer_por_id(stock.libro_id)
        if libro is None:
            raise ValueError(f"No existe un libro con ID {stock.libro_id}.")

        existente = self.repositorio_stock.leer_por_libro(stock.libro_id)

        if existente is None:
            raise ValueError(
                f"No existe un registro de stock para el libro {stock.libro_id}."
            )

        return self.repositorio_stock.actualizar(stock)

    @ServicioAuditoria.auditar
    def leer_precios_por_libro(self, libro_id: int) -> List[Precio]:
        """Devuelve los precios del libro, o una lista vacía."""
        return self.repositorio_precio.leer_por_libro(libro_id)

    @ServicioAuditoria.auditar
    def leer_precio_por_libro_y_moneda(self, libro_id: int, moneda_id: int) -> Optional[Precio]:
        """Devuelve el precio en la moneda solicitada, o None."""
        return self.repositorio_precio.leer_por_libro_y_moneda(libro_id, moneda_id)

    @ServicioAuditoria.auditar
    def leer_stock_por_libro(self, libro_id: int) -> Optional[Stock]:
        """Devuelve el stock registrado para el libro, o None si no existe."""
        return self.repositorio_stock.leer_por_libro(libro_id)

    @ServicioAuditoria.auditar
    def eliminar_precio_por_libro_y_moneda(self, libro_id: int, moneda_id: int) -> bool:
        """Elimina ese precio; el libro puede quedar sin precios."""
        return self.repositorio_precio.eliminar(libro_id, moneda_id)

    @ServicioAuditoria.auditar
    def eliminar_stock_por_libro(self, libro_id: int) -> bool:
        """Elimina el registro de stock; el libro permanece guardado."""
        return self.repositorio_stock.eliminar(libro_id)


class ServicioCotizacion:
    """Gestiona cotizaciones identificadas por tipo, monedas y fecha."""

    def __init__(
        self,
        repositorio: RepositorioCotizacion,
        servicio_auditoria: ServicioAuditoria,
        repositorio_moneda: Optional[RepositorioMoneda] = None,
        repositorio_tipo_cotizacion: Optional[RepositorioTipoCotizacion] = None,
    ):
        """Recibe cotizaciones y los repositorios para resolver los datos de la API."""
        self.repositorio = repositorio
        self.repositorio_moneda = repositorio_moneda
        self.repositorio_tipo_cotizacion = repositorio_tipo_cotizacion
        self.servicio_auditoria = servicio_auditoria

    @ServicioAuditoria.auditar
    def obtener_cotizaciones(self) -> List[Cotizacion]:
        """Importa cotizaciones de compra y venta, omitiendo registros con errores."""
      
        archivo_env = Path(__file__).resolve().parents[3] / ".env"
        api_url = os.getenv("API_URL") or dotenv_values(archivo_env).get("API_URL")
        if not api_url:
            raise ValueError("La variable API_URL no está definida.")

        destino = self.repositorio_moneda.leer_por_codigo_iso("ARS")
        if destino is None:
            raise ValueError("La moneda ARS no está registrada.")

        solicitud = Request(
            api_url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; BookManager/1.0)",
                "Accept": "application/json",
            },
        )

        try:
            with urlopen(solicitud, timeout=10) as respuesta:
                datos = json.load(respuesta, parse_float=Decimal)
        except HTTPError as error:
            raise RuntimeError(
                f"DolarAPI devolvió HTTP {error.code}: {error.reason}."
            ) from error
        except (URLError, TimeoutError) as error:
            raise RuntimeError(
                "No se pudieron descargar las cotizaciones."
            ) from error
        except (ValueError, UnicodeDecodeError) as error:
            raise ValueError("La API no devolvió un JSON válido.") from error

        if not isinstance(datos, list) or not datos:
            raise ValueError("La API debe devolver una lista no vacía.")

        cotizaciones = []
        nombres_tipos = {"contadoconliqui": "CCL"}

        for indice, dato in enumerate(datos, start=1):
            try:
                if not isinstance(dato, dict):
                    raise ValueError("El registro debe ser un objeto.")

                codigo_iso = dato["moneda"].strip().upper()
                casa = dato["casa"].strip()
                nombre_tipo = nombres_tipos.get(casa.casefold(), casa)

                if not codigo_iso or not nombre_tipo:
                    raise ValueError("La moneda y la casa no pueden estar vacías.")

                compra = Decimal(str(dato["compra"]))
                venta = Decimal(str(dato["venta"]))
                fecha = datetime.fromisoformat(
                    dato["fechaActualizacion"].replace("Z", "+00:00")
                ).date()

                origen = self.repositorio_moneda.leer_por_codigo_iso(codigo_iso)
                if origen is None:
                    raise ValueError(f"La moneda {codigo_iso} no está registrada.")

                tipo = self.repositorio_tipo_cotizacion.leer_por_nombre(nombre_tipo)

                if tipo is None:
                    tipo = TipoCotizacion(
                        nombre=nombre_tipo,
                        descripcion=f"Cotización {nombre_tipo} obtenida desde API.",
                    )
                    tipo = self.repositorio_tipo_cotizacion.crear(tipo)

                cotizacion = Cotizacion(
                    moneda_origen=origen,
                    moneda_destino=destino,
                    tipo_cotizacion=tipo,
                    compra=compra,
                    venta=venta,
                    fecha=fecha,
                )

                existente = self.repositorio.leer_por_tipo_moneda_origen_destino_y_fecha(
                    cotizacion.tipo_cotizacion.id,
                    cotizacion.moneda_origen.id,
                    cotizacion.moneda_destino.id,
                    cotizacion.fecha,
                )

                if existente is None:
                    guardada = self.crear(cotizacion)
                else:
                    guardada = self.actualizar(cotizacion)

                cotizaciones.append(guardada)

            except Exception as error:
                print(f"No se pudo importar la cotización {indice}: {error}")
                continue

        return cotizaciones

    @ServicioAuditoria.auditar
    def crear(self, cotizacion: Cotizacion) -> Cotizacion:
        """Crea una cotización y rechaza una combinación existente."""
        existente = self.repositorio.leer_por_tipo_moneda_origen_destino_y_fecha(
            cotizacion.tipo_cotizacion.id,
            cotizacion.moneda_origen.id,
            cotizacion.moneda_destino.id,
            cotizacion.fecha,
        )

        if existente is not None:
            raise ValueError(
                "Ya existe una cotización para ese tipo, monedas y fecha."
            )

        return self.repositorio.crear(cotizacion)

    @ServicioAuditoria.auditar
    def actualizar(self, cotizacion: Cotizacion) -> Cotizacion:
        """Actualiza compra y venta de una cotización existente."""
        existente = self.repositorio.leer_por_tipo_moneda_origen_destino_y_fecha(
            cotizacion.tipo_cotizacion.id,
            cotizacion.moneda_origen.id,
            cotizacion.moneda_destino.id,
            cotizacion.fecha,
        )

        if existente is None:
            raise ValueError(
                "No existe una cotización para ese tipo, monedas y fecha."
            )

        return self.repositorio.actualizar(cotizacion)

    @ServicioAuditoria.auditar
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

    @ServicioAuditoria.auditar
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

    @ServicioAuditoria.auditar
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

    @ServicioAuditoria.auditar
    def leer_ultima_por_tipo_y_monedas(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int,
    ) -> Optional[Cotizacion]:
        """Devuelve la cotización más reciente del tipo y las monedas indicadas."""
        cotizaciones = (
            self.repositorio
            .leer_historico_por_tipo_moneda_origen_moneda_destino(
                tipo_id,
                moneda_origen_id,
                moneda_destino_id,
            )
        )

        return max(
            cotizaciones,
            key=lambda cotizacion: cotizacion.fecha,
            default=None,
        )

    @ServicioAuditoria.auditar
    def leer_ultimas_cotizaciones_por_monedas(
        self,
        moneda_origen: Moneda,
        moneda_destino: Moneda,
    )-> list[Cotizacion]:
        """Devuelve la última cotización disponible por cada tipo."""
        if moneda_origen.id is None or moneda_destino.id is None:
            raise ValueError("Las monedas deben estar registradas.")


        cotizaciones = []

        for tipo in self.repositorio_tipo_cotizacion.leer_todos():
            ultima = self.leer_ultima_por_tipo_y_monedas(
                tipo.id,
                moneda_origen.id,
                moneda_destino.id,
        )
            if ultima is not None:
                cotizaciones.append(ultima)

        return cotizaciones


class ServicioCatalogo:
    """Gestiona las operaciones CRUD de libros, evitando ISBN duplicados."""

    def __init__(
        self,
        repositorio: RepositorioLibro,
        repositorio_editorial: RepositorioEditorial,
        repositorio_genero: RepositorioGenero,
        repositorio_precio: RepositorioPrecio,
        repositorio_stock: RepositorioStock,
        servicio_auditoria: ServicioAuditoria,
    ):
        """Recibe los repositorios de libros y sus entidades relacionadas."""
        self.repositorio = repositorio
        self.repositorio_editorial = repositorio_editorial
        self.repositorio_genero = repositorio_genero
        self.repositorio_precio = repositorio_precio
        self.repositorio_stock = repositorio_stock
        self.servicio_auditoria = servicio_auditoria

    @ServicioAuditoria.auditar
    def crear(self, libro: Libro) -> Libro:
        """Crea un libro sin ID y evita ISBN duplicados."""
        if libro.id is not None:
            raise ValueError("Un libro nuevo no debe tener un ID asignado.")

        existente = self.repositorio.leer_por_isbn(libro.isbn)

        if existente is not None:
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

        return self.repositorio.crear(libro)

    @ServicioAuditoria.auditar
    def actualizar(self, libro: Libro) -> Libro:
        """Actualiza un libro existente y evita ISBN duplicados."""
        if libro.id is None:
            raise ValueError("El libro debe tener un ID para actualizar.")

        if self.repositorio.leer_por_id(libro.id) is None:
            raise ValueError(
                f"No existe un libro con ID {libro.id}."
            )

        existente = self.repositorio.leer_por_isbn(libro.isbn)

        if existente is not None and existente.id != libro.id:
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

        return self.repositorio.actualizar(libro)

    @ServicioAuditoria.auditar
    def eliminar(self, id: int) -> bool:
        """Elimina el libro y sus relaciones mediante la cascada del repositorio.

        Devuelve False si el libro no existe.
        """
        return self.repositorio.eliminar(id)

    @ServicioAuditoria.auditar
    def leer_por_id(self, id: int) -> Optional[Libro]:
        """Devuelve el libro con el ID indicado, o None si no existe."""
        return self.repositorio.leer_por_id(id)

    @ServicioAuditoria.auditar
    def listar_todos(self) -> List[Libro]:
        """Devuelve todos los libros del repositorio."""
        return self.repositorio.leer_todos()


class ServicioEditorial:
    """Gestiona editoriales, evitando nombres duplicados y eliminaciones en uso."""

    def __init__(
        self,
        repositorio: RepositorioEditorial,
        repositorio_libro: RepositorioLibro,
        servicio_auditoria: ServicioAuditoria,
    ):
        """Recibe los repositorios de editoriales y libros y el servicio de auditoría."""
        self.repositorio = repositorio
        self.repositorio_libro = repositorio_libro
        self.servicio_auditoria = servicio_auditoria

    @ServicioAuditoria.auditar
    def crear(self, editorial: Editorial) -> Editorial:
        """Crea una editorial sin ID y evita nombres duplicados."""
        if editorial.id is not None:
            raise ValueError("Una editorial nueva no debe tener un ID asignado.")

        existente = self.repositorio.leer_por_nombre(editorial.nombre)

        if existente is not None:
            raise ValueError(
                f"Ya existe una editorial con nombre '{editorial.nombre}'."
            )

        return self.repositorio.crear(editorial)

    @ServicioAuditoria.auditar
    def actualizar(self, editorial: Editorial) -> Editorial:
        """Actualiza una editorial existente y evita nombres duplicados."""
        if editorial.id is None:
            raise ValueError("La editorial debe tener un ID para actualizar.")

        if self.repositorio.leer_por_id(editorial.id) is None:
            raise ValueError(
                f"No existe una editorial con ID {editorial.id}."
            )

        existente = self.repositorio.leer_por_nombre(editorial.nombre)

        if existente is not None and existente.id != editorial.id:
            raise ValueError(
                f"Ya existe una editorial con nombre '{editorial.nombre}'."
            )

        return self.repositorio.actualizar(editorial)

    @ServicioAuditoria.auditar
    def leer_por_id(self, id: int) -> Optional[Editorial]:
        """Devuelve la editorial con el ID indicado, o None si no existe."""
        return self.repositorio.leer_por_id(id)

    @ServicioAuditoria.auditar
    def leer_todos(self) -> List[Editorial]:
        """Devuelve todas las editoriales del repositorio."""
        return self.repositorio.leer_todos()

    @ServicioAuditoria.auditar
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
        servicio_auditoria: ServicioAuditoria,
    ):
        """Recibe los repositorios de géneros y libros de la aplicación."""
        self.repositorio = repositorio
        self.repositorio_libro = repositorio_libro
        self.servicio_auditoria = servicio_auditoria

    @ServicioAuditoria.auditar
    def crear(self, genero: Genero) -> Genero:
        """Crea un género sin ID y evita nombres duplicados."""
        if genero.id is not None:
            raise ValueError("Un género nuevo no debe tener un ID asignado.")

        existente = self.repositorio.leer_por_nombre(genero.nombre)

        if existente is not None:
            raise ValueError(
                f"Ya existe un género con nombre '{genero.nombre}'."
            )

        return self.repositorio.crear(genero)

    @ServicioAuditoria.auditar
    def actualizar(self, genero: Genero) -> Genero:
        """Actualiza un género existente y evita nombres duplicados."""
        if genero.id is None:
            raise ValueError("El género debe tener un ID para actualizar.")

        if self.repositorio.leer_por_id(genero.id) is None:
            raise ValueError(
                f"No existe un género con ID {genero.id}."
            )

        existente = self.repositorio.leer_por_nombre(genero.nombre)

        if existente is not None and existente.id != genero.id:
            raise ValueError(
                f"Ya existe un género con nombre '{genero.nombre}'."
            )

        return self.repositorio.actualizar(genero)

    @ServicioAuditoria.auditar
    def leer_por_id(self, id: int) -> Optional[Genero]:
        """Devuelve el género con el ID indicado, o None si no existe."""
        return self.repositorio.leer_por_id(id)

    @ServicioAuditoria.auditar
    def leer_todos(self) -> List[Genero]:
        """Devuelve todos los géneros del repositorio."""
        return self.repositorio.leer_todos()

    @ServicioAuditoria.auditar
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
            repositorio_cotizacion: RepositorioCotizacion,
            servicio_auditoria: ServicioAuditoria,
            ):
        """Recibe los repositorios de tipos de cotización y cotizaciones."""
        self.repositorio = repositorio
        self.repositorio_cotizacion = repositorio_cotizacion
        self.servicio_auditoria = servicio_auditoria

    @ServicioAuditoria.auditar
    def crear(self, tipo_cotizacion: TipoCotizacion) -> TipoCotizacion:
        """Crea un tipo de cotización sin ID y evita nombres duplicados."""
        if tipo_cotizacion.id is not None:
            raise ValueError(
                "Un tipo de cotización nuevo no debe tener un ID asignado."
            )

        existente = self.repositorio.leer_por_nombre(
            tipo_cotizacion.nombre
        )

        if existente is not None:
            raise ValueError(
                f"Ya existe un tipo de cotización con nombre '{tipo_cotizacion.nombre}'."
            )

        return self.repositorio.crear(tipo_cotizacion)

    @ServicioAuditoria.auditar
    def actualizar(self, tipo_cotizacion: TipoCotizacion) -> TipoCotizacion:
        """Actualiza un tipo de cotización existente y evita nombres duplicados."""
        if tipo_cotizacion.id is None:
            raise ValueError(
                "El tipo de cotización debe tener un ID para actualizar."
            )

        if self.repositorio.leer_por_id(tipo_cotizacion.id) is None:
            raise ValueError(
                f"No existe un tipo de cotización con ID {tipo_cotizacion.id}."
            )

        existente = self.repositorio.leer_por_nombre(
            tipo_cotizacion.nombre
        )

        if existente is not None and existente.id != tipo_cotizacion.id:
            raise ValueError(
                f"Ya existe un tipo de cotización con nombre '{tipo_cotizacion.nombre}'."
            )

        return self.repositorio.actualizar(tipo_cotizacion)

    @ServicioAuditoria.auditar
    def leer_por_id(self, id: int) -> Optional[TipoCotizacion]:
        """Devuelve el tipo de cotización con el ID indicado, o None si no existe."""
        return self.repositorio.leer_por_id(id)

    @ServicioAuditoria.auditar
    def leer_todos(self) -> List[TipoCotizacion]:
        """Devuelve la lista de tipos de cotización del repositorio."""
        return self.repositorio.leer_todos()

    @ServicioAuditoria.auditar
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
                 repositorio_precio: RepositorioPrecio,
                 servicio_auditoria: ServicioAuditoria):
        """Recibe los repositorios de monedas, cotizaciones y precios."""
        self.repositorio = repositorio
        self.repositorio_cotizacion = repositorio_cotizacion
        self.repositorio_precio = repositorio_precio
        self.servicio_auditoria = servicio_auditoria

    @ServicioAuditoria.auditar
    def crear(self, moneda: Moneda) -> Moneda:
        """Crea una moneda sin ID y evita códigos ISO duplicados."""
        if moneda.id is not None:
            raise ValueError("Una moneda nueva no debe tener un ID asignado.")

        existente = self.repositorio.leer_por_codigo_iso(moneda.codigo_iso)

        if existente is not None:
            raise ValueError(
                f"Ya existe una moneda con código ISO '{moneda.codigo_iso}'."
            )

        return self.repositorio.crear(moneda)

    @ServicioAuditoria.auditar
    def actualizar(self, moneda: Moneda) -> Moneda:
        """Actualiza una moneda existente y evita códigos ISO duplicados."""
        if moneda.id is None:
            raise ValueError("La moneda debe tener un ID para actualizar.")

        if self.repositorio.leer_por_id(moneda.id) is None:
            raise ValueError(
                f"No existe una moneda con ID {moneda.id}."
            )

        existente = self.repositorio.leer_por_codigo_iso(moneda.codigo_iso)

        if existente is not None and existente.id != moneda.id:
            raise ValueError(
                f"Ya existe una moneda con código ISO '{moneda.codigo_iso}'."
            )

        return self.repositorio.actualizar(moneda)

    @ServicioAuditoria.auditar
    def leer_por_id(self, id: int) -> Optional[Moneda]:
        """Devuelve la moneda con el ID indicado, o None si no existe."""
        return self.repositorio.leer_por_id(id)

    @ServicioAuditoria.auditar
    def leer_todos(self) -> List[Moneda]:
        """Devuelve la lista de monedas del repositorio."""
        return self.repositorio.leer_todos()

    @ServicioAuditoria.auditar
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

class ServicioCotizador:
    """Convierte precios entre las monedas de una cotización."""

    @staticmethod
    def convertir_precio(
        precio: Precio,
        cotizacion: Cotizacion,
    ) -> Decimal:

        if precio is None and cotizacion is None:
            raise ValueError("Se requieren un precio y una cotización.")

        if precio is None:
            raise ValueError("Se requiere un precio para convertir.")

        if cotizacion is None:
            raise ValueError("Se requiere una cotización para convertir.")
        
        moneda = precio.moneda.codigo_iso
        origen = cotizacion.moneda_origen.codigo_iso
        destino = cotizacion.moneda_destino.codigo_iso
        tasa = cotizacion.venta

        if moneda == origen:
            resultado = precio.precio_base * tasa
        elif moneda == destino:
            resultado = precio.precio_base / tasa
        else:
            raise ValueError("La moneda del precio no pertenece a la cotización.")

        return resultado.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
