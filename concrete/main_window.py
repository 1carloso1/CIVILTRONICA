from PySide6.QtWidgets import QMainWindow, QGridLayout, QVBoxLayout, \
    QSpacerItem, QSizePolicy, QWidget

from concrete import conector
from concrete.board_widget import BoardMiniWidget
from concrete.board_widget import BoardWidget
from concrete.registro import Registro
from concrete.sensor_widget import SensorWidget
from ui.ui_main import Ui_main


class MainWindow(QMainWindow, Ui_main):

    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.show()
        self.widget_boards = QWidget()
        self.widget_mini_boards = QWidget()
        self.populate_dashboard()
        self.populate_with_mini()
        self.set_main_layout()
        self.__signals__()

    def __signals__(self):
        self.btn_grafico.toggled.connect(self.swap_layout)
        self.accion_dispositivo.triggered.connect(self.register_new)

    def set_main_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.widget_boards)
        layout.addWidget(self.widget_mini_boards)
        self.scroll_area_contents.setLayout(layout)
        self.widget_mini_boards.setVisible(False)

    def swap_layout(self):
        self.widget_boards.setVisible(not self.widget_boards.isVisible())
        self.widget_mini_boards.setVisible(not self.widget_mini_boards.isVisible())

    def populate_dashboard(self):
        layout = self.widget_boards.layout()
        if layout is None:
            layout = QGridLayout(self.widget_boards)
            self.widget_boards.setLayout(layout)
        self.clear_layout(layout)
        tarjetas = conector.consultar_tarjetas()
        columns = 3
        for i, tarjeta in enumerate(tarjetas):
            row = i // columns
            col = i % columns
            layout.addWidget(BoardWidget(tarjeta), row, col)

    @staticmethod
    def clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def populate_with_mini(self):
        layout = self.widget_mini_boards.layout()
        if layout is None:
            layout = QVBoxLayout(self.widget_mini_boards)
            layout.setSpacing(1)
            self.widget_mini_boards.setLayout(layout)
        self.clear_layout(layout)
        tarjetas = conector.consultar_tarjetas()
        for tarjeta in tarjetas:
            layout.addWidget(BoardMiniWidget(tarjeta))
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding))

    def register_new(self):
        registro = Registro()
        if registro.exec():
            self.populate_dashboard()
            self.populate_with_mini()
