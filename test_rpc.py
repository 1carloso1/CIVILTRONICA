# test_rpc.py
"""
Simula el POST de un sensor a la función RPC de Supabase.
Sólo usa librería estándar (no requiere instalar nada).
Ejecuta:  py test_rpc.py
"""

import json
import urllib.request
import urllib.error

SUPABASE_URL = "https://scudsjezxywmbtqvhnnp.supabase.co"
API_KEY = "sb_publishable_DgUNinHbdO3Qp8Xq66NzwA_Bmlx8JtB"  # tu llave publishable


def enviar_lectura(mac, sensor, temp, hum, numero_lectura=None):
    url = f"{SUPABASE_URL}/rest/v1/rpc/registrar_lectura"
    payload = {
        "p_mac": mac,
        "p_sensor": sensor,
        "p_temp": temp,
        "p_hum": hum,
        "p_numero_lectura": numero_lectura,
    }
    body = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("apikey", API_KEY)
    req.add_header("Authorization", f"Bearer {API_KEY}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req) as resp:
            print(f"OK  HTTP {resp.status}")
            print("Respuesta (lectura_id):", resp.read().decode() or "(vacío)")
    except urllib.error.HTTPError as e:
        print(f"ERROR HTTP {e.code}")
        print(e.read().decode())
    except Exception as e:
        print("ERROR de conexión:", e)


if __name__ == "__main__":
    enviar_lectura("ACA70406E0123", "Sensor_01", 22.35, 52.96, 128)