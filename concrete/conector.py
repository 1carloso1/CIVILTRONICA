# conector.py
"""
Capa de acceso a datos sobre PostgreSQL/Supabase (SQLAlchemy).

Modelo real en la base:  nodo -> sensor -> lectura.

Para NO reescribir tu interfaz, este facade expone la API "vieja" que tu
app ya usa (consultar_tarjetas, consultar_sensores_por_tarjeta, etc.),
pero por debajo lee de las tablas nuevas:

    Tarjeta  ->  nodo   (id_fisico = mac)
    Sensor   ->  renglón de tablero por métrica (Temperatura / Humedad),
                 con el último valor de la última lectura.

Más abajo está también la API "nueva" (consultar_nodos, consultar_lecturas)
y la ingesta desde hardware.
"""

from types import SimpleNamespace

from concrete.serializers import Tarjeta, Nodo, Sensor, Lectura
from concrete.db import (
    session_scope,
    NodoRepository,
    SensorRepository,
    LecturaRepository,
)


# =====================================================================
#  API VIEJA  — la que consume tu UI actual (no toques los widgets)
# =====================================================================

def _renglon(tipo, dato, unidades, sensor_id, campo):
    """
    Objeto ligero que tus widgets leen como un 'sensor'.
    Lleva tipo/dato/unidades (para la tarjeta del dashboard) y además
    sensor_id + campo ('temp'/'hum') para que el historial sepa qué
    serie pedir de cada lectura.
    """
    return SimpleNamespace(tipo=tipo, dato=dato, unidades=unidades,
                           sensor_id=sensor_id, campo=campo)


def consultar_tarjetas():
    """Cada nodo se presenta como una 'tarjeta' del dashboard."""
    with session_scope() as s:
        nodos = NodoRepository(s).listar()
        return [
            Tarjeta(
                tarjeta_id=n.nodo_id,
                id_fisico=n.mac,
                nombre=(n.nombre or n.mac),
                grupo_id=None,
                tags=[],
            )
            for n in nodos
        ]


def consultar_sensores_por_tarjeta(tarjeta_id):
    """
    tarjeta_id es en realidad el nodo_id. Por cada sensor del nodo devuelve
    DOS renglones (Temperatura y Humedad) con el último valor leído, que es
    justo lo que tu tarjeta dibuja.
    """
    with session_scope() as s:
        sensores = SensorRepository(s).listar_por_nodo(tarjeta_id)
        lr = LecturaRepository(s)
        renglones = []
        for sensor in sensores:
            ultima = lr.ultima(sensor.sensor_id)
            temp = ultima.temp if ultima else None
            hum = ultima.hum if ultima else None
            renglones.append(_renglon('Temperatura', temp, '°C', sensor.sensor_id, 'temp'))
            renglones.append(_renglon('Humedad', hum, '%', sensor.sensor_id, 'hum'))
        return renglones


def consultar_grupos():
    """El modelo nuevo no tiene grupos; se conserva para no romper imports."""
    return []


def agregar_tarjeta(tarjeta, tipo_sensores=None):
    """
    Registro manual de dispositivo: crea el nodo (la MAC va en id_fisico)
    y un sensor. (Normalmente el hardware los crea solo vía la función RPC.)
    """
    with session_scope() as s:
        nodo = NodoRepository(s).obtener_o_crear(
            mac=tarjeta.id_fisico, nombre=tarjeta.nombre
        )
        SensorRepository(s).obtener_o_crear(
            nodo_id=nodo.nodo_id, nombre=(tarjeta.nombre or 'Sensor_01')
        )
        tarjeta.tarjeta_id = nodo.nodo_id
    return tarjeta


def agregar_sensor(sensor):
    """Crea un sensor. `sensor` debe traer .nodo_id y .nombre."""
    with session_scope() as s:
        nuevo = SensorRepository(s).crear(nombre=sensor.nombre, nodo_id=sensor.nodo_id)
        return nuevo.sensor_id


# =====================================================================
#  API NUEVA  — modelo nodo/sensor/lectura (para el historial y el hardware)
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
    """Para las gráficas de historial: devuelve lecturas (temp+hum) por rango."""
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