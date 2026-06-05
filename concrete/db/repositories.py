# concrete/db/repositories.py
"""
Patrón Repositorio. Una clase por entidad; todas operan sobre una Session.
No conocen el proveedor (eso vive en engine.py).
"""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Nodo, Sensor, Lectura


class NodoRepository:
    def __init__(self, session: Session):
        self.session = session

    def listar(self) -> list[Nodo]:
        return list(self.session.scalars(select(Nodo).order_by(Nodo.nodo_id)))

    def obtener_por_mac(self, mac: str) -> Nodo | None:
        return self.session.scalar(select(Nodo).where(Nodo.mac == mac))

    def crear(self, *, mac: str, nombre: str | None = None) -> Nodo:
        nodo = Nodo(mac=mac, nombre=nombre)
        self.session.add(nodo)
        self.session.flush()
        return nodo

    def obtener_o_crear(self, *, mac: str, nombre: str | None = None) -> Nodo:
        return self.obtener_por_mac(mac) or self.crear(mac=mac, nombre=nombre)


class SensorRepository:
    def __init__(self, session: Session):
        self.session = session

    def listar_por_nodo(self, nodo_id: int) -> list[Sensor]:
        return list(self.session.scalars(
            select(Sensor).where(Sensor.nodo_id == nodo_id).order_by(Sensor.sensor_id)
        ))

    def buscar(self, *, nodo_id: int, nombre: str) -> Sensor | None:
        return self.session.scalar(
            select(Sensor).where(Sensor.nodo_id == nodo_id, Sensor.nombre == nombre)
        )

    def crear(self, *, nombre: str, nodo_id: int) -> Sensor:
        sensor = Sensor(nombre=nombre, nodo_id=nodo_id)
        self.session.add(sensor)
        self.session.flush()
        return sensor

    def obtener_o_crear(self, *, nodo_id: int, nombre: str) -> Sensor:
        return self.buscar(nodo_id=nodo_id, nombre=nombre) or \
            self.crear(nombre=nombre, nodo_id=nodo_id)


class LecturaRepository:
    """Acceso a la serie de tiempo. Sólo necesita sensor_id."""

    def __init__(self, session: Session):
        self.session = session

    def graficar(self, sensor_id: int,
                 fecha_inicial: datetime,
                 fecha_final: datetime) -> list[Lectura]:
        """Consulta de las gráficas: usa el índice (sensor_id, fecha DESC)."""
        stmt = (
            select(Lectura)
            .where(
                Lectura.sensor_id == sensor_id,
                Lectura.fecha.between(fecha_inicial, fecha_final),
            )
            .order_by(Lectura.fecha.desc())
        )
        return list(self.session.scalars(stmt))

    def ultima(self, sensor_id: int) -> Lectura | None:
        """Última lectura del sensor (para el valor actual de las tarjetas)."""
        return self.session.scalar(
            select(Lectura)
            .where(Lectura.sensor_id == sensor_id)
            .order_by(Lectura.fecha.desc())
            .limit(1)
        )

    def crear(self, *, sensor_id: int, fecha: datetime,
              temp: float | None = None, hum: float | None = None,
              numero_lectura: int | None = None, manual: bool = False) -> Lectura:
        lectura = Lectura(
            sensor_id=sensor_id, fecha=fecha, temp=temp, hum=hum,
            numero_lectura=numero_lectura, manual=manual,
        )
        self.session.add(lectura)
        self.session.flush()
        return lectura

    def crear_lote(self, lecturas: list[dict]) -> int:
        """Inserción masiva (fase crítica, cada 10 min)."""
        self.session.bulk_insert_mappings(Lectura, lecturas)
        return len(lecturas)