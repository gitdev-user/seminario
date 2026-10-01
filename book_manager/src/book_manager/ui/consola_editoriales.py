from pydantic import ValidationError

from entities.editorial import Editorial
from services.servicio_editorial import ServicioEditorial
from ui.consola import ConsolaOperaciones


class ConsolaEditoriales(ConsolaOperaciones):
    CAMPOS = (
        ("nombre", "Nombre"),
        ("grupo", "Grupo"),
        ("pais_origen", "País de origen"),
        ("telefono", "Teléfono"),
        ("email", "Correo electrónico"),
    )

    def __init__(self, acciones=None, servicio: ServicioEditorial | None = None):
        self.servicio = servicio
        operaciones = [
            ("alta", "Alta"), ("modificacion", "Modificación"),
            ("baja", "Baja"), ("listado", "Ver Listado"),
            ("buscar", "Buscar Editorial"),
        ]
        manejadores = {}
        if servicio is not None:
            manejadores = {
                clave: self._manejar_errores(getattr(self, clave))
                for clave, _ in operaciones
            }
        if acciones is not None:
            manejadores.update(acciones)
        super().__init__("Gestión de Editoriales", operaciones, manejadores)

    @staticmethod
    def _manejar_errores(accion):
        def ejecutar():
            try:
                accion()
            except ValidationError as error:
                print("Datos inválidos:")
                for detalle in error.errors():
                    campo = ".".join(str(parte) for parte in detalle["loc"])
                    print(f"- {campo}: {detalle['msg']}")
            except (ValueError, OSError) as error:
                print(f"No se pudo completar la operación: {error}")
        return ejecutar

    @staticmethod
    def _pedir_id() -> int:
        while True:
            try:
                return int(input("ID de editorial: ").strip())
            except ValueError:
                print("Ingrese un número entero para el ID.")

    def _pedir_datos(self, id: int, actual: Editorial | None = None) -> Editorial:
        datos = {"id": id}
        if actual is not None:
            datos = actual.model_dump()
            print("Presione Enter para conservar cada valor actual.")
        for campo, etiqueta in self.CAMPOS:
            valor_actual = getattr(actual, campo) if actual is not None else None
            indicacion = f" [{valor_actual}]" if actual is not None else ""
            valor = input(f"{etiqueta}{indicacion}: ").strip()
            datos[campo] = valor_actual if actual is not None and not valor else valor
        return Editorial.model_validate(datos)

    @classmethod
    def _mostrar(cls, editorial: Editorial) -> None:
        print(f"\nID: {editorial.id}")
        for campo, etiqueta in cls.CAMPOS:
            print(f"{etiqueta}: {getattr(editorial, campo)}")

    @classmethod
    def _mostrar_listado(cls, editoriales: list[Editorial]) -> None:
        columnas = (("id", "ID"),) + cls.CAMPOS
        encabezados = [etiqueta for _, etiqueta in columnas]
        filas = [
            [" ".join(str(getattr(editorial, campo)).split()) for campo, _ in columnas]
            for editorial in editoriales
        ]
        anchos = [
            max(len(encabezado), max((len(fila[i]) for fila in filas), default=0))
            for i, encabezado in enumerate(encabezados)
        ]
        print()
        print(" | ".join(texto.ljust(ancho) for texto, ancho in zip(encabezados, anchos)))
        print("-+-".join("-" * ancho for ancho in anchos))
        for fila in filas:
            print(" | ".join(texto.ljust(ancho) for texto, ancho in zip(fila, anchos)))

    def alta(self) -> None:
        creada = self.servicio.guardar(self._pedir_datos(0))
        print(f"Editorial creada exitosamente. ID asignado: {creada.id}.")

    def modificacion(self) -> None:
        id = self._pedir_id()
        actual = self.servicio.leer_por_id(id)
        if actual is None:
            print("No se encontró la editorial.")
            return
        self._mostrar_listado([actual])
        self.servicio.guardar(self._pedir_datos(id, actual))
        print("Editorial modificada exitosamente.")

    def baja(self) -> None:
        id = self._pedir_id()
        actual = self.servicio.leer_por_id(id)
        if actual is None:
            print("No se encontró la editorial.")
            return
        self._mostrar(actual)
        if input("¿Confirma la baja? [s/N]: ").strip().lower() not in ("s", "si", "sí"):
            print("Baja cancelada.")
            return
        if self.servicio.eliminar(id):
            print("Editorial eliminada exitosamente.")
        else:
            print("No se encontró la editorial.")

    def listado(self) -> None:
        editoriales = self.servicio.leer_todos()
        if not editoriales:
            print("No hay editoriales registradas.")
            return
        self._mostrar_listado(editoriales)

    def buscar(self) -> None:
        editorial = self.servicio.leer_por_id(self._pedir_id())
        if editorial is None:
            print("No se encontró la editorial.")
            return
        self._mostrar_listado([editorial])
