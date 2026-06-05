# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sensor.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QWidget)
from . import resources_rc

class Ui_sensor(object):
    def setupUi(self, sensor):
        if not sensor.objectName():
            sensor.setObjectName(u"sensor")
        sensor.resize(252, 48)
        self.gridLayout = QGridLayout(sensor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, -1, 0, -1)
        self.lbl_icon = QLabel(sensor)
        self.lbl_icon.setObjectName(u"lbl_icon")
        self.lbl_icon.setMaximumSize(QSize(30, 30))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        self.lbl_icon.setFont(font)
        self.lbl_icon.setPixmap(QPixmap(u":/sensor/icons/temperature.png"))
        self.lbl_icon.setScaledContents(True)

        self.gridLayout.addWidget(self.lbl_icon, 0, 0, 1, 1)

        self.lbl_type = QLabel(sensor)
        self.lbl_type.setObjectName(u"lbl_type")
        font1 = QFont()
        font1.setFamilies([u"Inter"])
        font1.setPointSize(11)
        self.lbl_type.setFont(font1)

        self.gridLayout.addWidget(self.lbl_type, 0, 1, 1, 1)

        self.lbl_value = QLabel(sensor)
        self.lbl_value.setObjectName(u"lbl_value")
        font2 = QFont()
        font2.setFamilies([u"Menlo"])
        font2.setPointSize(12)
        self.lbl_value.setFont(font2)
        self.lbl_value.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lbl_value, 0, 2, 1, 1)

        self.lbl_units = QLabel(sensor)
        self.lbl_units.setObjectName(u"lbl_units")
        self.lbl_units.setFont(font1)

        self.gridLayout.addWidget(self.lbl_units, 0, 3, 1, 1)


        self.retranslateUi(sensor)

        QMetaObject.connectSlotsByName(sensor)
    # setupUi

    def retranslateUi(self, sensor):
        sensor.setWindowTitle(QCoreApplication.translate("sensor", u"Form", None))
        self.lbl_type.setText(QCoreApplication.translate("sensor", u"Type", None))
        self.lbl_value.setText(QCoreApplication.translate("sensor", u"Value", None))
        self.lbl_units.setText(QCoreApplication.translate("sensor", u"Units", None))
    # retranslateUi

