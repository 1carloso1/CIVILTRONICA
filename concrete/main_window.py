from PySide6.QtCore import Qt
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


ANCHO_VENTANA = 820       # ancho fijo de la ventana
ALTO_VENTANA = 640        # alto fijo (pensado para ver ~4 tarjetas: 2 filas)
COLUMNAS = 2              # tarjetas por fila -> 2 columnas x 2 filas = 4 a la vista


class MainWindow(QMainWindow, Ui_main):

    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.widget_boards = QWidget()
        self.widget_mini_boards = QWidget()
        self._ajustar_menu()
        self._configurar_ventana()
        self._crear_filtro()
        self.set_main_layout()
        self.__signals__()
        self.show()
        self._cargar_filtro()
        self.populate_dashboard()
        self.populate_with_mini()

    def __signals__(self):
        self.btn_grafico.toggled.connect(self.swap_layout)
        self.accion_dispositivo.triggered.connect(self.register_new)
        self.le_filtrar.textChanged.connect(self._aplicar_filtro)

    # ----- Tamaño fijo + scroll vertical -----
    def _configurar_ventana(self):
        # Tamaño fijo: ya no se puede estirar con el mouse ni crece con el contenido.
        self.setFixedSize(ANCHO_VENTANA, ALTO_VENTANA)
        # El contenido que no cabe se navega con scroll vertical (sin scroll horizontal).
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    # ----- Limpieza del menú -----
    def _ajustar_menu(self):
        self.menuAgregar.setTitle("Sensores")
        self.accion_dispositivo.setText("Administrar sensores")
        self.menuAgregar.removeAction(self.accion_grupo)
        self.le_filtrar.setPlaceholderText("Buscar por nombre…")

    # ----- Filtro por nodo -----
    def _crear_filtro(self):
        self.cb_filtro = QComboBox()
        self.cb_filtro.setMinimumSize(0, 30)
        self.cb_filtro.setStyleSheet("background-color: white; color: black;")
        self.horizontalLayout.insertWidget(1, self.cb_filtro)
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
        for i, tarjeta in enumerate(tarjetas):
            row = i // COLUMNAS
            col = i % COLUMNAS
            layout.addWidget(BoardWidget(tarjeta), row, col)
        # Empuja las tarjetas hacia arriba para que el scroll se vea natural.
        layout.setRowStretch(layout.rowCount(), 1)

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