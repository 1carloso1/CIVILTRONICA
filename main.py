import sys

from dotenv import load_dotenv
load_dotenv()

from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QGuiApplication, QPalette, QColor
from PySide6 import QtXml

from concrete.main_window import MainWindow



app = QApplication(sys.argv)
app.setStyle(QStyleFactory.create("Fusion"))

# Force light palette
palette = QPalette()
palette.setColor(QPalette.Window, QColor(255, 255, 255))
palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
palette.setColor(QPalette.Base, QColor(255, 255, 255))
palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
palette.setColor(QPalette.Text, QColor(0, 0, 0))
palette.setColor(QPalette.Button, QColor(240, 240, 240))
palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
app.setPalette(palette)
concrete = MainWindow()
# concrete.installEventFilter(concrete)
sys.exit(app.exec())
