  # CHANGELOG

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