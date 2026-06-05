from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox, QLineEdit,
    QPushButton, QLabel, QMessageBox,
)

from concrete import conector


class Registro(QDialog):
    """
    Gestor de sensores: pone nombre amigable (alias) al sensor, nombra su nodo
    (grupo) y permite eliminar sensores o nodos completos. La creación de
    nodos/sensores la hace el hardware al enviar datos; aquí sólo se administran.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sensores / Nodos")
        self.setMinimumWidth(460)
        self._construir_ui()
        self._signals()
        self._cargar()

    def _construir_ui(self):
        layout = QVBoxLayout(self)

        form = QFormLayout()
        self.cb_sensor = QComboBox()
        self.le_nodo = QLineEdit()
        self.le_nodo.setPlaceholderText("Ej. Receptor Obra A")
        self.le_alias = QLineEdit()
        self.le_alias.setPlaceholderText("Ej. Losa Norte - Piso 3")
        form.addRow("Sensor:", self.cb_sensor)
        form.addRow("Nombre del nodo (grupo):", self.le_nodo)
        form.addRow("Nombre del sensor (losa):", self.le_alias)
        layout.addLayout(form)

        self.lbl_info = QLabel()
        self.lbl_info.setStyleSheet("color: #666;")
        self.lbl_info.setWordWrap(True)
        layout.addWidget(self.lbl_info)

        self.lbl_error = QLabel()
        self.lbl_error.setStyleSheet("color: #c0392b;")
        self.lbl_error.setVisible(False)
        layout.addWidget(self.lbl_error)

        self.btn_guardar = QPushButton("Guardar nombres")
        layout.addWidget(self.btn_guardar)

        # Botones de eliminación (con estilo discreto)
        fila_borrar = QHBoxLayout()
        self.btn_del_sensor = QPushButton("Eliminar sensor")
        self.btn_del_nodo = QPushButton("Eliminar nodo completo")
        for b in (self.btn_del_sensor, self.btn_del_nodo):
            b.setStyleSheet("color: #c0392b;")
            fila_borrar.addWidget(b)
        layout.addLayout(fila_borrar)

    def _signals(self):
        self.cb_sensor.currentIndexChanged.connect(self._on_changed)
        self.btn_guardar.clicked.connect(self._guardar)
        self.btn_del_sensor.clicked.connect(self._eliminar_sensor)
        self.btn_del_nodo.clicked.connect(self._eliminar_nodo)

    def _cargar(self):
        self.cb_sensor.blockSignals(True)
        self.cb_sensor.clear()
        sensores = conector.consultar_sensores()
        for s in sensores:
            etiqueta = f"{s.nodo_nombre or s.mac}  ·  {s.alias or s.nombre}"
            self.cb_sensor.addItem(etiqueta, s)
        self.cb_sensor.blockSignals(False)

        hay = bool(sensores)
        for w in (self.le_nodo, self.le_alias, self.btn_guardar,
                  self.btn_del_sensor, self.btn_del_nodo):
            w.setEnabled(hay)

        if not hay:
            self.lbl_info.setText(
                "No hay sensores. Aparecerán cuando el hardware envíe su "
                "primera lectura."
            )
            self.le_nodo.clear()
            self.le_alias.clear()
            return
        self._on_changed()

    def _on_changed(self):
        s = self.cb_sensor.currentData()
        if s is None:
            return
        self.le_nodo.setText(s.nodo_nombre or "")
        self.le_alias.setText(s.alias or "")
        self.lbl_info.setText(
            f"MAC del nodo: {s.mac}    |    Sensor (hardware): {s.nombre}"
        )
        self.lbl_error.setVisible(False)

    def _guardar(self):
        s = self.cb_sensor.currentData()
        if s is None:
            return
        conector.renombrar_sensor(s.sensor_id, self.le_alias.text().strip() or None)
        conector.renombrar_nodo(s.nodo_id, self.le_nodo.text().strip() or None)
        self.accept()

    def _eliminar_sensor(self):
        s = self.cb_sensor.currentData()
        if s is None:
            return
        nombre = s.alias or s.nombre
        if self._confirmar(f"¿Eliminar el sensor «{nombre}» y TODAS sus lecturas?\n"
                           "Esta acción no se puede deshacer."):
            conector.eliminar_sensor(s.sensor_id)
            self._cargar()

    def _eliminar_nodo(self):
        s = self.cb_sensor.currentData()
        if s is None:
            return
        etiqueta = s.nodo_nombre or s.mac
        if self._confirmar(f"¿Eliminar el NODO «{etiqueta}» con TODOS sus sensores "
                           "y lecturas?\nEsta acción no se puede deshacer."):
            conector.eliminar_nodo(s.nodo_id)
            self._cargar()

    def _confirmar(self, texto):
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle("Confirmar eliminación")
        box.setText(texto)
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        box.setDefaultButton(QMessageBox.No)
        box.setStyleSheet("color: black")
        return box.exec() == QMessageBox.Yes