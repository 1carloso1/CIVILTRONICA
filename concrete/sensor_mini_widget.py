from PySide6.QtGui import QFont, Qt, QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout

from ui import resources_rc

class SensorMiniWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

    def add_sensor(self, sensor):
        if sensor.dato is not None:
            dato = f"{sensor.dato:.2f}"
        else:
            dato = "—"
        labels = {
            'icon': QLabel(),
            # 'tipo': QLabel(sensor.tipo),
            'dato': QLabel(dato),
            'unidades': QLabel(sensor.unidades),
        }
        translate_icons = {
            'temperatura': 'temperature',
            'humedad': 'humidity',
        }
        labels['icon'].setPixmap(QPixmap(
            f":/sensor/icons/{translate_icons.get(sensor.tipo.lower())}.png"))
        labels['icon'].setMaximumSize(30, 30)
        labels['icon'].setScaledContents(True)
        for index, (key, label) in enumerate(labels.items()):
            label.setFont(QFont("Inter", 11))
            self.layout().addWidget(label)
        labels['dato'].setFont(QFont("Menlo", 12))
        labels['dato'].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
