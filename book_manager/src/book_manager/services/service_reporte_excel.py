"""Genera un reporte Excel a partir del CSV de alertas."""

import csv
from datetime import date
from decimal import Decimal
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font


class ServicioReporteExcel:
    """Transforma las alertas de precios en un archivo Excel."""

    def __init__(self, archivo_alertas: Path):
        """Recibe la ruta del CSV de alertas que se utilizará como origen."""
        self.archivo_alertas = Path(archivo_alertas)

    def ejecutar(self) -> None:
        """Genera un Excel fechado en la misma carpeta que el CSV.

        Si el archivo de origen está vacío o contiene solo encabezados,
        genera el reporte únicamente con sus encabezados. Las fechas se
        muestran como DD-MM-YYYY y los importes como valores monetarios.

        Raises:
            FileNotFoundError: Si no existe el archivo de alertas.
        """
        libro_excel = Workbook()
        hoja = libro_excel.active
        hoja.title = "Reporte Precios"

        hoja.append([
            "ISBN",
            "Título",
            "Precio interno",
            "Precio web",
            "Diferencia",
            "Fecha de extracción",
        ])

        with self.archivo_alertas.open(
            encoding="utf-8-sig", newline=""
        ) as archivo:
            for fila in csv.DictReader(archivo):
                hoja.append([
                    fila["isbn"],
                    fila["titulo"],
                    float(Decimal(fila["precio_interno"])),
                    float(Decimal(fila["precio_web"])),
                    float(Decimal(fila["diferencia"])),
                    date.fromisoformat(fila["fecha_extraccion"]),
                ])

        for celda in hoja[1]:
            celda.font = Font(bold=True)

        for fila in hoja.iter_rows(min_row=2):
            fila[0].number_format = "@"

            for celda in fila[2:5]:
                celda.number_format = '"$" #,##0.00'

            fila[5].number_format = "dd-mm-yyyy"

        hoja.column_dimensions["A"].width = 20
        hoja.column_dimensions["B"].width = 45

        for columna in ("C", "D", "E", "F"):
            hoja.column_dimensions[columna].width = 22

        hoja.freeze_panes = "A2"
        hoja.auto_filter.ref = hoja.dimensions

        archivo_excel = self.archivo_alertas.with_name(
            f"reporte_precios_{date.today().isoformat()}.xlsx"
        )
        libro_excel.save(archivo_excel)


