from abc import ABC, abstractmethod
from typing import Callable, Mapping


class IConsola(ABC):
    @abstractmethod
    def ejecutar(self) -> None:
        """Muestra la consola hasta que el usuario vuelva o salga."""


class ConsolaMenu(IConsola):
    def __init__(self, titulo: str, opciones: Mapping[str, tuple[str, Callable[[], None]]],
                 salida: str = "Volver",
                 encabezado: str | None = "SISTEMA DE GESTION DE LIBRERIA"):
        self.titulo = titulo
        self.opciones = dict(opciones)
        self.salida = salida
        self.encabezado = encabezado

    def ejecutar(self) -> None:
        while True:
            if self.encabezado:
                ancho = max(50, len(self.encabezado) + 4)
                print("\n" + "=" * ancho)
                print(self.encabezado.center(ancho))
                print("=" * ancho)
            print(f"\n=== {self.titulo} ===")
            for clave, (texto, _) in self.opciones.items():
                print(f"{clave}. {texto}")
            print(f"0. {self.salida}")
            opcion = input("Seleccione una opción: ").strip()
            if opcion == "0":
                return
            if opcion not in self.opciones:
                print("Opción inválida. Intente nuevamente.")
                continue
            self.opciones[opcion][1]()


class ConsolaOperaciones(ConsolaMenu):
    """Reutiliza el menú y recibe las acciones que llamarán a los servicios."""

    def __init__(self, titulo: str, operaciones: list[tuple[str, str]],
                 acciones: Mapping[str, Callable[[], None]] | None = None):
        acciones = {} if acciones is None else acciones
        desconocidas = set(acciones) - {clave for clave, _ in operaciones}
        if desconocidas:
            raise ValueError(f"Acciones desconocidas: {desconocidas}")
        opciones = {}
        for numero, (clave, texto) in enumerate(operaciones, start=1):
            opciones[str(numero)] = (
                texto, acciones.get(clave, self._pendiente(texto))
            )
        super().__init__(titulo, opciones)

    @staticmethod
    def _pendiente(texto: str) -> Callable[[], None]:
        def avisar() -> None:
            print(f"{texto}: operación pendiente de conectar al servicio.")
        return avisar
