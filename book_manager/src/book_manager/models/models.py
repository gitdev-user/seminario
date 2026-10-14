"""Modelos SQLAlchemy para persistir las entidades de la librería."""

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """Base declarativa que reúne los metadatos de todas las tablas."""


class TipoCotizacionModel(Base):
    __tablename__ = "tipos_cotizacion"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(15), nullable=False, unique=True)
    descripcion = Column(String(50), nullable=False)


class MonedaModel(Base):
    __tablename__ = "monedas"

    id = Column(Integer, primary_key=True)
    codigo_iso = Column(String(3), nullable=False, unique=True)
    nombre = Column(String(50), nullable=False)
    simbolo = Column(String(5), nullable=False)


class GeneroModel(Base):
    __tablename__ = "generos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(20), nullable=False,unique=True)
    descripcion = Column(String(50), nullable=False)

    libros = relationship("LibroModel", back_populates="genero")


class EditorialModel(Base):
    __tablename__ = "editoriales"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(20), nullable=False,unique=True)
    grupo = Column(String(50), nullable=False)
    pais_origen = Column(String(20), nullable=False)
    telefono = Column(String(20), nullable=False)
    email = Column(Text, nullable=False)

    libros = relationship("LibroModel", back_populates="editorial")


class LibroModel(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True)
    isbn = Column(String(13), nullable=False,unique=True)
    titulo = Column(String(30), nullable=False)
    autor = Column(String(20), nullable=False)
    peso = Column(Float, nullable=False)
    dimensiones = Column(String(50), nullable=False)
    numero_paginas = Column(Integer, nullable=False)
    fecha_publicacion = Column(Date, nullable=False)
    idioma = Column(String(30), nullable=False)
    editorial_id = Column(Integer, ForeignKey("editoriales.id"), nullable=False)
    genero_id = Column(Integer, ForeignKey("generos.id"), nullable=False)

    editorial = relationship("EditorialModel", back_populates="libros")
    genero = relationship("GeneroModel", back_populates="libros")
    precio = relationship(
        "PrecioModel", back_populates="libro", uselist=False,
        cascade="all, delete-orphan", single_parent=True,
    )
    stock = relationship(
        "StockModel", back_populates="libro", uselist=False,
        cascade="all, delete-orphan", single_parent=True,
    )


class PrecioModel(Base):
    __tablename__ = "precios"

    # La entidad admite un solo precio por libro.
    libro_id = Column(Integer, ForeignKey("libros.id"), primary_key=True)
    moneda_id = Column(Integer, ForeignKey("monedas.id"), nullable=False)
    precio_base = Column(Float, nullable=False)

    libro = relationship("LibroModel", back_populates="precio")
    moneda = relationship("MonedaModel")


class StockModel(Base):
    __tablename__ = "stock"

    # La entidad admite un solo stock por libro.
    libro_id = Column(Integer, ForeignKey("libros.id"), primary_key=True)
    cantidad_minima = Column(Integer, nullable=False)
    cantidad_total = Column(Integer, nullable=False)

    libro = relationship("LibroModel", back_populates="stock")


class CotizacionModel(Base):
    __tablename__ = "cotizaciones"

    __table_args__ = (
        UniqueConstraint(
            "tipo_cotizacion_id",
            "moneda_origen_id",
            "moneda_destino_id",
            "fecha",
            name="uq_cotizacion_tipo_monedas_fecha",
        ),
    )

    id = Column(Integer, primary_key=True)
    moneda_origen_id = Column(
        Integer, ForeignKey("monedas.id"), nullable=False,
    )
    moneda_destino_id = Column(
        Integer, ForeignKey("monedas.id"), nullable=False,
    )
    tipo_cotizacion_id = Column(
        Integer, ForeignKey("tipos_cotizacion.id"), nullable=False,
    )
    fecha = Column(Date, nullable=False)
    valor = Column(Float, nullable=False)

    moneda_origen = relationship("MonedaModel", foreign_keys=[moneda_origen_id])
    moneda_destino = relationship("MonedaModel", foreign_keys=[moneda_destino_id])
    tipo_cotizacion = relationship("TipoCotizacionModel")
