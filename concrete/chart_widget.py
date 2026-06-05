import matplotlib.pyplot as plt

from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

    def plot_data(self, fechas, series):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.clear()
        for key, registros in series.items():
            ax.plot(fechas, registros, label=key)
        ax.set_xlabel("Fecha")
        # ax.set_ylabel("Temperatura")
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        self.fig.tight_layout()
        self.canvas.draw()
