from datetime import date
from typing import List, Optional

from dto.cotizacion_detalle import CotizacionDetalle
from entities.cotizacion import Cotizacion
from repositories.impl.csv_archivo_repositorio_cotizacion_impl import (
    CSVArchivoRepositorioCotizacion,
)
from repositories.impl.csv_archivo_repositorio_moneda_impl import (
    CSVArchivoRepositorioMoneda,
)
from repositories.impl.csv_archivo_repositorio_tipo_cotizacion_impl import (
    CSVArchivoRepositorioTipoCotizacion,
)


class ServicioCotizacion:
    """Gestiona cotizaciones identificadas por tipo, monedas y fecha."""

    def __init__(
        self,
        repositorio: CSVArchivoRepositorioCotizacion,
        repositorio_moneda: CSVArchivoRepositorioMoneda,
        repositorio_tipo_cotizacion: CSVArchivoRepositorioTipoCotizacion,
    ):
        self.repositorio = repositorio
        self.repositorio_moneda = repositorio_moneda
        self.repositorio_tipo_cotizacion = repositorio_tipo_cotizacion

    def guardar(self, cotizacion: Cotizacion) -> Cotizacion:
        """Crea la cotización si su clave no existe; si existe, la actualiza."""
        for moneda_id in (cotizacion.moneda_origen_id, cotizacion.moneda_destino_id):
            if self.repositorio_moneda.leer_por_id(moneda_id) is None:
                raise ValueError(f"No existe una moneda con ID {moneda_id}")
        if self.repositorio_tipo_cotizacion.leer_por_id(cotizacion.tipo_cotizacion_id) is None:
            raise ValueError(f"No existe el tipo de cotización {cotizacion.tipo_cotizacion_id}")
        existente = self.repositorio.leer_por_tipo_moneda_origen_destino_y_fecha(
            cotizacion.tipo_cotizacion_id,
            cotizacion.moneda_origen_id,
            cotizacion.moneda_destino_id,
            cotizacion.fecha,
        )
        if existente is None:
            return self.repositorio.crear(cotizacion)
        return self.repositorio.actualizar(cotizacion)

    def eliminar(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int,
        fecha: date,
    ) -> bool:
        """Elimina la cotización y devuelve False si no existe."""
        return self.repositorio.eliminar(
            tipo_id, moneda_origen_id, moneda_destino_id, fecha
        )

    def leer_por_tipo_moneda_origen_destino_y_fecha(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int,
        fecha: date,
    ) -> Optional[Cotizacion]:
        """Devuelve la cotización de la clave indicada, o None si no existe."""
        return self.repositorio.leer_por_tipo_moneda_origen_destino_y_fecha(
            tipo_id, moneda_origen_id, moneda_destino_id, fecha
        )

    def leer_historico_por_tipo_moneda_origen_moneda_destino(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int,
    ) -> List[Cotizacion]:
        """Devuelve el histórico para el tipo y las monedas indicados."""
        return self.repositorio.leer_historico_por_tipo_moneda_origen_moneda_destino(
            tipo_id, moneda_origen_id, moneda_destino_id
        )

    def leer_historico_detalle_por_tipo_moneda_origen_moneda_destino(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int,
    ) -> List[CotizacionDetalle]:
        """Arma el histórico reutilizando la consulta de detalle individual.

        Devuelve una lista vacía si no hay cotizaciones. Lanza ValueError si
        una cotización deja de existir durante la consulta o falta una relación.
        """
        cotizaciones = self.leer_historico_por_tipo_moneda_origen_moneda_destino(
            tipo_id, moneda_origen_id, moneda_destino_id
        )
        detalles: List[CotizacionDetalle] = []
        for cotizacion in cotizaciones:
            detalle = self.leer_detalle_por_tipo_moneda_origen_destino_y_fecha(
                cotizacion.tipo_cotizacion_id,
                cotizacion.moneda_origen_id,
                cotizacion.moneda_destino_id,
                cotizacion.fecha,
            )
            if detalle is None:
                raise ValueError(
                    "La cotización del histórico ya no existe: "
                    f"tipo {cotizacion.tipo_cotizacion_id}, "
                    f"monedas {cotizacion.moneda_origen_id} y "
                    f"{cotizacion.moneda_destino_id}, fecha {cotizacion.fecha}"
                )
            detalles.append(detalle)
        return detalles

    def leer_detalle_por_tipo_moneda_origen_destino_y_fecha(
        self,
        tipo_id: int,
        moneda_origen_id: int,
        moneda_destino_id: int,
        fecha: date,
    ) -> Optional[CotizacionDetalle]:
        """Devuelve el detalle, o None si la cotización no existe.

        Raises:
            ValueError: Si una moneda o el tipo referenciados no existen.
        """
        cotizacion = self.leer_por_tipo_moneda_origen_destino_y_fecha(
            tipo_id, moneda_origen_id, moneda_destino_id, fecha
        )
        if cotizacion is None:
            return None

        moneda_origen = self.repositorio_moneda.leer_por_id(
            cotizacion.moneda_origen_id
        )
        if moneda_origen is None:
            raise ValueError(
                f"No existe la moneda de origen con ID {cotizacion.moneda_origen_id}"
            )

        moneda_destino = self.repositorio_moneda.leer_por_id(
            cotizacion.moneda_destino_id
        )
        if moneda_destino is None:
            raise ValueError(
                f"No existe la moneda de destino con ID {cotizacion.moneda_destino_id}"
            )

        tipo_cotizacion = self.repositorio_tipo_cotizacion.leer_por_id(
            cotizacion.tipo_cotizacion_id
        )
        if tipo_cotizacion is None:
            raise ValueError(
                f"No existe el tipo de cotización con ID {cotizacion.tipo_cotizacion_id}"
            )

        return CotizacionDetalle(
            cotizacion=cotizacion,
            moneda_origen=moneda_origen,
            moneda_destino=moneda_destino,
            tipo_cotizacion=tipo_cotizacion,
        )
