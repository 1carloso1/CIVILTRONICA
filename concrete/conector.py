# conector.py
"""
Capa de acceso a datos sobre PostgreSQL/Supabase.

Modelo: nodo (receptor, agrupa) -> sensor (unidad monitoreada) -> lectura.
El dashboard muestra UNA tarjeta por SENSOR; el nodo es la agrupación.
"""

from types import SimpleNamespace

from concrete.serializers import Tarjeta, Nodo, Sensor, Lectura
from concrete.db import (
    session_scope,
    NodoRepository,
    SensorRepository,
    LecturaRepository,
)


def _renglon(tipo, dato, unidades, sensor_id, campo):
    return SimpleNamespace(tipo=tipo, dato=dato, unidades=unidades,
                           sensor_id=sensor_id, campo=campo)


# =====================================================================
#  API que consume tu UI
# =====================================================================

def consultar_tarjetas(nodo_id=None):
    """
    Cada SENSOR es una tarjeta. El nodo va como etiqueta de agrupación.
    Si nodo_id se da, sólo devuelve los sensores de ese nodo (filtro).
    """
    with session_scope() as s:
        filas = SensorRepository(s).listar_con_nodo(nodo_id)
        tarjetas = []
        for sensor, nodo in filas:
            etiqueta_nodo = nodo.nombre or nodo.mac
            nombre = sensor.alias or sensor.nombre
            tarjetas.append(Tarjeta(
                tarjeta_id=sensor.sensor_id,
                id_fisico=nodo.mac,
                nombre=nombre,
                grupo_id=nodo.nodo_id,
                tags=[etiqueta_nodo],
            ))
        return tarjetas


def consultar_sensores_por_tarjeta(sensor_id):
    """Renglones Temperatura/Humedad con el último valor de ese sensor."""
    with session_scope() as s:
        ultima = LecturaRepository(s).ultima(sensor_id)
        temp = ultima.temp if ultima else None
        hum = ultima.hum if ultima else None
        return [
            _renglon('Temperatura', temp, '°C', sensor_id, 'temp'),
            _renglon('Humedad', hum, '%', sensor_id, 'hum'),
        ]


# =====================================================================
#  Gestión / etiquetado / eliminación (diálogo)
# =====================================================================

def consultar_sensores():
    """Detalle de cada sensor + su nodo, para el diálogo."""
    with session_scope() as s:
        filas = SensorRepository(s).listar_con_nodo()
        return [
            SimpleNamespace(
                sensor_id=sensor.sensor_id,
                nombre=sensor.nombre,
                alias=sensor.alias,
                nodo_id=nodo.nodo_id,
                nodo_nombre=nodo.nombre,
                mac=nodo.mac,
            )
            for sensor, nodo in filas
        ]


def renombrar_sensor(sensor_id, alias):
    with session_scope() as s:
        SensorRepository(s).actualizar_alias(sensor_id, alias)


def renombrar_nodo(nodo_id, nombre):
    with session_scope() as s:
        NodoRepository(s).actualizar_nombre(nodo_id, nombre)


def eliminar_sensor(sensor_id):
    """Borra un sensor y todas sus lecturas (cascada)."""
    with session_scope() as s:
        SensorRepository(s).eliminar(sensor_id)


def eliminar_nodo(nodo_id):
    """Borra un nodo con todos sus sensores y lecturas (cascada)."""
    with session_scope() as s:
        NodoRepository(s).eliminar(nodo_id)


# =====================================================================
#  API nueva / hardware
# =====================================================================

def _nodo_to_serializer(n):
    nodo = Nodo()
    nodo.update_from_dict({"nodo_id": n.nodo_id, "mac": n.mac, "nombre": n.nombre})
    return nodo


def _lectura_to_serializer(l):
    lectura = Lectura()
    lectura.update_from_dict({
        "lectura_id": l.lectura_id, "sensor_id": l.sensor_id,
        "numero_lectura": l.numero_lectura, "fecha": l.fecha,
        "temp": l.temp, "hum": l.hum,
    })
    return lectura


def consultar_nodos():
    with session_scope() as s:
        return [_nodo_to_serializer(n) for n in NodoRepository(s).listar()]


def consultar_lecturas(sensor_id, fecha_inicial, fecha_final):
    with session_scope() as s:
        filas = LecturaRepository(s).graficar(sensor_id, fecha_inicial, fecha_final)
        return [_lectura_to_serializer(l) for l in filas]


def registrar_lectura_desde_hardware(mac, nombre_sensor, fecha,
                                     temp=None, hum=None, numero_lectura=None):
    with session_scope() as s:
        nodo = NodoRepository(s).obtener_o_crear(mac=mac)
        sensor = SensorRepository(s).obtener_o_crear(nodo_id=nodo.nodo_id, nombre=nombre_sensor)
        return LecturaRepository(s).crear(
            sensor_id=sensor.sensor_id, fecha=fecha, temp=temp, hum=hum,
            numero_lectura=numero_lectura,
        ).lectura_id