from PySide6 import QtWidgets
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, \
    QTableWidgetItem, QAbstractItemView, QSplitter, QHBoxLayout, QTableWidget

from concrete import conector
from concrete.chart_widget import ChartWidget
from ui.ui_data import Ui_data


class DataWidget(QWidget, Ui_data):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.widget_chart = ChartWidget()
        self.splitter = QSplitter()
        self.widget_table = QTableWidget()
        self.splitter.addWidget(self.widget_table)
        self.splitter.addWidget(self.widget_chart)
        self.layout().insertWidget(0, self.splitter)
        self.tarjeta = None
        self.sensores = []
        self.__signals()

    def __signals(self):
        self.fecha_inicial.dateTimeChanged.connect(self.consultar_datos)
        self.fecha_final.dateTimeChanged.connect(self.consultar_datos)

    def mostrar_datos(self, tarjeta, sensores):
        self.setWindowTitle(f'Datos de {tarjeta.nombre}')
        self.sensores = sensores
        self.consultar_datos()
        self.show()

    def consultar_datos(self):
        self.widget_table.setRowCount(0)

        # columnas
        headers = ["Fecha"]
        self.widget_table.setColumnCount(len(headers))
        self.widget_table.setHorizontalHeaderLabels(headers)
        series = {}
        fechas = []

        for sensor in self.sensores:
            series[sensor.tipo] = []
            # .astimezone() adjunta tu zona horaria local a la fecha del
            # selector, para que la comparación contra los datos en UTC sea
            # correcta (si no, habría un desfase de horas y saldría vacío).
            fecha_inicial = self.fecha_inicial.dateTime().toPython().astimezone()
            fecha_final = self.fecha_final.dateTime().toPython().astimezone()
            # Modelo nuevo: una lectura trae temp y hum juntas.
            # sensor.campo indica cuál de las dos usa este renglón.
            lecturas = conector.consultar_lecturas(
                sensor.sensor_id, fecha_inicial, fecha_final)

            # agregar columna
            col = self.widget_table.columnCount()
            self.widget_table.insertColumn(col)
            self.widget_table.setHorizontalHeaderItem(col, QTableWidgetItem(
                sensor.tipo))

            # construir índice de fechas existentes en la tabla
            filas_por_fecha = {}
            for row in range(self.widget_table.rowCount()):
                item = self.widget_table.item(row, 0)
                if item:
                    fecha_str = item.text()
                    filas_por_fecha[fecha_str] = row

            # escribir lecturas
            for reg in lecturas:
                valor = getattr(reg, sensor.campo)   # reg.temp o reg.hum
                if valor is None:
                    continue
                fecha_str = reg.fecha.strftime("%Y-%m-%d %H:%M")
                if fecha_str in filas_por_fecha:
                    row = filas_por_fecha[fecha_str]
                    item = QTableWidgetItem(f"{valor:.2f} {sensor.unidades}")
                    item.setTextAlignment(Qt.AlignRight)
                    self.widget_table.setItem(row, col, item)
                else:
                    row = self.widget_table.rowCount()
                    self.widget_table.insertRow(row)
                    self.widget_table.setItem(
                        row, 0, QTableWidgetItem(fecha_str))
                    item = QTableWidgetItem(f"{valor:.2f} {sensor.unidades}")
                    item.setTextAlignment(Qt.AlignRight)
                    self.widget_table.setItem(row, col, item)
                    filas_por_fecha[fecha_str] = row
                    fechas.append(reg.fecha)
                series[sensor.tipo].append(valor)
        if series:
            self.widget_chart.plot_data(fechas, series)
        self.widget_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.widget_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.widget_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.widget_table.verticalHeader().setVisible(False)
        self.widget_table.resizeColumnsToContents()
        header = self.widget_table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)