from datetime import date

from entities.cotizacion import Cotizacion
from services.servicio_cotizacion import ServicioCotizacion
from ui.consola import ConsolaOperaciones
from ui.consola_entidad import ConsolaEntidad


class ConsolaGestionCotizaciones(ConsolaOperaciones):
    def __init__(self, acciones=None, servicio: ServicioCotizacion | None = None):
        self.servicio = servicio
        operaciones = [
            ("alta", "Alta"), ("modificacion", "Modificación"), ("baja", "Baja"),
            ("listado", "Ver Listado Histórico"), ("buscar", "Buscar Cotización"),
        ]
        manejadores = {}
        if servicio is not None:
            manejadores = {
                clave: ConsolaEntidad._manejar_errores(getattr(self, clave))
                for clave, _ in operaciones
            }
        if acciones is not None:
            manejadores.update(acciones)
        super().__init__("Gestión de Cotizaciones", operaciones, manejadores)

    @staticmethod
    def _pedir_id(etiqueta):
        while True:
            try:
                valor = int(input(f"{etiqueta}: ").strip())
                if valor > 0:
                    return valor
            except ValueError:
                pass
            print("Ingrese un ID entero mayor que cero.")

    def _pedir_filtros(self):
        return (
            self._pedir_id("ID del tipo de cotización"),
            self._pedir_id("ID de moneda de origen"),
            self._pedir_id("ID de moneda de destino"),
        )

    def _pedir_clave(self):
        filtros = self._pedir_filtros()
        while True:
            try:
                fecha = date.fromisoformat(input("Fecha (AAAA-MM-DD): ").strip())
                return (*filtros, fecha)
            except ValueError:
                print("Ingrese una fecha válida en formato AAAA-MM-DD.")

    @staticmethod
    def _mostrar(detalles):
        if not detalles:
            print("No hay cotizaciones para los filtros indicados.")
            return
        encabezados = ["Fecha", "Tipo", "Moneda origen", "Moneda destino", "Valor"]
        filas = [
            [str(d.cotizacion.fecha), f"{d.tipo_cotizacion.id} - {d.tipo_cotizacion.nombre}",
             f"{d.moneda_origen.id} - {d.moneda_origen.codigo_iso}",
             f"{d.moneda_destino.id} - {d.moneda_destino.codigo_iso}",
             f"{d.cotizacion.valor:.2f}"]
            for d in detalles
        ]
        filas = [[" ".join(valor.split()) for valor in fila] for fila in filas]
        anchos = [max(len(titulo), *(len(fila[i]) for fila in filas))
                  for i, titulo in enumerate(encabezados)]
        print()
        print(" | ".join(v.ljust(a) for v, a in zip(encabezados, anchos)))
        print("-+-".join("-" * a for a in anchos))
        for fila in filas:
            print(" | ".join(v.ljust(a) for v, a in zip(fila, anchos)))

    def alta(self):
        clave = self._pedir_clave()
        if self.servicio.leer_por_tipo_moneda_origen_destino_y_fecha(*clave) is not None:
            print("Ya existe esa cotización. Use Modificación.")
            return
        tipo, origen, destino, fecha = clave
        cotizacion = Cotizacion(
            tipo_cotizacion_id=tipo, moneda_origen_id=origen,
            moneda_destino_id=destino, fecha=fecha,
            valor=input("Valor (unidades de destino por unidad de origen): ").strip(),
        )
        self.servicio.guardar(cotizacion)
        print("Cotización creada exitosamente.")

    def modificacion(self):
        clave = self._pedir_clave()
        detalle = self.servicio.leer_detalle_por_tipo_moneda_origen_destino_y_fecha(*clave)
        if detalle is None:
            print("No se encontró la cotización.")
            return
        self._mostrar([detalle])
        valor = input(f"Valor [{detalle.cotizacion.valor}] (Enter para conservar): ").strip()
        datos = detalle.cotizacion.model_dump()
        if valor:
            datos["valor"] = valor
        self.servicio.guardar(Cotizacion.model_validate(datos))
        print("Cotización modificada exitosamente.")

    def baja(self):
        clave = self._pedir_clave()
        detalle = self.servicio.leer_detalle_por_tipo_moneda_origen_destino_y_fecha(*clave)
        if detalle is None:
            print("No se encontró la cotización.")
            return
        self._mostrar([detalle])
        if input("¿Confirma la baja? [s/N]: ").strip().lower() not in ("s", "si", "sí"):
            print("Baja cancelada.")
            return
        if self.servicio.eliminar(*clave):
            print("Cotización eliminada exitosamente.")
        else:
            print("No se encontró la cotización.")

    def listado(self):
        detalles = self.servicio.leer_historico_detalle_por_tipo_moneda_origen_moneda_destino(
            *self._pedir_filtros()
        )
        self._mostrar(sorted(detalles, key=lambda d: d.cotizacion.fecha))

    def buscar(self):
        detalle = self.servicio.leer_detalle_por_tipo_moneda_origen_destino_y_fecha(
            *self._pedir_clave()
        )
        if detalle is None:
            print("No se encontró la cotización.")
            return
        self._mostrar([detalle])
