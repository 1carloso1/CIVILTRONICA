# Changelog

## Migración a Supabase/PostgreSQL y rediseño del modelo

Migración completa de la persistencia de **MySQL local** a **PostgreSQL en la
nube (Supabase)**, con rediseño del modelo de datos y mejoras de interfaz e
ingesta desde hardware.

---

### Base de datos (Supabase / PostgreSQL)
- **Nuevo modelo** `nodo → sensor → lectura` en reemplazo de
  `grupo / tarjeta / tipo / registro`. El nodo es el receptor que agrupa
  sensores; cada lectura trae temperatura y humedad juntas.
- `TIMESTAMPTZ` para las fechas e **índice compuesto** `(sensor_id, fecha DESC)`
  para que las consultas por rango (gráficas) sean rápidas.
- Columna **`alias`** en `sensor` (nombre amigable, sin afectar el nombre de
  hardware con el que se emparejan las lecturas).
- **RLS activado** + función **RPC `registrar_lectura`** para la ingesta del
  hardware (autocrea nodo/sensor por MAC y nombre).
- *Justificación:* acceso remoto desde la nube, modelo acorde a los datos
  reales y consultas de series de tiempo optimizadas.

### Capa de datos (Python) — nueva, en `concrete/db/`
- `engine.py`: conexión que lee `DATABASE_URL` del `.env`. Único archivo que
  conoce el proveedor → cambiar de Supabase a self-hosted es sólo editar el
  `.env`.
- `models.py`: modelos ORM (Nodo, Sensor, Lectura) con SQLAlchemy 2.0.
- `repositories.py`: patrón Repositorio (consultas y escrituras por entidad).
- `__init__.py`: expone la capa.
- `conector.py` **reescrito** como *facade* sobre SQLAlchemy/PostgreSQL,
  conservando la API que usa la interfaz para no reescribir los widgets.

### Interfaz (aplicación de escritorio)
- `main.py`: se agregó `load_dotenv()` al inicio (carga la cadena de conexión
  antes de tocar la base).
- `serializers.py`: se agregaron `Nodo`, `Sensor` (nuevo) y `Lectura`.
- `main_window.py`:
  - Dashboard muestra **una tarjeta por sensor**; el nodo aparece como
    agrupación (etiqueta).
  - **Filtro por nodo** + **búsqueda por texto**.
  - Limpieza del menú: "Administrar sensores" (antes "Dispositivo"), se quitó
    "Grupo".
  - **Ventana de tamaño fijo**, 2 columnas y **scroll vertical**.
  - Corrección del **parpadeo** al arrancar (la ventana se muestra ya armada).
- `data.py` **reescrito**:
  - Historial con **dos series** (temperatura y humedad) de una sola consulta.
  - Manejo de **zona horaria**: se guarda en UTC, se muestra en hora local.
  - **Rango de fechas automático** (primer–último registro del sensor).
  - **Filtrado en memoria** (mover el rango ya no consulta la nube).
  - **Cursor de "cargando"** al abrir un sensor.
  - Columna **No. señal** y **tabla ajustada al contenido** (sin scroll
    horizontal ni margen vacío).
- `registro.py` **reescrito**: pasó de "agregar dispositivo/grupo" a
  **administrar sensores**: etiquetar (alias), nombrar el nodo y **eliminar**
  sensores o nodos. *(El hardware ya crea nodos/sensores solo.)*

### Hardware / ingesta
- `GUIA_HARDWARE.md`: documento de integración (endpoint, llave publishable,
  formato JSON, ejemplo para ESP32/Arduino).

### Eliminado / obsoleto
- Modelo de grupos (tablas `grupo`, `tarjeta`, `tipo`, `registro`).
- Funciones `consultar_grupos`, `agregar_tarjeta`, `agregar_sensor`.
- Acción de menú "Grupo".
- En `serializers.py` quedan obsoletas las clases `Grupo` y `Registro`
  (pueden eliminarse).

---
