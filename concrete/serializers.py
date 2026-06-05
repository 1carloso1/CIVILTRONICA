import json

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


#Turns the object into a dictionary and JSON
class JsonMixin:

    @property
    def diccionario(self):
        diccionario = {}
        for key, value in self.__dict__.items():

            if isinstance(value, JsonMixin):
                value = value.diccionario

            elif isinstance(value, datetime):
                value = value.isoformat(sep=' ', timespec='seconds')

            diccionario[key.lstrip('_')] = value

        return diccionario

#Llena el objeto desde un diccionario
class MapperMixin(ABC):

    # Override this per model if needed
    @staticmethod
    def special_fields():
        return {}  # db_key -> converter_function

    def update_from_dict(self, data):
        for db_key, python_attr in self.map_to_db_fields().items():
            if db_key not in data:
                continue

            value = data[db_key]

            converters = self.special_fields()
            if db_key in converters:
                try:
                    value = converters[db_key](value)
                except Exception:
                    pass

            # Convert ISO timestamps
            if isinstance(value, str):
                try:
                    from datetime import datetime
                    value = datetime.fromisoformat(value)
                except ValueError:
                    pass

            setattr(self, python_attr, value)

    @staticmethod
    @abstractmethod
    def map_to_db_fields():
        """Subclasses must implement this method to provide field mappings."""
        pass


# =====================================================================
#  MODELO NUEVO:  Nodo -> Sensor -> Lectura
# =====================================================================

@dataclass
class Nodo(JsonMixin, MapperMixin):

    nodo_id: int = 0
    mac: str = ''
    nombre: str = ''

    def __init__(self, nodo_id=0, mac='', nombre=''):
        self.nodo_id = nodo_id
        self.mac = mac
        self.nombre = nombre

    @staticmethod
    def map_to_db_fields():
        return {
            'nodo_id': 'nodo_id',
            'mac': 'mac',
            'nombre': 'nombre',
        }


@dataclass
class Sensor(JsonMixin, MapperMixin):

    sensor_id: int = 0
    nodo_id: int = None
    nombre: str = ''

    def __init__(self, sensor_id=0, nodo_id=None, nombre=''):
        self.sensor_id = sensor_id
        self.nodo_id = nodo_id
        self.nombre = nombre

    @staticmethod
    def map_to_db_fields():
        return {
            'sensor_id': 'sensor_id',
            'nodo_id': 'nodo_id',
            'nombre': 'nombre',
        }


@dataclass
class Lectura(JsonMixin, MapperMixin):

    lectura_id: int = 0
    sensor_id: int = None
    numero_lectura: int = None
    fecha: datetime = None
    temp: float = None
    hum: float = None

    def __init__(self, lectura_id=0, sensor_id=None, numero_lectura=None,
                 fecha=None, temp=None, hum=None):
        self.lectura_id = lectura_id
        self.sensor_id = sensor_id
        self.numero_lectura = numero_lectura
        self.fecha = fecha
        self.temp = temp
        self.hum = hum

    @staticmethod
    def map_to_db_fields():
        return {
            'lectura_id': 'lectura_id',
            'sensor_id': 'sensor_id',
            'numero_lectura': 'numero_lectura',
            'fecha': 'fecha',
            'temp': 'temp',
            'hum': 'hum',
        }


# =====================================================================
#  MODELO VIEJO (en desuso, se conservan para no romper imports antiguos)
# =====================================================================

@dataclass
class Tarjeta(JsonMixin, MapperMixin):

    tarjeta_id: int = 0
    nombre: str = ''
    id_fisico: str = ''
    grupo_id: int = None
    tags: list = None

    def __init__(self, tarjeta_id=0, id_fisico='', nombre="", grupo_id=None, tags=None):
        self.tarjeta_id = tarjeta_id
        self.id_fisico = id_fisico
        self.nombre = nombre
        self.grupo_id = grupo_id
        self.tags = tags

    @staticmethod
    def map_to_db_fields():
        return {
            'tarjeta_id': 'tarjeta_id',
            'id_fisico': 'id_fisico',
            'nombre': 'nombre',
            'grupo_id': 'grupo_id',
            'tags': 'tags',
        }

    @staticmethod
    def special_fields():
        return {
            'tags': lambda t: [s.strip() for s in t.split(',')] if t else []
        }


@dataclass
class Registro(JsonMixin, MapperMixin):

    registro_id: int = 0
    sensor_id: int = None
    fecha: datetime = None
    dato: float = None

    def __init__(self, registro_id=0, sensor_id=None, fecha=None, dato=None):
        self.registro_id = registro_id
        self.sensor_id = sensor_id
        self.fecha = fecha
        self.dato = dato

    @staticmethod
    def map_to_db_fields():
        return {
            'registro_id': 'registro_id',
            'sensor_id': 'sensor_id',
            'fecha': 'fecha',
            'dato': 'dato',
        }


@dataclass
class Grupo(JsonMixin, MapperMixin):

    grupo_id: int = 0
    nombre: str = ''

    def __init__(self, grupo_id=0, nombre=''):
        self.grupo_id = grupo_id
        self.nombre = nombre

    @staticmethod
    def map_to_db_fields():
        return {
            'grupo_id': 'grupo_id',
            'grupo_nombre': 'nombre',
        }