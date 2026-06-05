# sembrar_datos.py
"""
Siembra datos de prueba: varios NODOS, cada uno con varios SENSORES, y para
cada sensor un historial de lecturas (temp/hum). Usa la MISMA función RPC que
el hardware, así que valida todo el camino y crea nodos/sensores solos.

Ejecuta:  py sembrar_datos.py
Sólo usa librería estándar (no instalas nada). Re-ejecutarlo es seguro:
las lecturas repetidas se ignoran por la restricción UNIQUE.
"""

import json
import random
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

SUPABASE_URL = "https://scudsjezxywmbtqvhnnp.supabase.co"
API_KEY = "sb_publishable_DgUNinHbdO3Qp8Xq66NzwA_Bmlx8JtB"  # tu llave publishable

# Define los nodos (MAC) y qué sensores cuelga cada uno:
NODOS = {
    "ACA70406E001": ["Sensor_01", "Sensor_02"],
    "ACA70406E002": ["Sensor_01"],
    "ACA70406E003": ["Sensor_01", "Sensor_02", "Sensor_03"],
}

N_LECTURAS = 12                       # puntos de historial por sensor
INTERVALO = timedelta(minutes=10)     # separación entre lecturas


def enviar(mac, sensor, temp, hum, fecha, numero_lectura):
    url = f"{SUPABASE_URL}/rest/v1/rpc/registrar_lectura"
    payload = {
        "p_mac": mac,
        "p_sensor": sensor,
        "p_temp": round(temp, 2),
        "p_hum": round(hum, 2),
        "p_fecha": fecha.isoformat(),
        "p_numero_lectura": numero_lectura,
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                method="POST")
    req.add_header("apikey", API_KEY)
    req.add_header("Authorization", f"Bearer {API_KEY}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as resp:
        return resp.status


def main():
    ahora = datetime.now(timezone.utc)
    total = 0
    for mac, sensores in NODOS.items():
        for sensor in sensores:
            base_t = random.uniform(20.0, 26.0)
            base_h = random.uniform(45.0, 60.0)
            for i in range(N_LECTURAS):
                fecha = ahora - INTERVALO * (N_LECTURAS - 1 - i)
                temp = base_t + random.uniform(-0.5, 0.5)
                hum = base_h + random.uniform(-1.0, 1.0)
                try:
                    enviar(mac, sensor, temp, hum, fecha, numero_lectura=i + 1)
                    total += 1
                except urllib.error.HTTPError as e:
                    print(f"ERROR HTTP {e.code}: {e.read().decode()}")
                    return
            print(f"  {mac} / {sensor}: {N_LECTURAS} lecturas")
    print(f"\nListo. {total} lecturas enviadas en {len(NODOS)} nodos.")


if __name__ == "__main__":
    main()