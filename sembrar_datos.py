# sembrar_datos.py
"""
Inyector de datos EN TIEMPO REAL para probar el sistema.

Corre en bucle: cada minuto envía una lectura nueva por cada sensor, con
valores que varían suavemente (camino aleatorio), usando la misma función RPC
que el hardware. Déjalo corriendo en una terminal con el sistema abierto y
verás cómo aparecen los datos solos (la app se auto-refresca cada 30 s).

Ejecuta:  py sembrar_datos.py
Detén:    Ctrl+C
Sólo usa librería estándar (no instala nada).
"""

import json
import random
import time
import urllib.request
import urllib.error
from datetime import datetime

SUPABASE_URL = "https://scudsjezxywmbtqvhnnp.supabase.co"
API_KEY = "sb_publishable_DgUNinHbdO3Qp8Xq66NzwA_Bmlx8JtB"  # tu llave publishable

# Nodos y sus sensores a simular:
NODOS = {
    "ACA70406E001": ["Sensor_01", "Sensor_02"],
    "ACA70406E002": ["Sensor_01"],
    "ACA70406E003": ["Sensor_01", "Sensor_02", "Sensor_03"],
}

INTERVALO_SEG = 60   # 1 minuto entre rondas


def enviar(mac, sensor, temp, hum, numero_lectura):
    url = f"{SUPABASE_URL}/rest/v1/rpc/registrar_lectura"
    payload = {
        "p_mac": mac,
        "p_sensor": sensor,
        "p_temp": round(temp, 2),
        "p_hum": round(hum, 2),
        "p_numero_lectura": numero_lectura,
        # sin p_fecha -> el servidor usa la hora de recepción (ahora)
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                method="POST")
    req.add_header("apikey", API_KEY)
    req.add_header("Authorization", f"Bearer {API_KEY}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as resp:
        return resp.status


def main():
    print(f"Inyectando datos cada {INTERVALO_SEG}s. Ctrl+C para detener.\n")

    # Estado por sensor: valor actual + contador único (base = hora actual,
    # para que no choque con datos de corridas anteriores).
    base = int(time.time())
    estado = {}
    for mac, sensores in NODOS.items():
        for sensor in sensores:
            estado[(mac, sensor)] = {
                "temp": random.uniform(20.0, 26.0),
                "hum": random.uniform(45.0, 60.0),
                "n": base,
            }

    try:
        while True:
            hora = datetime.now().strftime("%H:%M:%S")
            enviadas = 0
            for (mac, sensor), st in estado.items():
                # Variación suave respecto al valor anterior, con límites realistas.
                st["temp"] = min(35.0, max(10.0, st["temp"] + random.uniform(-0.3, 0.3)))
                st["hum"] = min(95.0, max(20.0, st["hum"] + random.uniform(-0.6, 0.6)))
                st["n"] += 1
                try:
                    enviar(mac, sensor, st["temp"], st["hum"], st["n"])
                    enviadas += 1
                except urllib.error.HTTPError as e:
                    print(f"  ERROR HTTP {e.code}: {e.read().decode()}")
                    return
                except Exception as e:
                    print(f"  ERROR de conexión: {e}")
                    return
            print(f"[{hora}] {enviadas} lecturas enviadas. Próxima ronda en {INTERVALO_SEG}s…")
            time.sleep(INTERVALO_SEG)
    except KeyboardInterrupt:
        print("\nDetenido por el usuario.")


if __name__ == "__main__":
    main()