from pydantic import BaseModel, ValidationError
from ui.consola import ConsolaOperaciones


class ConsolaEntidad(ConsolaOperaciones):
    MODELO: type[BaseModel]
    TITULO: str
    NOMBRE: str
    CAMPOS: tuple

    def __init__(self, acciones=None, servicio=None):
        self.servicio = servicio
        operaciones = [
            ("alta", "Alta"), ("modificacion", "Modificación"),
            ("baja", "Baja"), ("listado", "Ver Listado"),
            ("buscar", f"Buscar {self.NOMBRE}"),
        ]
        manejadores = {}
        if servicio is not None:
            manejadores = {
                clave: self._manejar_errores(getattr(self, clave))
                for clave, _ in operaciones
            }
        if acciones is not None:
            manejadores.update(acciones)
        super().__init__(self.TITULO, operaciones, manejadores)

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

    @classmethod
    def _pedir_id(cls) -> int:
        while True:
            try:
                return int(input(f"ID de {cls.NOMBRE.lower()}: ").strip())
            except ValueError:
                print("Ingrese un número entero para el ID.")

    def _pedir_datos(self, id: int, actual: BaseModel | None = None) -> BaseModel:
        datos = {"id": id}
        if actual is not None:
            datos = actual.model_dump()
            print("Presione Enter para conservar cada valor actual.")
        for campo, etiqueta in self.CAMPOS:
            valor_actual = getattr(actual, campo) if actual is not None else None
            indicacion = f" [{valor_actual}]" if actual is not None else ""
            valor = input(f"{etiqueta}{indicacion}: ").strip()
            datos[campo] = valor_actual if actual is not None and not valor else valor
        return self.MODELO.model_validate(datos)

    @classmethod
    def _mostrar(cls, entidad: BaseModel) -> None:
        print(f"\nID: {entidad.id}")
        for campo, etiqueta in cls.CAMPOS:
            print(f"{etiqueta}: {getattr(entidad, campo)}")

    @classmethod
    def _mostrar_listado(cls, entidades: list[BaseModel]) -> None:
        columnas = (("id", "ID"),) + cls.CAMPOS
        encabezados = [etiqueta for _, etiqueta in columnas]
        filas = [
            [" ".join(str(getattr(entidad, campo)).split()) for campo, _ in columnas]
            for entidad in entidades
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
        print(f"Alta realizada exitosamente. ID asignado: {creada.id}.")

    def modificacion(self) -> None:
        id = self._pedir_id()
        actual = self.servicio.leer_por_id(id)
        if actual is None:
            print("No se encontró el registro.")
            return
        self._mostrar_listado([actual])
        self.servicio.guardar(self._pedir_datos(id, actual))
        print("Modificación realizada exitosamente.")

    def baja(self) -> None:
        id = self._pedir_id()
        actual = self.servicio.leer_por_id(id)
        if actual is None:
            print("No se encontró el registro.")
            return
        self._mostrar(actual)
        if input("¿Confirma la baja? [s/N]: ").strip().lower() not in ("s", "si", "sí"):
            print("Baja cancelada.")
            return
        if self.servicio.eliminar(id):
            print("Baja realizada exitosamente.")
        else:
            print("No se encontró el registro.")

    def listado(self) -> None:
        entidades = self.servicio.leer_todos()
        if not entidades:
            print("No hay registros.")
            return
        self._mostrar_listado(entidades)

    def buscar(self) -> None:
        entidad = self.servicio.leer_por_id(self._pedir_id())
        if entidad is None:
            print("No se encontró el registro.")
            return
        self._mostrar_listado([entidad])
