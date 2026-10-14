"""Administra la conexión a PostgreSQL y las transacciones con SQLAlchemy."""
from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

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

class ContextManager:
    """Crea sesiones y administra sus transacciones mediante ``with``."""

    def __init__(self, conexion: ConexionDB):
        """Configura la fábrica de sesiones asociada al motor de conexión.

        Args:
            conexion: Instancia de ConexionDB cuyo motor usarán las sesiones.
        """
        self.session_factory = sessionmaker(
            bind=conexion.engine,
            autoflush=False,
            expire_on_commit=False
        )

    @contextmanager
    def transaction(self) -> Generator[Session, None, None]:
        """Entrega una sesión y cierra su transacción al salir del contexto.

        Confirma los cambios si el bloque termina correctamente. Ante una
        excepción, revierte los cambios y propaga el error. En ambos casos
        cierra la sesión.

        Yields:
            Sesión de SQLAlchemy disponible durante el bloque ``with``.

        Example:
            with gestor.transaction() as session:
                session.add(libro)
        """
        session = self.session_factory()

        try:
            yield session
            session.commit()

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()