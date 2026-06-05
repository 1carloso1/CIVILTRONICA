from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, \
    QSizePolicy, QHBoxLayout

from concrete import conector
from concrete.data import DataWidget
from concrete.sensor_mini_widget import SensorMiniWidget
from concrete.sensor_widget import SensorWidget
from ui.ui_board import Ui_board
from ui.ui_board_mini import Ui_board_mini


class BaseBoardWidget(QWidget):

    def __init__(self, tarjeta, parent=None):
        super().__init__(parent)
        self.tarjeta = tarjeta
        self.sensores = conector.consultar_sensores_por_tarjeta(
            self.tarjeta.tarjeta_id
        )
        self.data_widget = DataWidget()

    def mostrar_datos(self, event):
        self.data_widget.mostrar_datos(self.tarjeta, self.sensores)
        event.accept()

    def set_common_ui(self, lbl_nombre, widget_tags):
        lbl_nombre.setText(self.tarjeta.nombre)
        layout = widget_tags.layout()
        for tag in self.tarjeta.tags:
            label = QLabel(tag)
            self.customize_tag_label(label)   # hook
            layout.insertWidget(layout.count() - 1, label)

    # Hook for subclasses
    def customize_tag_label(self, label):
        pass

    # Shared helper
    def populate_common_board(self, widget_sensores):
        layout = self.make_layout()           # hook
        sensor_widget = self.make_sensor_widget()  # hook
        for sensor in self.sensores:
            sensor_widget.add_sensor(sensor)
        layout.addWidget(sensor_widget)
        widget_sensores.setLayout(layout)

    # Hooks
    def make_layout(self):
        raise NotImplementedError()

    def make_sensor_widget(self):
        raise NotImplementedError()


class BoardWidget(BaseBoardWidget, Ui_board):

    def __init__(self, tarjeta, parent=None):
        super().__init__(tarjeta, parent)
        self.setupUi(self)
        self.set_common_ui(self.lbl_nombre, self.widget_tags)
        self.populate_common_board(self.widget_sensores)
        self.btn_historial.setVisible(False)
        self.__signals()

    def __signals(self):
        self.card_frame.mouseReleaseEvent = self.mostrar_datos

    def make_layout(self):
        return QVBoxLayout()

    def make_sensor_widget(self):
        return SensorWidget()


class BoardMiniWidget(BaseBoardWidget, Ui_board_mini):

    def __init__(self, tarjeta, parent=None):
        super().__init__(tarjeta, parent)
        self.setupUi(self)
        self.set_common_ui(self.lbl_nombre, self.widget_tags)
        self.populate_common_board(self.widget_sensores)
        self.__signals()

    def __signals(self):
        self.mini_frame.mouseReleaseEvent = self.mostrar_datos

    def customize_tag_label(self, label):
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def make_layout(self):
        return QHBoxLayout()

    def make_sensor_widget(self):
        return SensorMiniWidget()
