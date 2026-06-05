from PySide6.QtWidgets import (
    QMainWindow, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy,
    QWidget, QComboBox,
)

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
        self._ajustar_menu()
        self._crear_filtro()
        self.populate_dashboard()
        self.populate_with_mini()
        self.set_main_layout()
        self.__signals__()

    def __signals__(self):
        self.btn_grafico.toggled.connect(self.swap_layout)
        self.accion_dispositivo.triggered.connect(self.register_new)
        self.le_filtrar.textChanged.connect(self._aplicar_filtro)

    # ----- Limpieza del menú (en código; no se toca ui_main.py) -----
    def _ajustar_menu(self):
        self.menuAgregar.setTitle("Sensores")
        self.accion_dispositivo.setText("Administrar sensores")
        self.menuAgregar.removeAction(self.accion_grupo)   # "Grupo" ya no aplica
        self.le_filtrar.setPlaceholderText("Buscar por nombre…")

    # ----- Filtro por nodo (desplegable) dentro de la toolbar existente -----
    def _crear_filtro(self):
        self.cb_filtro = QComboBox()
        self.cb_filtro.setMinimumSize(0, 30)
        self.cb_filtro.setStyleSheet("background-color: white; color: black;")
        # Se inserta entre el botón de gráfico (0) y el buscador de texto.
        self.horizontalLayout.insertWidget(1, self.cb_filtro)
        self._cargar_filtro()
        self.cb_filtro.currentIndexChanged.connect(self._aplicar_filtro)

    def _cargar_filtro(self):
        anterior = self.cb_filtro.currentData() if self.cb_filtro.count() else None
        self.cb_filtro.blockSignals(True)
        self.cb_filtro.clear()
        self.cb_filtro.addItem("Todos los nodos", None)
        for nodo in conector.consultar_nodos():
            self.cb_filtro.addItem(nodo.nombre or nodo.mac, nodo.nodo_id)
        idx = self.cb_filtro.findData(anterior)
        self.cb_filtro.setCurrentIndex(idx if idx >= 0 else 0)
        self.cb_filtro.blockSignals(False)

    def _aplicar_filtro(self):
        self.populate_dashboard()
        self.populate_with_mini()

    def _nodo_seleccionado(self):
        return self.cb_filtro.currentData() if hasattr(self, "cb_filtro") else None

    def _tarjetas_filtradas(self):
        tarjetas = conector.consultar_tarjetas(self._nodo_seleccionado())
        texto = self.le_filtrar.text().strip().lower()
        if texto:
            tarjetas = [
                t for t in tarjetas
                if texto in (t.nombre or "").lower()
                or any(texto in (tag or "").lower() for tag in (t.tags or []))
            ]
        return tarjetas

    # ----- Layout -----
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
        tarjetas = self._tarjetas_filtradas()
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
        tarjetas = self._tarjetas_filtradas()
        for tarjeta in tarjetas:
            layout.addWidget(BoardMiniWidget(tarjeta))
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding))

    def register_new(self):
        Registro().exec()
        self._cargar_filtro()
        self.populate_dashboard()
        self.populate_with_mini()