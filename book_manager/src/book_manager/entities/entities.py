
import re, math
from decimal import Decimal, InvalidOperation
from datetime import date, datetime

class EntidadBase:
    """Entidad base con un identificador opcional."""

    def __init__(self, id: int | None = None):
        self.id = id

    @property
    def id(self) -> int | None:
        return self._id

    @id.setter
    def id(self, valor: int | None):
        if valor is not None:
            if isinstance(valor, bool) or not isinstance(valor, int):
                raise TypeError("El ID debe ser un número entero o None.")

            if valor <= 0:
                raise ValueError("El ID debe ser mayor que cero.")

        self._id = valor

class TipoCotizacion(EntidadBase):
    """Representa un tipo de cotización con su nombre y descripción."""

    def __init__(self, nombre: str, descripcion: str):
        super().__init__()
        self.nombre = nombre
        self.descripcion = descripcion

    # Propiedad nombre
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("El nombre debe ser una cadena de texto.")

        if not 1 <= len(valor) <= 15:
            raise ValueError("El nombre debe tener entre 1 y 15 caracteres.")

        self._nombre = valor

    # Propiedad descripcion
    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("La descripción debe ser una cadena de texto.")

        if not 1 <= len(valor) <= 50:
            raise ValueError("La descripción debe tener entre 1 y 50 caracteres.")

        self._descripcion = valor


class Moneda(EntidadBase):
    """Representa una moneda con su código ISO, nombre y símbolo."""

    def __init__(
        self,
        codigo_iso: str,
        nombre: str,
        simbolo: str,
    ):
        super().__init__()

        self.codigo_iso = codigo_iso
        self.nombre = nombre
        self.simbolo = simbolo

    # Propiedad codigo_iso
    @property
    def codigo_iso(self) -> str:
        return self._codigo_iso

    @codigo_iso.setter
    def codigo_iso(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("El código ISO debe ser una cadena de texto.")

        valor = valor.upper()

        if not re.fullmatch(r"[A-Z]{3}", valor):
            raise ValueError(
                "El código ISO debe contener exactamente 3 letras mayúsculas."
            )

        self._codigo_iso = valor

    # Propiedad nombre
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("El nombre debe ser una cadena de texto.")

        if not 1 <= len(valor) <= 50:
            raise ValueError(
                "El nombre debe tener entre 1 y 50 caracteres."
            )

        self._nombre = valor

    # Propiedad simbolo
    @property
    def simbolo(self) -> str:
        return self._simbolo

    @simbolo.setter
    def simbolo(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("El símbolo debe ser una cadena de texto.")

        if not 1 <= len(valor) <= 5:
            raise ValueError(
                "El símbolo debe tener entre 1 y 5 caracteres."
            )

        self._simbolo = valor

class Genero(EntidadBase):
    """Representa un tipo de género literario con su nombre y descripcion."""

    def __init__(
        self,
        nombre: str,
        descripcion: str
    ):
        super().__init__()
        self.nombre = nombre
        self.descripcion = descripcion

    # Propiedad nombre
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("El nombre debe ser una cadena de texto.")

        if not 3 <= len(valor) <= 20:
            raise ValueError(
                "El nombre debe tener entre 3 y 20 caracteres."
            )

        self._nombre = valor

    # Propiedad descripcion
    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("La descripción debe ser una cadena de texto.")

        if not 1 <= len(valor) <= 50:
            raise ValueError(
                "La descripción debe tener entre 1 y 50 caracteres."
            )

        self._descripcion = valor


class Editorial(EntidadBase):
    """Representa una editorial con sus datos de contacto."""

    def __init__(
        self,
        nombre: str,
        grupo: str,
        pais_origen: str,
        telefono: str,
        email: str
    ):
        super().__init__()
        self.nombre = nombre
        self.grupo = grupo
        self.pais_origen = pais_origen
        self.telefono = telefono
        self.email = email

    def __str__(self) -> str:
        return (
            f"Editorial(id={self.id}, "
            f"nombre={self.nombre!r}, "
            f"grupo={self.grupo!r}, "
            f"pais_origen={self.pais_origen!r}, "
            f"telefono={self.telefono!r}, "
            f"Email={self.email!r})"
        )
    
    # Propiedad nombre
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("El nombre debe ser una cadena de texto.")

        if not 1 <= len(valor) <= 50:
            raise ValueError(
                "El nombre debe tener entre 1 y 50 caracteres."
            )

        self._nombre = valor

    # Propiedad grupo
    @property
    def grupo(self) -> str:
        return self._grupo

    @grupo.setter
    def grupo(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("El grupo debe ser una cadena de texto.")

        if not 1 <= len(valor) <= 50:
            raise ValueError(
                "El grupo debe tener entre 1 y 50 caracteres."
            )

        self._grupo = valor

    # Propiedad pais_origen
    @property
    def pais_origen(self) -> str:
        return self._pais_origen

    @pais_origen.setter
    def pais_origen(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("El país de origen debe ser una cadena de texto.")

        if not 2 <= len(valor) <= 20:
            raise ValueError(
                "El país de origen debe tener entre 2 y 20 caracteres."
            )

        self._pais_origen = valor

    # Propiedad telefono
    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("El teléfono debe ser una cadena de texto.")

        if not 7 <= len(valor) <= 20:
            raise ValueError(
                "El teléfono debe tener entre 7 y 20 caracteres."
            )

        patron = r"^\+?[0-9\s\-]{7,20}$"

        if not re.fullmatch(patron, valor):
            raise ValueError(
                "El teléfono debe tener un formato válido "
                "(ej: +123456789 o 444-5555)."
            )

        self._telefono = valor

    # Propiedad email
    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("El email debe ser una cadena de texto.")

        patron = r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        if not re.fullmatch(patron, valor):
            raise ValueError(
                "El email debe tener un formato válido."
            )

        self._email = valor


class Precio:
    """Representa un precio con su moneda y precio base"""

    def __init__(
        self,
        libro_id: int,
        moneda: Moneda,
        precio_base: Decimal
    ):
        self.libro_id = libro_id
        self.moneda = moneda
        self.precio_base = precio_base

    @property
    def libro_id(self) -> int:
        return self._libro_id

    @libro_id.setter
    def libro_id(self, valor: int):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("El ID del libro debe ser un entero.")

        if valor <= 0:
            raise ValueError("El ID del libro debe ser mayor a cero.")

        self._libro_id = valor

    # Propiedad moneda
    @property
    def moneda(self) -> Moneda:
        return self._moneda

    @moneda.setter
    def moneda(self, valor: Moneda):
        if not isinstance(valor, Moneda):
            raise TypeError(
                "La moneda debe ser una instancia de la clase Moneda."
            )

        self._moneda = valor

    # Propiedad precio_base
    @property
    def precio_base(self) -> Decimal:
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor: Decimal):
        if isinstance(valor, bool):
            raise TypeError("El precio debe ser un valor numérico.")

        try:
            valor = Decimal(str(valor))
        except (InvalidOperation, ValueError, TypeError):
            raise TypeError("El precio debe ser un valor numérico válido.")

        if not valor.is_finite():
            raise ValueError("El precio no puede ser infinito ni nulo.")

        if valor < 0:
            raise ValueError("El precio debe ser mayor o igual a cero.")

        # Validar máximo de 2 decimales
        if valor.as_tuple().exponent < -2:
            raise ValueError(
                "El precio no puede tener más de 2 decimales."
            )

        # Validar máximo de 10 dígitos (8 enteros + 2 decimales)
        if valor >= Decimal("100000000"):
            raise ValueError(
                "El precio no puede superar los 8 dígitos enteros."
            )

        self._precio_base = valor

class Stock:
    """Representa el stock de un libro con su cantidad minima y total de ejemplares."""

    def __init__(
        self,
        libro_id: int,
        cantidad_minima: int,
        cantidad_total: int
    ):
        self.libro_id = libro_id
        self.cantidad_minima = cantidad_minima
        self.cantidad_total = cantidad_total

    @property
    def libro_id(self) -> int:
        return self._libro_id
    
    # Propiedad cantidad_minima
    @property
    def cantidad_minima(self) -> int:
        return self._cantidad_minima

    @libro_id.setter
    def libro_id(self, valor: int):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("El ID del libro debe ser un entero.")

        if valor <= 0:
            raise ValueError("El ID del libro debe ser mayor a cero.")

        self._libro_id = valor

    @cantidad_minima.setter
    def cantidad_minima(self, valor: int):
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError(
                "La cantidad mínima debe ser un número entero."
            )

        if valor < 0:
            raise ValueError(
                "La cantidad mínima no puede ser menor a 0."
            )

        self._cantidad_minima = valor

    # Propiedad cantidad_total
    @property
    def cantidad_total(self) -> int:
        return self._cantidad_total

    @cantidad_total.setter
    def cantidad_total(self, valor: int):
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError(
                "La cantidad total debe ser un número entero."
            )

        if valor < 0:
            raise ValueError(
                "La cantidad total no puede ser menor a 0."
            )

        self._cantidad_total = valor


class Cotizacion:
    """Representa los importes de compra y venta entre dos monedas en una fecha."""

    def __init__(
        self,
        moneda_origen: Moneda,
        moneda_destino: Moneda,
        tipo_cotizacion: TipoCotizacion,
        compra: Decimal,
        venta: Decimal,
        fecha: date
    ):
        self.moneda_origen = moneda_origen
        self.moneda_destino = moneda_destino
        self.tipo_cotizacion = tipo_cotizacion
        self.compra = compra
        self.venta = venta
        self.fecha = fecha

    # Propiedad moneda_origen
    @property
    def moneda_origen(self) -> Moneda:
        return self._moneda_origen

    @moneda_origen.setter
    def moneda_origen(self, valor: Moneda):
        if not isinstance(valor, Moneda):
            raise TypeError(
                "La moneda de origen debe ser una instancia de Moneda."
            )

        self._moneda_origen = valor

    # Propiedad moneda_destino
    @property
    def moneda_destino(self) -> Moneda:
        return self._moneda_destino

    @moneda_destino.setter
    def moneda_destino(self, valor: Moneda):
        if not isinstance(valor, Moneda):
            raise TypeError(
                "La moneda de destino debe ser una instancia de Moneda."
            )

        self._moneda_destino = valor

    # Propiedad tipo_cotizacion
    @property
    def tipo_cotizacion(self) -> TipoCotizacion:
        return self._tipo_cotizacion

    @tipo_cotizacion.setter
    def tipo_cotizacion(self, valor: TipoCotizacion):
        if not isinstance(valor, TipoCotizacion):
            raise TypeError(
                "El tipo de cotización debe ser una instancia de TipoCotizacion."
            )

        self._tipo_cotizacion = valor

    # Propiedad compra
    @property
    def compra(self) -> Decimal:
        return self._compra

    @compra.setter
    def compra(self, valor: Decimal):
        if isinstance(valor, bool):
            raise TypeError("La compra debe ser numérica.")

        try:
            valor = Decimal(str(valor))
        except (InvalidOperation, ValueError, TypeError):
            raise TypeError(
                "La compra de la cotización debe ser numérica."
            )

        if not valor.is_finite():
            raise ValueError(
                "La compra no puede ser infinita ni nula."
            )

        if valor <= 0:
            raise ValueError(
                "La compra de la cotización debe ser mayor a cero."
            )

        # Validar máximo de 2 decimales
        if valor.as_tuple().exponent < -2:
            raise ValueError(
                "La compra no puede tener más de 2 decimales."
            )

        # Validar máximo de 12 dígitos (10 enteros + 2 decimales)
        if valor >= Decimal("10000000000"):
            raise ValueError(
                "La compra no puede superar los 10 dígitos enteros."
            )

        self._compra = valor

    # Propiedad venta
    @property
    def venta(self) -> Decimal:
        return self._venta

    @venta.setter
    def venta(self, valor: Decimal):
        if isinstance(valor, bool):
            raise TypeError("La venta debe ser numérica.")

        try:
            valor = Decimal(str(valor))
        except (InvalidOperation, ValueError, TypeError):
            raise TypeError(
                "La venta de la cotización debe ser numérica."
            )

        if not valor.is_finite():
            raise ValueError(
                "La venta no puede ser infinita ni nula."
            )

        if valor <= 0:
            raise ValueError(
                "La venta de la cotización debe ser mayor a cero."
            )

        # Validar máximo de 2 decimales
        if valor.as_tuple().exponent < -2:
            raise ValueError(
                "La venta no puede tener más de 2 decimales."
            )

        # Validar máximo de 12 dígitos (10 enteros + 2 decimales)
        if valor >= Decimal("10000000000"):
            raise ValueError(
                "La venta no puede superar los 10 dígitos enteros."
            )

        self._venta = valor

    # Propiedad fecha
    @property
    def fecha(self) -> date:
        return self._fecha

    @fecha.setter
    def fecha(self, valor: date):
        if not isinstance(valor, date):
            raise TypeError(
                "La fecha debe ser una instancia de fecha."
            )

        self._fecha = valor


class Libro(EntidadBase):
    """Representa un libro con sus datos bibliográficos, precios y stock."""

    def __init__(
        self,
        isbn: str,
        titulo: str,
        autor: str,
        peso: float,
        dimensiones: str,
        numero_paginas: int,
        fecha_publicacion: date,
        idioma: str,
        editorial: Editorial,
        genero: Genero,
        precios: list[Precio] | None = None,
        stock: Stock = None
    ):
        super().__init__()
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.peso = peso
        self.dimensiones = dimensiones
        self.numero_paginas = numero_paginas
        self.fecha_publicacion = fecha_publicacion
        self.idioma = idioma
        self.editorial = editorial
        self.genero = genero
        self.precios = precios if precios is not None else []
        self.stock = stock

    # Propiedad isbn
    @property
    def isbn(self) -> str:
        return self._isbn

    @isbn.setter
    def isbn(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("El ISBN debe ser una cadena de texto.")

        if not 10 <= len(valor) <= 13:
            raise ValueError(
                "El ISBN debe tener entre 10 y 13 caracteres."
            )

        self._isbn = valor

    # Propiedad titulo
    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("El título debe ser una cadena de texto.")

        if not 1 <= len(valor) <= 30:
            raise ValueError(
                "El título debe tener entre 1 y 20 caracteres."
            )

        self._titulo = valor

    # Propiedad autor
    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("El autor debe ser una cadena de texto.")

        if not 1 <= len(valor) <= 20:
            raise ValueError(
                "El autor debe tener entre 1 y 20 caracteres."
            )

        self._autor = valor

    # Propiedad peso
    @property
    def peso(self) -> float:
        return self._peso

    @peso.setter
    def peso(self, valor: float):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise TypeError("El peso debe ser un número.")

        if not math.isfinite(valor):
            raise ValueError(
                "El peso no puede ser infinito ni nulo."
            )

        if valor <= 0:
            raise ValueError(
                "El peso debe ser mayor a cero."
            )

        self._peso = float(valor)

    # Propiedad dimensiones
    @property
    def dimensiones(self) -> str:
        return self._dimensiones

    @dimensiones.setter
    def dimensiones(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError(
                "Las dimensiones deben ser una cadena de texto."
            )

        if not 5 <= len(valor) <= 50:
            raise ValueError(
                "Las dimensiones deben tener entre 5 y 20 caracteres."
            )

        self._dimensiones = valor

    # Propiedad numero_paginas
    @property
    def numero_paginas(self) -> int:
        return self._numero_paginas

    @numero_paginas.setter
    def numero_paginas(self, valor: int):
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError(
                "El número de páginas debe ser un número entero."
            )

        if valor <= 0:
            raise ValueError(
                "El número de páginas debe ser mayor a cero."
            )

        self._numero_paginas = valor

    # Propiedad fecha_publicacion
    @property
    def fecha_publicacion(self) -> date:
        return self._fecha_publicacion

    @fecha_publicacion.setter
    def fecha_publicacion(self, valor: date):
        if not isinstance(valor, date) or isinstance(valor, datetime):
            raise TypeError(
                "La fecha de publicación debe ser una instancia de fecha."
            )

        if valor > date.today():
            raise ValueError(
                "La fecha de publicación no puede ser una fecha futura."
            )

        self._fecha_publicacion = valor

    # Propiedad idioma
    @property
    def idioma(self) -> str:
        return self._idioma

    @idioma.setter
    def idioma(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("El idioma debe ser una cadena de texto.")

        if not 2 <= len(valor) <= 30:
            raise ValueError(
                "El idioma debe tener entre 2 y 30 caracteres."
            )

        self._idioma = valor

    # Propiedad editorial
    @property
    def editorial(self) -> Editorial:
        return self._editorial

    @editorial.setter
    def editorial(self, valor: Editorial):
        if not isinstance(valor, Editorial):
            raise TypeError(
                "La editorial debe ser una instancia de Editorial."
            )

        self._editorial = valor

    # Propiedad genero
    @property
    def genero(self) -> Genero:
        return self._genero

    @genero.setter
    def genero(self, valor: Genero):
        if not isinstance(valor, Genero):
            raise TypeError(
                "El género debe ser una instancia de Genero."
            )

        self._genero = valor

    # Propiedad precios
    @property
    def precios(self) -> list[Precio]:
        # Una copia evita agregar duplicados sin pasar por la validación.
        return list(self._precios)

    @precios.setter
    def precios(self, valor: list[Precio]):
        if not isinstance(valor, list) or any(not isinstance(p, Precio) for p in valor):
            raise TypeError("Los precios deben ser una lista de instancias de Precio.")
        monedas = [p.moneda.codigo_iso for p in valor]
        ids = [p.moneda.id for p in valor if p.moneda.id is not None]
        if len(monedas) != len(set(monedas)) or len(ids) != len(set(ids)):
            raise ValueError("El libro no puede tener dos precios en la misma moneda.")
        libro_id = getattr(self, "id", None)
        if libro_id is not None and any(p.libro_id != libro_id for p in valor):
            raise ValueError("Todos los precios deben pertenecer al libro.")
        self._precios = list(valor)

    # Propiedad stock
    @property
    def stock(self) -> Stock | None:
        return self._stock

    @stock.setter
    def stock(self, valor: Stock | None):
        if valor is not None and not isinstance(valor, Stock):
            raise TypeError(
                "El stock debe ser una instancia de Stock."
            )

        self._stock = valor
