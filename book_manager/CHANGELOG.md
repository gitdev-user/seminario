  # CHANGELOG

  ## [Ejercicio 4]
   ### Nuevo

   - Se implementó `ServicioAlerta` para ejecutar el scraping, leer el JSON y comparar los precios web e internos en ARS de los libros encontrados, identificados por ISBN. El usuario ingresa un umbral porcentual entre 0 y 1 antes de cada ejecución. Si la diferencia absoluta supera ese umbral, se registra una alerta en `reportes/alertas_precios_AAAAMMDD.csv`, con ISBN, título, precios, diferencia monetaria, umbral y fecha de extracción. El archivo se genera con encabezados aunque no haya alertas.

   ---
   
   ## [Ejercicio 3]
   ### Nuevo
   - Se implementó el scraping de Cúspide con búsqueda por título y coincidencia exacta entre títulos normalizados, extracción de datos mediante `CuspideLibroLoader`, validación con pipeline y ejecución mediante `ServicioScraping`, con configuración centralizada en `settings.py` y exportación a `reportes/libros_cuspide.json`

   ### Modificación
   - Se agregó la clase faltante de `ServicioScraping`.

   ### Modificación
   - Se agregó la clase faltante de `scraper/loaders.py`.

   ---
   
   ## [Ejercicio 2]
   ### Verificación
   - Se verificó que la carga de archivos SQL ya estaba implementada en `ProcesoPrecarga.importar_datos()` y conectada al flujo de inicio en `main.py` (Sprint 2)
   - No fue necesario realizar cambios en el código.

   ---

   ## [Ejercicio 1]
   ### Nuevo
   - Se creó la rama para el Sprint 3
   - Se agregó nuevo contenido vinculado al Sprint 3 en el archivo README.md.
   - Se agregó la estructura inicial para el scraper con el comando `python -m scrapy startproject scraper`.
   - Se agregó la carpeta `reportes` para almacenar futuros reportes.
   
   ---