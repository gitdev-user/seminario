"""Administra la conexión a PostgreSQL y las transacciones con SQLAlchemy."""
from __future__ import annotations

from sqlalchemy import create_engine, text

class ConexionDB:
    """Gestiona el motor de SQLAlchemy para acceder a PostgreSQL."""

    def __init__(self, url: str):
        """Configura el motor sin abrir todavía una conexión.

        Args:
            url: URL de conexión a PostgreSQL, obtenida de la configuración.
        """
        self.engine = create_engine(
            url,
            pool_pre_ping=True
        )

    def connect(self) -> bool:
        """Comprueba el acceso a la base de datos ejecutando ``SELECT 1``.

        Returns:
            True si la consulta se ejecuta correctamente; False si ocurre
            un error, que se informa por consola.
        """
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                return True
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False

    def close(self) -> None:
        """Libera las conexiones inactivas del pool del motor.

        Debe llamarse después de cerrar las sesiones que utilizan el motor.
        """
        self.engine.dispose()
