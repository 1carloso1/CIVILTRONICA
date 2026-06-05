# concrete/db/repositories.py
"""Patrón Repositorio. Una clase por entidad; operan sobre una Session."""

from datetime import datetime

from sqlalchemy import select, delete
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

    def actualizar_nombre(self, nodo_id: int, nombre: str | None) -> Nodo | None:
        nodo = self.session.get(Nodo, nodo_id)
        if nodo is not None:
            nodo.nombre = nombre
        return nodo

    def eliminar(self, nodo_id: int) -> None:
        # ON DELETE CASCADE en la BD borra sus sensores y lecturas.
        self.session.execute(delete(Nodo).where(Nodo.nodo_id == nodo_id))


class SensorRepository:
    def __init__(self, session: Session):
        self.session = session

    def listar_por_nodo(self, nodo_id: int) -> list[Sensor]:
        return list(self.session.scalars(
            select(Sensor).where(Sensor.nodo_id == nodo_id).order_by(Sensor.sensor_id)
        ))

    def listar_con_nodo(self, nodo_id: int | None = None) -> list[tuple[Sensor, Nodo]]:
        """Sensores junto con su nodo. Si nodo_id se da, filtra por ese nodo."""
        stmt = select(Sensor, Nodo).join(Nodo, Sensor.nodo_id == Nodo.nodo_id)
        if nodo_id is not None:
            stmt = stmt.where(Nodo.nodo_id == nodo_id)
        stmt = stmt.order_by(Nodo.nodo_id, Sensor.sensor_id)
        return list(self.session.execute(stmt).all())

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

    def actualizar_alias(self, sensor_id: int, alias: str | None) -> Sensor | None:
        sensor = self.session.get(Sensor, sensor_id)
        if sensor is not None:
            sensor.alias = alias or None
        return sensor

    def eliminar(self, sensor_id: int) -> None:
        # ON DELETE CASCADE borra sus lecturas.
        self.session.execute(delete(Sensor).where(Sensor.sensor_id == sensor_id))


class LecturaRepository:
    def __init__(self, session: Session):
        self.session = session

    def graficar(self, sensor_id: int, fecha_inicial: datetime,
                 fecha_final: datetime) -> list[Lectura]:
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
        return self.session.scalar(
            select(Lectura).where(Lectura.sensor_id == sensor_id)
            .order_by(Lectura.fecha.desc()).limit(1)
        )

    def crear(self, *, sensor_id: int, fecha: datetime,
              temp: float | None = None, hum: float | None = None,
              numero_lectura: int | None = None, manual: bool = False) -> Lectura:
        lectura = Lectura(sensor_id=sensor_id, fecha=fecha, temp=temp, hum=hum,
                          numero_lectura=numero_lectura, manual=manual)
        self.session.add(lectura)
        self.session.flush()
        return lectura

    def crear_lote(self, lecturas: list[dict]) -> int:
        self.session.bulk_insert_mappings(Lectura, lecturas)
        return len(lecturas)