# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data.ui'
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
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QHBoxLayout, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_data(object):
    def setupUi(self, data):
        if not data.objectName():
            data.setObjectName(u"data")
        data.resize(869, 561)
        self.verticalLayout = QVBoxLayout(data)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.fecha_inicial = QDateTimeEdit(data)
        self.fecha_inicial.setObjectName(u"fecha_inicial")
        font = QFont()
        font.setFamilies([u"Inter"])
        font.setPointSize(11)
        self.fecha_inicial.setFont(font)
        self.fecha_inicial.setDateTime(QDateTime(QDate(2025, 11, 19), QTime(0, 0, 0)))
        self.fecha_inicial.setDate(QDate(2025, 11, 19))
        self.fecha_inicial.setCalendarPopup(True)

        self.horizontalLayout_2.addWidget(self.fecha_inicial)

        self.fecha_final = QDateTimeEdit(data)
        self.fecha_final.setObjectName(u"fecha_final")
        self.fecha_final.setFont(font)
        self.fecha_final.setDateTime(QDateTime(QDate(2025, 11, 21), QTime(0, 0, 0)))
        self.fecha_final.setCalendarPopup(True)

        self.horizontalLayout_2.addWidget(self.fecha_final)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(data)

        QMetaObject.connectSlotsByName(data)
    # setupUi

    def retranslateUi(self, data):
        data.setWindowTitle(QCoreApplication.translate("data", u"Datos", None))
    # retranslateUi

