# concrete/db/models.py
"""
Modelos ORM (SQLAlchemy 2.0).  Jerarquía: Nodo 1───* Sensor 1───* Lectura
El nodo agrupa sensores (es el receptor). El sensor es la unidad monitoreada.
"""

from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Double, ForeignKey, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Nodo(Base):
    __tablename__ = "nodo"

    nodo_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    mac: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    nombre: Mapped[str | None] = mapped_column(Text)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    sensores: Mapped[list["Sensor"]] = relationship(back_populates="nodo")


class Sensor(Base):
    __tablename__ = "sensor"

    sensor_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    nombre: Mapped[str] = mapped_column(Text, nullable=False)        # nombre de hardware
    alias: Mapped[str | None] = mapped_column(Text)                  # nombre amigable (display)
    nodo_id: Mapped[int] = mapped_column(
        ForeignKey("nodo.nodo_id", ondelete="CASCADE"), nullable=False
    )
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    nodo: Mapped["Nodo"] = relationship(back_populates="sensores")
    lecturas: Mapped[list["Lectura"]] = relationship(back_populates="sensor")


class Lectura(Base):
    __tablename__ = "lectura"

    lectura_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sensor_id: Mapped[int] = mapped_column(
        ForeignKey("sensor.sensor_id", ondelete="CASCADE"), nullable=False
    )
    numero_lectura: Mapped[int | None] = mapped_column(BigInteger)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    temp: Mapped[float | None] = mapped_column(Double)
    hum: Mapped[float | None] = mapped_column(Double)
    manual: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    sensor: Mapped["Sensor"] = relationship(back_populates="lecturas")