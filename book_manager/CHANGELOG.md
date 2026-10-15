  # CHANGELOG

  ## [Ejericio 8]
  ### Nuevo
  -Se agregó en el menu de Gestión de Cotizaciones la opción "Obtener las cotizaciones por Api" 

  ---
  
  ## [Ejercicio 7]
  ### Nuevo
  - Se agregó  el método `obtener_cotizaciones()` en `ServicioCotizacion` para descargar y registrar las cotizaciones de venta desde la API.
  - En `.env` se agregó la url de la API e las cotizaciones del dólar.

  ---

  ## [Ejercicio 6]
  ### Modificación

  - Se modificó `entities.py` para permitir nombres de editorial de hasta 50 caracteres.
  - Se modificó `models.py` para ampliar a 50 caracteres el campo nombre de `EditorialModel`.
  - Se modificó `preload_data.py` para verificar los SQL, recrear las tablas, ejecutar los inserts en orden y sincronizar los IDs.
  - Se adaaptó `repositories.py` a los modelos actuales y a los campos obligatorios de precio y stock.
  - Se modificó `services.py` para utilizar los repositorios de base de datos.
  - Se modificó `main.py` para cargar la conexión desde `.env` y ejecutar la migración y precarga cuando `import_default_data=True`.

  ---

   ## [Ejercicio 5]
   ### Nuevo

  - Se agregó un proceso de migración de archivos CSV a sentencias con inserts de sql.
  - Se agregaron los archivos SQL con los inserts generados en migrations/sql
   ### Modificacion
   - Se corrigió el separador decimal de un precio en precios.csv.

  ---

   ## [Ejercicio 4]
   ### Nuevo
 - Se agregaron en `models.py` los modelos SQLAlchemy de todas las entidades, con sus columnas, claves primarias, claves foráneas, relaciones y restricciones de unicidad.

  ---

   ## [Ejercicio 3]
   ### Nuevo
  - Se agregó la clase `ContextManager` en `connection.py` para gestionar las transacciones de la base de datos, confirmando los cambios o revirtiéndolos ante errores y cerrando las sesiones.
   
   ---

   ## [Ejercicio 2]
   ### Nuevo
  - Se agrega la clase ConexionDB en connection.py para gestionar la conexión a la base de datos y se incorpora SQLAlchemy en requirements.txt.
   
   ---

   ## [Ejercicio 1]
   ### Nuevo
   - Se creó la rama para el Sprint 2
   - Se agregó nuevo contenido vinculado al Sprint 2 en el archivo README.md.
   - Se agregó `pydantic-settings` a requirements.txt para gestionar y validar la configuración de la aplicación mediante variables de entorno.
   - Se incorporó `connection.py` en database/ y `models.py` en models/.
   
   ---