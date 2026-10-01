from ui.consola import ConsolaOperaciones
from ui.consola_entidad import ConsolaEntidad


class ConsolaRegistroInventario(ConsolaOperaciones):
    """Comparte las operaciones de un registro de inventario por libro."""

    def __init__(self, acciones=None, servicio=None):
        self.servicio = servicio
        operaciones = [("alta", "Alta"), ("modificacion", "Modificación"),
                       ("buscar", f"Buscar {self.NOMBRE}")]
        manejadores = {}
        if servicio is not None:
            manejadores = {
                clave: ConsolaEntidad._manejar_errores(getattr(self, clave))
                for clave, _ in operaciones
            }
        if acciones is not None:
            manejadores.update(acciones)
        super().__init__(self.TITULO, operaciones, manejadores)

    @staticmethod
    def _pedir_libro():
        while True:
            try:
                id = int(input("ID del libro: ").strip())
                if id > 0:
                    return id
            except ValueError:
                pass
            print("Ingrese un ID entero mayor que cero.")

    def _leer(self, libro_id):
        return getattr(self.servicio, self.METODO_LEER)(libro_id)

    def _guardar(self, registro):
        return getattr(self.servicio, self.METODO_GUARDAR)(registro)

    def _pedir_datos(self, libro_id, actual=None):
        datos = {"libro_id": libro_id} if actual is None else actual.model_dump()
        if actual is not None:
            print("Presione Enter para conservar cada valor actual.")
        for campo, etiqueta in self.CAMPOS:
            anterior = datos.get(campo)
            indicacion = f" [{anterior}]" if actual is not None else ""
            valor = input(f"{etiqueta}{indicacion}: ").strip()
            if valor or actual is None:
                datos[campo] = valor
        return self.MODELO.model_validate(datos)

    @staticmethod
    def _tabla(encabezados, valores):
        valores = [" ".join(str(valor).split()) for valor in valores]
        anchos = [max(len(titulo), len(valor)) for titulo, valor in zip(encabezados, valores)]
        print()
        print(" | ".join(t.ljust(a) for t, a in zip(encabezados, anchos)))
        print("-+-".join("-" * a for a in anchos))
        print(" | ".join(v.ljust(a) for v, a in zip(valores, anchos)))

    def _mostrar(self, registro):
        self._tabla(["ID Libro"] + [etiqueta for _, etiqueta in self.CAMPOS],
                    [registro.libro_id] + [getattr(registro, campo) for campo, _ in self.CAMPOS])

    def alta(self):
        libro_id = self._pedir_libro()
        if self._leer(libro_id) is not None:
            print(f"Ya existe {self.NOMBRE.lower()} para el libro. Use Modificación.")
            return
        self._guardar(self._pedir_datos(libro_id))
        print("Alta realizada exitosamente.")

    def modificacion(self):
        libro_id = self._pedir_libro()
        actual = self._leer(libro_id)
        if actual is None:
            print(f"No hay {self.NOMBRE.lower()} registrado para ese libro.")
            return
        self._mostrar(actual)
        self._guardar(self._pedir_datos(libro_id, actual))
        print("Modificación realizada exitosamente.")

    def buscar(self):
        actual = self._leer(self._pedir_libro())
        if actual is None:
            print(f"No hay {self.NOMBRE.lower()} registrado para ese libro.")
            return
        self._mostrar(actual)
