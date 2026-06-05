# test_conexion.py
"""
Prueba de humo de la capa de datos contra Supabase/PostgreSQL.
Crea un nodo + sensor + 2 lecturas, las consulta y las imprime.

Ejecuta:  python test_conexion.py
(Requiere el .env con DATABASE_URL y: pip install SQLAlchemy psycopg2-binary python-dotenv)
"""

from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
load_dotenv()  # carga DATABASE_URL desde el archivo .env ANTES de importar la capa db

from concrete.db import session_scope, NodoRepository, SensorRepository, LecturaRepository


def main():
    ahora = datetime.now(timezone.utc)

    with session_scope() as s:
        nodo = NodoRepository(s).obtener_o_crear(mac="ACA70406E0-TEST", nombre="Nodo de prueba")
        sensor = SensorRepository(s).obtener_o_crear(nodo_id=nodo.nodo_id, nombre="Sensor_01")

        lr = LecturaRepository(s)
        lr.crear(sensor_id=sensor.sensor_id, fecha=ahora - timedelta(minutes=10),
                 temp=22.35, hum=52.96, numero_lectura=126)
        lr.crear(sensor_id=sensor.sensor_id, fecha=ahora,
                 temp=22.37, hum=53.01, numero_lectura=127)

        sensor_id = sensor.sensor_id  # guarda el id antes de cerrar la sesión

    # Consulta tipo "gráfica": lecturas del último día
    with session_scope() as s:
        filas = LecturaRepository(s).graficar(
            sensor_id, ahora - timedelta(days=1), ahora + timedelta(minutes=1)
        )
        print(f"Conexión OK. {len(filas)} lecturas encontradas:")
        for l in filas:
            print(f"  #{l.numero_lectura}  {l.fecha}  temp={l.temp}  hum={l.hum}")


if __name__ == "__main__":
    main()