from datetime import date

from sqlalchemy.exc import SQLAlchemyError

from ui.console_helper import (
    limpiar_pantalla, 
    mostrar_menu,
    input_entero,
    input_decimal,
    input_fecha,
    mostrar_separador,
)

from entities.entities import (
    Editorial,
    Genero,
    Moneda,
    TipoCotizacion,
    Cotizacion,
    Libro,
    Stock,
    Precio,
)
from services.services import (
    ServicioEditorial,
    ServicioGenero,
    ServicoMoneda,
    ServicioTipoCotizacion,
    ServicioCotizacion,
    ServicioCatalogo,
    ServicioInventario,
 )


class ConsolaGeneral:
    """Clase encargada de inicializar los controladores y ejecutar los menús."""
    def __init__(self, 
                 servicio_editorial: ServicioEditorial,
                 servicio_genero: ServicioGenero,
                 servicio_moneda: ServicoMoneda,
                 servicio_tipo_cotizacion: ServicioTipoCotizacion,
                 servicio_cotizacion: ServicioCotizacion,
                 servicio_catalogo: ServicioCatalogo,
                 servicio_inventario: ServicioInventario,
        ):
        self.servicio_editorial = servicio_editorial
        self.servicio_genero = servicio_genero
        self.servicio_moneda = servicio_moneda
        self.servicio_tipo_cotizacion = servicio_tipo_cotizacion
        # Mapeo de opciones a controladores configurados dinámicamente
        self.controladores = {
            "1": ControladorEditorial(self.servicio_editorial),
            "2": ControladorGenero(self.servicio_genero),
            "3": ControladorMoneda(self.servicio_moneda),
            "4": ControladorTipoCotizacion(self.servicio_tipo_cotizacion),
            "5": ControladorCatalogo(
                servicio_catalogo, servicio_editorial, servicio_genero
            ),
            "6": ControladorInventario(
                servicio_inventario, servicio_catalogo, servicio_moneda
            ),
            "7": ControladorCotizacion(
                servicio_cotizacion, servicio_moneda, servicio_tipo_cotizacion
            ),
        }

    def ejecutar(self):
        """Inicia el bucle del menú principal de la aplicación."""
        while True:
            limpiar_pantalla()
            print()
            mostrar_separador()
            print("  SISTEMA DE GESTIÓN DE LIBRERÍA  ")
            mostrar_separador()
            print("1. Gestionar Editoriales")
            print("2. Gestionar Géneros")
            print("3. Gestionar Monedas")
            print("4. Gestionar Tipos de Cotización")
            print("5. Gestionar Catálogo")
            print("6. Gestionar Inventario")
            print("7. Gestionar Cotizaciones")
            print("8. Salir del Sistema")
            mostrar_separador()
            
            opcion = input("Seleccione una opción (1-8): ").strip()
            limpiar_pantalla()

            match opcion:
                case "1":
                    self.controladores[opcion].ejecutar()
                case "2":
                    self.controladores[opcion].ejecutar()
                case "3":
                    self.controladores[opcion].ejecutar()
                case "4":
                    self.controladores[opcion].ejecutar()
                case "5":
                    self.controladores[opcion].ejecutar()
                case "6":
                    self.controladores[opcion].ejecutar()
                case "7":
                    self.controladores[opcion].ejecutar()
                case "8":
                    print("¡Gracias por usar el sistema!")
                    return
                case _:
                    print("Opción inválida.")
                    input("\nPresione Enter para continuar...")

class ControladorInventario:
    """Gestiona por consola el alta, modificación, baja y búsqueda de stock y precios por libro."""

    def __init__(self, servicio: ServicioInventario,
                 servicio_catalogo: ServicioCatalogo,
                 servicio_moneda: ServicoMoneda):
        self.servicio = servicio
        self.servicio_catalogo = servicio_catalogo
        self.servicio_moneda = servicio_moneda

    def ejecutar(self):
        opciones = {
            "1": ("Alta de stock", self.alta_stock),
            "2": ("Modificación de stock", self.modificacion_stock),
            "3": ("Baja de stock", self.baja_stock),
            "4": ("Buscar stock por libro", self.buscar_stock_por_libro),
            "5": ("Alta de precio", self.alta_precio),
            "6": ("Modificación de precio", self.modificacion_precio),
            "7": ("Baja de precio", self.baja_precio),
            "8": ("Buscar precios por libro", self.buscar_precios_por_libro),
            "9": ("Listar precios bimonetarios", self.listar_precios_bimonetarios),
            "10": ("Exportar precios a archivo CSV", self.exportar_precios_csv),
            "11": ("Volver atrás", None),
        }
        while True:
            limpiar_pantalla()
            opcion = mostrar_menu("GESTIÓN DE INVENTARIO", opciones)
            limpiar_pantalla()

            if opcion not in opciones:
                print("Opción inválida.")
            else:
                _, accion = opciones[opcion]
                if accion is None:
                    return
                accion()
            input("\nPresione Enter para continuar...")

    def listar_precios_bimonetarios(self):
        """Informa que el listado de precios bimonetarios está pendiente."""
        print("Sección en construcción")

    def exportar_precios_csv(self):
        """Informa que la exportación de precios está pendiente."""
        print("Sección en construcción")

    def _pedir_libro(self):
        """Solicita el ID de un libro, valida su existencia y devuelve el objeto."""
        libro_id = input_entero("ID de libro: ")
        libro = self.servicio_catalogo.leer_por_id(libro_id)
        if libro is None:
            raise ValueError("No existe ese libro.")
        print(f"Libro: {libro.isbn} - {libro.titulo}")
        return libro

    def _pedir_moneda(self):
        """Solicita el ID de una moneda y valida su existencia."""
        moneda_id = input_entero("ID de moneda: ")
        moneda = self.servicio_moneda.leer_por_id(moneda_id)
        if moneda is None:
            raise ValueError("No existe esa moneda.")
        print(f"Moneda: {moneda.codigo_iso} - {moneda.nombre}")
        return moneda

    @staticmethod
    def _mostrar_stock(libro, stock):
        mostrar_separador()
        print("ID libro", "ISBN", "Título", "Stock mínimo", "Stock total", sep=" | ")
        mostrar_separador()
        print(libro.id, libro.isbn, libro.titulo, stock.cantidad_minima,
              stock.cantidad_total, sep=" | ")

    @staticmethod
    def _mostrar_precio(libro, precio):
        ControladorInventario._mostrar_precios(libro, [precio])

    @staticmethod
    def _mostrar_precios(libro, precios):
        mostrar_separador()
        print("ID libro", "ISBN", "Título", "Moneda", "Precio Base", sep=" | ")
        mostrar_separador()
        for precio in precios:
            print(libro.id, libro.isbn, libro.titulo,
                  precio.moneda.codigo_iso, f"{precio.precio_base:.2f}", sep=" | ")

    def alta_stock(self):
        print("\n--- ALTA DE STOCK ---")
        try:
            libro = self._pedir_libro()
            
            stock = Stock(
                libro_id=libro.id,
                cantidad_minima=input_entero("Cantidad mínima: "),
                cantidad_total=input_entero("Cantidad total: "),
            )
            self.servicio.guardar_stock(stock)
            print("Stock creado correctamente.")
        except (ValueError, TypeError) as error:
            print(f"No se pudo crear el stock: {error}")

    def modificacion_stock(self):
        print("\n--- MODIFICACIÓN DE STOCK ---")
        try:
            libro = self._pedir_libro()
            actual = self.servicio.leer_stock_por_libro(libro.id)
            if actual is None:
                print("No hay stock registrado para ese libro.")
                return
            self._mostrar_stock(libro, actual)
            print("Presione Enter para conservar el valor actual.")
            minima = input_entero(
                f"Cantidad mínima [{actual.cantidad_minima}]: ",
                valor_actual=actual.cantidad_minima,
            )
            total = input_entero(
                f"Cantidad total [{actual.cantidad_total}]: ",
                valor_actual=actual.cantidad_total,
            )
            actual.cantidad_minima = minima
            actual.cantidad_total = total
            self.servicio.guardar_stock(actual)
            print("Stock modificado correctamente.")
        except (ValueError, TypeError) as error:
            print(f"No se pudo modificar el stock: {error}")

    def baja_stock(self):
        print("\n--- BAJA DE STOCK ---")
        try:
            libro = self._pedir_libro()
            stock = self.servicio.leer_stock_por_libro(libro.id)
            if stock is None:
                print("No hay stock registrado para ese libro.")
                return
            self._mostrar_stock(libro, stock)
            confirmacion = input(
                f"¿Eliminar el stock de '{libro.titulo}'? [s/N]: "
            ).strip().lower()
            if confirmacion not in ("s", "si", "sí"):
                print("Baja cancelada.")
                return
            if self.servicio.eliminar_stock_por_libro(libro.id):
                print("Stock eliminado correctamente.")
            else:
                print("No se encontró el stock.")
        except (ValueError, TypeError) as error:
            print(f"No se pudo eliminar el stock: {error}")

    def buscar_stock_por_libro(self):
        print("\n--- BÚSQUEDA DE STOCK POR LIBRO ---")
        try:
            libro = self._pedir_libro()
            stock = self.servicio.leer_stock_por_libro(libro.id)
            if stock is None:
                print("No hay stock registrado para ese libro.")
                return
            self._mostrar_stock(libro, stock)
        except (ValueError, TypeError) as error:
            print(f"No se pudo encontrar el stock: {error}")

    def alta_precio(self):
        print("\n--- ALTA DE PRECIO ---")
        try:
            libro = self._pedir_libro()
           
            precio = Precio(
                libro_id=libro.id,
                moneda=self._pedir_moneda(),
                precio_base=input_decimal("Precio base: "),
            )
            self.servicio.guardar_precio(precio)
            print("Precio creado correctamente.")
        except (ValueError, TypeError) as error:
            print(f"No se pudo crear el precio: {error}")

    def modificacion_precio(self):
        print("\n--- MODIFICACIÓN DE PRECIO ---")
        try:
            libro = self._pedir_libro()
            actual = self._seleccionar_precio(libro)
            if actual is None:
                return
            self._mostrar_precio(libro, actual)
            print("Presione Enter para conservar el valor actual.")
            precio_base = input_decimal(
                f"Precio base [{actual.precio_base}]: ",
                valor_actual=actual.precio_base,
            )
           
            actual.precio_base = precio_base
            self.servicio.guardar_precio(actual)
            print("Precio modificado correctamente.")
        except (ValueError, TypeError) as error:
            print(f"No se pudo modificar el precio: {error}")

    def baja_precio(self):
        print("\n--- BAJA DE PRECIO ---")
        try:
            libro = self._pedir_libro()
            precio = self._seleccionar_precio(libro)
            if precio is None:
                return
            self._mostrar_precio(libro, precio)
            confirmacion = input(
                f"¿Eliminar el precio de '{libro.titulo}' en "
                f"{precio.moneda.codigo_iso} por {precio.precio_base}? [s/N]: "
            ).strip().lower()
            if confirmacion not in ("s", "si", "sí"):
                print("Baja cancelada.")
                return
            if self.servicio.eliminar_precio_por_libro_y_moneda(libro.id, precio.moneda.id):
                print("Precio eliminado correctamente.")
            else:
                print("No se encontró el precio.")
        except (ValueError, TypeError) as error:
            print(f"No se pudo eliminar el precio: {error}")

    def _seleccionar_precio(self, libro):
        """Muestra los precios registrados y selecciona uno por ID de moneda."""
        precios = self.servicio.leer_precios_por_libro(libro.id)
        if not precios:
            print("Sin precios registrados.")
            return None
        for precio in precios:
            print(f"Moneda {precio.moneda.id}: {precio.moneda.codigo_iso} {precio.precio_base}")
        moneda_id = input_entero("ID de moneda del precio: ")
        for precio in precios:
            if precio.moneda.id == moneda_id:
                return precio
        raise ValueError("El libro no tiene un precio registrado en esa moneda.")

    def buscar_precios_por_libro(self):
        print("\n--- BÚSQUEDA DE PRECIOS POR LIBRO ---")
        try:
            libro = self._pedir_libro()
            precios = self.servicio.leer_precios_por_libro(libro.id)
            if not precios:
                print("Sin precios registrados.")
                return
            self._mostrar_precios(libro, precios)
        except (ValueError, TypeError) as error:
            print(f"No se pudo buscar el precio: {error}")


class ControladorCatalogo:
    """Gestiona por consola el alta, modificación, baja, listado y búsqueda de libros por ID."""

    def __init__(self, servicio: ServicioCatalogo,
                 servicio_editorial: ServicioEditorial,
                 servicio_genero: ServicioGenero):
        self.servicio = servicio
        self.servicio_editorial = servicio_editorial
        self.servicio_genero = servicio_genero

    def ejecutar(self):
        opciones = {
            "1": ("Listado", self.listar),
            "2": ("Alta", self.alta),
            "3": ("Modificación", self.modificacion),
            "4": ("Baja", self.baja),
            "5": ("Buscar libro por ID", self.buscar),
            "6": ("Volver atrás", None),
        }
        while True:
            limpiar_pantalla()
            opcion = mostrar_menu("GESTIÓN DE CATÁLOGO", opciones)
            limpiar_pantalla()
            if opcion not in opciones:
                print("Opción inválida.")
            else:
                _, accion = opciones[opcion]
                if accion is None:
                    return
                accion()
            input("\nPresione Enter para continuar...")

    @staticmethod
    def _mostrar(libros):
        mostrar_separador()
        print("ID", "ISBN", "Título", "Autor", "Peso (g)", "Dimensiones",
              "Páginas", "Fecha de publicación", "Idioma", "Editorial",
              "Género", "Stock Total", sep=" | ")
        mostrar_separador()
        for libro in libros:
            print(f"{libro.id}", 
                  f"{libro.isbn}", 
                  f"{libro.titulo}", 
                  f"{libro.autor}", 
                  f"{libro.peso}",
                  f"{libro.dimensiones}", 
                  f"{libro.numero_paginas}", 
                  f"{libro.fecha_publicacion}",
                  f"{libro.idioma}", 
                  f"{libro.editorial.nombre}", 
                  f"{libro.genero.nombre}",
                  f"{libro.stock.cantidad_total}" if libro.stock else "Sin Stock",
                  sep=" | ")

    def alta(self):
        print("\n--- ALTA DE LIBRO ---")
        try:
            isbn = input("ISBN: ").strip()
            titulo = input("Título: ").strip()
            autor = input("Autor: ").strip()
            peso = input_decimal("Peso (g): ")
            dimensiones = input("Dimensiones: ").strip()
            numero_paginas = input_entero("Páginas: ")
            fecha_publicacion = date.fromisoformat(
                input_fecha("Fecha de publicación (AAAA-MM-DD): ")
            )
            idioma = input("Idioma: ").strip()

            editorial_id = input_entero("ID de editorial: ")
            editorial = self.servicio_editorial.leer_por_id(editorial_id)
            if editorial is None:
                raise ValueError("No existe esa editorial.")

            genero_id = input_entero("ID de género: ")
            genero = self.servicio_genero.leer_por_id(genero_id)
            if genero is None:
                raise ValueError("No existe ese género.")

            libro = Libro(
                isbn=isbn,
                titulo=titulo,
                autor=autor,
                peso=peso,
                dimensiones=dimensiones,
                numero_paginas=numero_paginas,
                fecha_publicacion=fecha_publicacion,
                idioma=idioma,
                editorial=editorial,
                genero=genero,
            )
            creado = self.servicio.guardar(libro)
            print(f"Libro creado correctamente. ID: {creado.id}")
        except (ValueError, TypeError) as error:
            print(f"No se pudo crear el libro: {error}")

    def modificacion(self):
        print("\n--- MODIFICACIÓN DE LIBRO ---")

        try:
            libro_id = input_entero("ID de libro: ")
            actual = self.servicio.leer_por_id(libro_id)

            if actual is None:
                print("No existe ese libro.")
                return

            self._mostrar([actual])
            print("Presione Enter para conservar el valor actual.")

            isbn = input(f"ISBN [{actual.isbn}]: ").strip() or actual.isbn
            titulo = input(f"Título [{actual.titulo}]: ").strip() or actual.titulo
            autor = input(f"Autor [{actual.autor}]: ").strip() or actual.autor
            peso = input_decimal(
                f"Peso (g) [{actual.peso}]: ",
                valor_actual=actual.peso,
            )
            dimensiones = input(
                f"Dimensiones [{actual.dimensiones}]: "
            ).strip() or actual.dimensiones
            numero_paginas = input_entero(
                f"Páginas [{actual.numero_paginas}]: ",
                valor_actual=actual.numero_paginas,
            )
            fecha_publicacion = date.fromisoformat(input_fecha(
                f"Fecha de publicación [{actual.fecha_publicacion}] "
                "(AAAA-MM-DD): ",
                valor_actual=actual.fecha_publicacion,
            ))
            idioma = input(f"Idioma [{actual.idioma}]: ").strip() or actual.idioma

            editorial_id = input_entero(
                f"ID de editorial [{actual.editorial.id}]: ",
                valor_actual=actual.editorial.id,
            )
            editorial = self.servicio_editorial.leer_por_id(editorial_id)
            if editorial is None:
                raise ValueError("No existe esa editorial.")

            genero_id = input_entero(
                f"ID de género [{actual.genero.id}]: ",
                valor_actual=actual.genero.id,
            )
            genero = self.servicio_genero.leer_por_id(genero_id)
            if genero is None:
                raise ValueError("No existe ese género.")

            actual.isbn = isbn
            actual.titulo = titulo
            actual.autor = autor
            actual.peso = peso
            actual.dimensiones = dimensiones
            actual.numero_paginas = numero_paginas
            actual.fecha_publicacion = fecha_publicacion
            actual.idioma = idioma
            actual.editorial = editorial
            actual.genero = genero

            self.servicio.guardar(actual)
            print("Libro modificado correctamente.")

        except (ValueError, TypeError) as error:
            print(f"No se pudo modificar el libro: {error}")

    def baja(self):
        print("\n--- BAJA DE LIBRO ---")
        try:
            libro_id = input_entero("ID de libro: ")
            libro = self.servicio.leer_por_id(libro_id)
            if libro is None:
                print("No existe ese libro.")
                return
            self._mostrar([libro])
            confirmacion = input(
                f"¿Eliminar el libro '{libro.titulo}'? [s/N]: "
            ).strip().lower()
            if confirmacion not in ("s", "si", "sí"):
                print("Baja cancelada.")
                return
            if self.servicio.eliminar(libro_id):
                print("Libro eliminado correctamente.")
            else:
                print("No se encontró el libro.")
        except (ValueError, TypeError) as error:
            print(f"No se pudo eliminar el libro: {error}")

    def listar(self):
        print("\n--- LISTADO DE LIBROS ---")
        libros = self.servicio.listar_todos()
        if not libros:
            print("No hay libros registrados.")
            return
        self._mostrar(libros)

    def buscar(self):
        print("\n--- BÚSQUEDA DE LIBRO POR ID ---")
        try:
            libro = self.servicio.leer_por_id(input_entero("ID de libro: "))
            if libro is None:
                print("No existe ese libro.")
                return
            self._mostrar([libro])
        except (ValueError, TypeError) as error:
            print(f"No se pudo buscar el libro: {error}")


class ControladorCotizacion:
    """Gestiona por consola las cotizaciones y su histórico por tipo y monedas."""

    def __init__(self, servicio: ServicioCotizacion,
                 servicio_moneda: ServicoMoneda,
                 servicio_tipo_cotizacion: ServicioTipoCotizacion):
        self.servicio = servicio
        self.servicio_moneda = servicio_moneda
        self.servicio_tipo_cotizacion = servicio_tipo_cotizacion

    def _pedir_clave(self):
        """Solicita y valida el tipo, las monedas y la fecha de una cotización.

        Returns:
            Tupla con los IDs de tipo, moneda origen y moneda destino, y la fecha.

        Raises:
            ValueError: Si el tipo o alguna de las monedas no existe.
        """
        tipo_id = input_entero("ID de tipo de cotización: ")
        tipo = self.servicio_tipo_cotizacion.leer_por_id(tipo_id)
        if tipo is None:
            raise ValueError("No existe ese tipo de cotización.")

        origen_id = input_entero("ID de moneda de origen: ")
        origen = self.servicio_moneda.leer_por_id(origen_id)
        if origen is None:
            raise ValueError("No existe esa moneda de origen.")

        destino_id = input_entero("ID de moneda de destino: ")
        destino = self.servicio_moneda.leer_por_id(destino_id)
        if destino is None:
            raise ValueError("No existe esa moneda de destino.")

        fecha = date.fromisoformat(input_fecha("Fecha (AAAA-MM-DD): "))
        return tipo.id, origen.id, destino.id, fecha

    def ejecutar(self):
        opciones = {
            "1": ("Alta", self.alta),
            "2": ("Modificación", self.modificacion),
            "3": ("Baja", self.baja),
            "4": ("Búsqueda de cotización", self.buscar),
            "5": ("Ver Listado Histórico", self.listar_historico),
            "6": ("Obtener Cotizaciones por API", self.obtener_cotizaciones),
            "7": ("Volver atrás", None),
        }

        while True:
            limpiar_pantalla()
            opcion = mostrar_menu("GESTIÓN DE COTIZACIONES", opciones)
            limpiar_pantalla()

            if opcion not in opciones:
                print("Opción inválida.")
            else:
                _, accion = opciones[opcion]
                if accion is None:
                    return
                accion()

            input("\nPresione Enter para continuar...")

    @staticmethod
    def _mostrar(cotizaciones):
        mostrar_separador()
        print("Moneda origen", "Moneda destino", "Tipo de cotización", "Fecha", "Valor", sep=" | ")
        mostrar_separador()
        for cotizacion in cotizaciones:
            print(
                cotizacion.moneda_origen.codigo_iso,
                cotizacion.moneda_destino.codigo_iso,
                cotizacion.tipo_cotizacion.nombre,
                cotizacion.fecha,
                f"{cotizacion.valor:.2f}",
                sep=" | ",
            )

    def alta(self):
        print("\n--- ALTA DE COTIZACIÓN ---")
        try:
            tipo_id = input_entero("ID de tipo de cotización: ")
            tipo = self.servicio_tipo_cotizacion.leer_por_id(tipo_id)
            if tipo is None:
                raise ValueError("No existe ese tipo de cotización.")

            origen_id = input_entero("ID de moneda de origen: ")
            origen = self.servicio_moneda.leer_por_id(origen_id)
            if origen is None:
                raise ValueError("No existe esa moneda de origen.")

            destino_id = input_entero("ID de moneda de destino: ")
            destino = self.servicio_moneda.leer_por_id(destino_id)
            if destino is None:
                raise ValueError("No existe esa moneda de destino.")

            fecha = date.fromisoformat(input_fecha("Fecha (AAAA-MM-DD): "))

            cotizacion = Cotizacion(
                moneda_origen=origen,
                moneda_destino=destino,
                tipo_cotizacion=tipo,
                valor=input_decimal("Valor (use punto para decimales): "),
                fecha=fecha,
            )
            self.servicio.guardar(cotizacion)
            print("Cotización creada correctamente.")
        except (ValueError, TypeError) as error:
            print(f"No se pudo crear la cotización: {error}")

    def modificacion(self):
        print("\n--- MODIFICACIÓN DE COTIZACIÓN ---")
        try:
            tipo_id = input_entero("ID de tipo de cotización: ")
            tipo = self.servicio_tipo_cotizacion.leer_por_id(tipo_id)
            if tipo is None:
                raise ValueError("No existe ese tipo de cotización.")

            origen_id = input_entero("ID de moneda de origen: ")
            origen = self.servicio_moneda.leer_por_id(origen_id)
            if origen is None:
                raise ValueError("No existe esa moneda de origen.")

            destino_id = input_entero("ID de moneda de destino: ")
            destino = self.servicio_moneda.leer_por_id(destino_id)
            if destino is None:
                raise ValueError("No existe esa moneda de destino.")

            fecha = date.fromisoformat(input_fecha("Fecha (AAAA-MM-DD): "))
            actual = self.servicio.leer_por_tipo_moneda_origen_destino_y_fecha(
                tipo.id, origen.id, destino.id, fecha
            )
            if actual is None:
                print("No existe esa cotización.")
                return
            
            actual.valor = input_decimal(
                f"Valor [{actual.valor}] (Enter para conservar): ",
                valor_actual=actual.valor,
            )
            self.servicio.guardar(actual)
            print("Cotización modificada correctamente.")
        except (ValueError, TypeError) as error:
            print(f"No se pudo modificar la cotización: {error}")

    def baja(self):
        print("\n--- BAJA DE COTIZACIÓN ---")
        try:
            clave = self._pedir_clave()
            actual = self.servicio.leer_por_tipo_moneda_origen_destino_y_fecha(*clave)
            if actual is None:
                print("No existe esa cotización.")
                return

            self._mostrar([actual])
            confirmacion = input("¿Eliminar esta cotización? [s/N]: ").strip().lower()
            if confirmacion not in ("s", "si", "sí"):
                print("Baja cancelada.")
                return

            if self.servicio.eliminar(*clave):
                print("Cotización eliminada correctamente.")
            else:
                print("No se encontró la cotización.")
        except (ValueError, TypeError) as error:
            print(f"No se pudo eliminar la cotización: {error}")

    def buscar(self):
        print("\n--- BÚSQUEDA DE COTIZACIÓN ---")
        try:
            clave = self._pedir_clave()
            cotizacion = self.servicio.leer_por_tipo_moneda_origen_destino_y_fecha(*clave)
            if cotizacion is None:
                print("No existe esa cotización.")
                return
            self._mostrar([cotizacion])
        except (ValueError, TypeError) as error:
            print(f"No se pudo buscar la cotización: {error}")

    def obtener_cotizaciones(self):
        """Descarga y registra las cotizaciones de la API y muestra su listado."""
        print("\n--- OBTENER COTIZACIONES POR API ---")
        try:
            cotizaciones = self.servicio.obtener_cotizaciones()
            if not cotizaciones:
                print("No se obtuvieron cotizaciones.")
                return

            self._mostrar(cotizaciones)
            print(f"Cotizaciones registradas: {len(cotizaciones)}")
        except (ValueError, TypeError, RuntimeError, SQLAlchemyError) as error:
            print(f"No se pudieron obtener las cotizaciones: {error}")

    def listar_historico(self):
        print("\n--- LISTADO HISTÓRICO DE COTIZACIONES ---")
        try:
            tipo_id = input_entero("ID de tipo de cotización: ")
            origen_id = input_entero("ID de moneda de origen: ")
            destino_id = input_entero("ID de moneda de destino: ")
            cotizaciones = self.servicio.leer_historico_por_tipo_moneda_origen_moneda_destino(
                tipo_id, origen_id, destino_id
            )
            if not cotizaciones:
                print("No hay cotizaciones para el tipo y las monedas seleccionadas.")
                return
            self._mostrar(sorted(cotizaciones, key=lambda cotizacion: cotizacion.fecha))
        except (ValueError, TypeError) as error:
            print(f"No se pudo listar el histórico: {error}")


class ControladorTipoCotizacion:
    """Gestiona por consola el alta, modificación, baja y listado de tipos de cotización."""

    def __init__(self, servicio: ServicioTipoCotizacion):
        self.servicio = servicio

    def ejecutar(self):
        opciones = {
            "1": ("Listado", self.listar),
            "2": ("Alta", self.alta),
            "3": ("Modificación", self.modificacion),
            "4": ("Baja", self.baja),
            "5": ("Volver atrás", None),
        }

        while True:
            limpiar_pantalla()
            opcion = mostrar_menu("GESTIÓN DE TIPOS DE COTIZACIÓN", opciones)
            limpiar_pantalla()

            if opcion not in opciones:
                print("Opción inválida.")
            else:
                _, accion = opciones[opcion]
                if accion is None:
                    return
                accion()

            input("\nPresione Enter para continuar...")

    def listar(self):
        tipos = self.servicio.leer_todos()

        if not tipos:
            print("No hay tipos de cotización registrados.")
            return

        print("\n--- LISTADO DE TIPOS DE COTIZACIÓN ---")
        mostrar_separador()
        print("ID", "Nombre", "Descripción", sep=" | ")
        mostrar_separador()

        for tipo in tipos:
            print(tipo.id, tipo.nombre, tipo.descripcion, sep=" | ")

    def alta(self):
        print("\n--- ALTA DE TIPO DE COTIZACIÓN ---")

        try:
            tipo = TipoCotizacion(
                nombre=input("Nombre: ").strip(),
                descripcion=input("Descripción: ").strip(),
            )
            creado = self.servicio.guardar(tipo)
            print(f"Tipo de cotización creado correctamente. ID: {creado.id}")
        except ValueError as error:
            print(f"No se pudo crear el tipo de cotización: {error}")

    def modificacion(self):
        print("\n--- MODIFICACIÓN DE TIPO DE COTIZACIÓN ---")

        try:
            tipo_id = input_entero("ID de tipo de cotización: ")
            actual = self.servicio.leer_por_id(tipo_id)

            if actual is None:
                print("No existe ese tipo de cotización.")
                return

            print("Presione Enter para conservar el valor actual.")
            valores_anteriores = (actual.nombre, actual.descripcion)
            actual.nombre = input(
                f"Nombre [{actual.nombre}]: "
            ).strip() or actual.nombre
            actual.descripcion = input(
                f"Descripción [{actual.descripcion}]: "
            ).strip() or actual.descripcion

            self.servicio.guardar(actual)
            print("Tipo de cotización modificado correctamente.")
        except ValueError as error:
            print(f"No se pudo modificar el tipo de cotización: {error}")

    def baja(self):
        print("\n--- BAJA DE TIPO DE COTIZACIÓN ---")

        try:
            tipo_id = input_entero("ID de tipo de cotización: ")
            tipo = self.servicio.leer_por_id(tipo_id)

            if tipo is None:
                print("No existe ese tipo de cotización.")
                return

            confirmacion = input(
                f"¿Eliminar el tipo de cotización '{tipo.nombre}'? [s/N]: "
            ).strip().lower()

            if confirmacion not in ("s", "si", "sí"):
                print("Baja cancelada.")
                return

            if self.servicio.eliminar(tipo_id):
                print("Tipo de cotización eliminado correctamente.")
            else:
                print("No se encontró el tipo de cotización.")
        except ValueError as error:
            print(f"No se pudo eliminar el tipo de cotización: {error}")


class ControladorMoneda:
    """Gestiona por consola el alta, modificación, baja y listado de monedas."""

    def __init__(self, servicio: ServicoMoneda):
        self.servicio = servicio

    def ejecutar(self):
        opciones = {
            "1": ("Listado", self.listar),
            "2": ("Alta", self.alta),
            "3": ("Modificación", self.modificacion),
            "4": ("Baja", self.baja),
            "5": ("Volver atrás", None),
        }

        while True:
            limpiar_pantalla()
            opcion = mostrar_menu("GESTIÓN DE MONEDAS", opciones)
            limpiar_pantalla()

            if opcion not in opciones:
                print("Opción inválida.")
            else:
                _, accion = opciones[opcion]
                if accion is None:
                    return
                accion()

            input("\nPresione Enter para continuar...")

    def listar(self):
        monedas = self.servicio.leer_todos()

        if not monedas:
            print("No hay monedas registradas.")
            return

        print("\n--- LISTADO DE MONEDAS ---")
        mostrar_separador()
        print("ID", "Código ISO", "Nombre", "Símbolo", sep=" | ")
        mostrar_separador()

        for moneda in monedas:
            print(
                moneda.id,
                moneda.codigo_iso,
                moneda.nombre,
                moneda.simbolo,
                sep=" | ",
            )

    def alta(self):
        print("\n--- ALTA DE MONEDA ---")

        try:
            moneda = Moneda(
                codigo_iso=input("Código ISO: ").strip(),
                nombre=input("Nombre: ").strip(),
                simbolo=input("Símbolo: ").strip(),
            )
            creada = self.servicio.guardar(moneda)
            print(f"Moneda creada correctamente. ID: {creada.id}")
        except ValueError as error:
            print(f"No se pudo crear la moneda: {error}")

    def modificacion(self):
        print("\n--- MODIFICACIÓN DE MONEDA ---")

        try:
            moneda_id = input_entero("ID de moneda: ")
            actual = self.servicio.leer_por_id(moneda_id)

            if actual is None:
                print("No existe esa moneda.")
                return

            print("Presione Enter para conservar el valor actual.")
            actual.codigo_iso = input(
                f"Código ISO [{actual.codigo_iso}]: "
            ).strip() or actual.codigo_iso
            actual.nombre = input(
                f"Nombre [{actual.nombre}]: "
            ).strip() or actual.nombre
            actual.simbolo = input(
                f"Símbolo [{actual.simbolo}]: "
            ).strip() or actual.simbolo

            self.servicio.guardar(actual)
            print("Moneda modificada correctamente.")
        except ValueError as error:
            print(f"No se pudo modificar la moneda: {error}")

    def baja(self):
        print("\n--- BAJA DE MONEDA ---")

        try:
            moneda_id = input_entero("ID de moneda: ")
            moneda = self.servicio.leer_por_id(moneda_id)

            if moneda is None:
                print("No existe esa moneda.")
                return

            confirmacion = input(
                f"¿Eliminar la moneda '{moneda.nombre}'? [s/N]: "
            ).strip().lower()

            if confirmacion not in ("s", "si", "sí"):
                print("Baja cancelada.")
                return

            if self.servicio.eliminar(moneda_id):
                print("Moneda eliminada correctamente.")
            else:
                print("No se encontró la moneda.")
        except ValueError as error:
            print(f"No se pudo eliminar la moneda: {error}")


class ControladorGenero:
    """Gestiona por consola el alta, modificación, baja y listado de géneros literarios."""

    def __init__(self, servicio: ServicioGenero):
        self.servicio = servicio

    def ejecutar(self):
        opciones = {
            "1": ("Listado", self.listar),
            "2": ("Alta", self.alta),
            "3": ("Modificación", self.modificacion),
            "4": ("Baja", self.baja),
            "5": ("Volver atrás", None),
        }

        while True:
            limpiar_pantalla()
            opcion = mostrar_menu("GESTIÓN DE GÉNEROS", opciones)
            limpiar_pantalla()

            if opcion not in opciones:
                print("Opción inválida.")
            else:
                _, accion = opciones[opcion]
                if accion is None:
                    return
                accion()

            input("\nPresione Enter para continuar...")

    def listar(self):
        generos = self.servicio.leer_todos()

        if not generos:
            print("No hay géneros registrados.")
            return

        print("\n--- LISTADO DE GÉNEROS ---")
        mostrar_separador()
        print("ID", "Nombre", "Descripción", sep=" | ")
        mostrar_separador()

        for genero in generos:
            print(genero.id, genero.nombre, genero.descripcion, sep=" | ")

    def alta(self):
        print("\n--- ALTA DE GÉNERO ---")

        try:
            genero = Genero(
                nombre=input("Nombre: ").strip(),
                descripcion=input("Descripción: ").strip(),
            )
            creado = self.servicio.guardar(genero)
            print(f"Género creado correctamente. ID: {creado.id}")
        except ValueError as error:
            print(f"No se pudo crear el género: {error}")

    def modificacion(self):
        print("\n--- MODIFICACIÓN DE GÉNERO ---")

        actual = None
        try:
            genero_id = input_entero("ID de género: ")
            actual = self.servicio.leer_por_id(genero_id)

            if actual is None:
                print("No existe ese género.")
                return

            print("Presione Enter para conservar el valor actual.")
       
            actual.nombre = input(
                f"Nombre [{actual.nombre}]: "
            ).strip() or actual.nombre
            actual.descripcion = input(
                f"Descripción [{actual.descripcion}]: "
            ).strip() or actual.descripcion

            self.servicio.guardar(actual)
            print("Género modificado correctamente.")
        except ValueError as error:
            print(f"No se pudo modificar el género: {error}")

    def baja(self):
        print("\n--- BAJA DE GÉNERO ---")

        try:
            genero_id = input_entero("ID de género: ")
            genero = self.servicio.leer_por_id(genero_id)

            if genero is None:
                print("No existe ese género.")
                return

            confirmacion = input(
                f"¿Eliminar el género '{genero.nombre}'? [s/N]: "
            ).strip().lower()

            if confirmacion not in ("s", "si", "sí"):
                print("Baja cancelada.")
                return

            if self.servicio.eliminar(genero_id):
                print("Género eliminado correctamente.")
            else:
                print("No se encontró el género.")
        except ValueError as error:
            print(f"No se pudo eliminar el género: {error}")


class ControladorEditorial:
    """Gestiona por consola el alta, modificación, baja y listado de editoriales."""

    def __init__(self, servicio: ServicioEditorial):
        self.servicio = servicio

    def ejecutar(self):
        opciones = {
        "1": ("Listado", self.listar),
        "2": ("Alta", self.alta),
        "3": ("Modificación", self.modificacion),
        "4": ("Baja", self.baja),
        "5": ("Volver atrás", None),
    }

        while True:
            limpiar_pantalla()
            opcion = mostrar_menu("GESTIÓN DE EDITORIALES", opciones)
            limpiar_pantalla()

            if opcion not in opciones:
                print("Opción inválida.")
            else:
                _, accion = opciones[opcion]

                if accion is None:
                    return

                accion()

            input("\nPresione Enter para continuar...")

    def listar(self):
        editoriales = self.servicio.leer_todos()

        if not editoriales:
            print("No hay editoriales registradas.")
            return

        print("\n--- LISTADO DE EDITORIALES ---")
        mostrar_separador()
        print(
            "ID",
            "Nombre",
            "Grupo",
            "País de origen",
            "Teléfono",
            "Email",
            sep=" | ",
        )
        mostrar_separador()

        for editorial in editoriales:
            print(
                editorial.id,
                editorial.nombre,
                editorial.grupo,
                editorial.pais_origen,
                editorial.telefono,
                editorial.email,
            sep=" | ",
        )

    def alta(self):
        print("\n--- ALTA DE EDITORIAL ---")

        try:
            editorial = Editorial(
                nombre=input("Nombre: ").strip(),
                grupo=input("Grupo: ").strip(),
                pais_origen=input("País de origen: ").strip(),
                telefono=input("Teléfono: ").strip(),
                email=input("Email: ").strip(),
            )

            creada = self.servicio.guardar(editorial)

            print(f"Editorial creada correctamente. ID: {creada.id}")

        except ValueError as error:
            print(f"No se pudo crear la editorial: {error}")

    def modificacion(self):
        print("\n--- MODIFICACIÓN DE EDITORIAL ---")

        try:
            editorial_id = input_entero("ID de editorial: ")
            actual = self.servicio.leer_por_id(editorial_id)

            if actual is None:
                print("No existe esa editorial.")
                return

            print("Presione Enter para conservar el valor actual.")

            actual.nombre = input(
                f"Nombre [{actual.nombre}]: ").strip() or actual.nombre

            actual.grupo = input(
                 f"Grupo [{actual.grupo}]: ").strip() or actual.grupo

            actual.pais_origen = input(
                f"País de origen [{actual.pais_origen}]: ").strip() or actual.pais_origen

            actual.telefono = input(
                f"Teléfono [{actual.telefono}]: ").strip() or actual.telefono

            actual.email = input(
                f"Email [{actual.email}]: ").strip() or actual.email

            self.servicio.guardar(actual)
            print("Editorial modificada correctamente.")

        except ValueError as error:
            print(f"No se pudo modificar la editorial: {error}")

    def baja(self):
        print("\n--- BAJA DE EDITORIAL ---")

        try:
            editorial_id = input_entero("ID de editorial: ")
            editorial = self.servicio.leer_por_id(editorial_id)

            if editorial is None:
                print("No existe esa editorial.")
                return

            confirmacion = input(
                f"¿Eliminar la editorial '{editorial.nombre}'? [s/N]: "
            ).strip().lower()

            if confirmacion not in ("s", "si", "sí"):
                print("Baja cancelada.")
                return

            if self.servicio.eliminar(editorial_id):
                print("Editorial eliminada correctamente.")
            else:
                print("No se encontró la editorial.")

        except ValueError as error:
            print(f"No se pudo eliminar la editorial: {error}")


    
