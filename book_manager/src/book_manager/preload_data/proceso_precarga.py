import csv
from pathlib import Path
from typing import Any, Mapping, Sequence

from pydantic import BaseModel

from config.config import config
from preload_data.preload_data import DATOS_PRECARGA


class ProcesoPrecarga:
    """Recrea cada CSV con los registros validados por su modelo."""

    def ejecutar(
        self,
        carpeta_destino: str | Path | None = None,
        datos: Mapping[str, tuple[type[BaseModel], Sequence[Mapping[str, Any]]]] | None = None,
    ) -> None:
        """Elimina, valida y escribe un archivo por vez.

        Usa la carpeta configurada y DATOS_PRECARGA por defecto e informa cada
        precarga exitosa. Si falla una validación, el archivo anterior ya
        fue eliminado y los archivos procesados previamente se conservan.
        """
        destino = (
            Path(carpeta_destino) if carpeta_destino is not None
            else config.directorio_repositorio
        ).resolve()
        destino.mkdir(parents=True, exist_ok=True)
        conjuntos = DATOS_PRECARGA if datos is None else datos

        for nombre, (modelo, registros) in conjuntos.items():
            archivo = destino / nombre
            if archivo.resolve().parent != destino or archivo.suffix.lower() != ".csv":
                raise ValueError(f"El destino debe ser un CSV dentro de {destino}: {nombre}")
            archivo.unlink(missing_ok=True)

            entidades = [modelo.model_validate(registro) for registro in registros]

            with archivo.open("w", newline="", encoding="utf-8") as salida:
                escritor = csv.DictWriter(salida, fieldnames=list(modelo.model_fields))
                escritor.writeheader()
                escritor.writerows(
                    entidad.model_dump(mode="json") for entidad in entidades
                )
            
