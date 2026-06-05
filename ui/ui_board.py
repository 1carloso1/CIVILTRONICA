# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'board.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
from . import resources_rc

class Ui_board(object):
    def setupUi(self, board):
        if not board.objectName():
            board.setObjectName(u"board")
        board.resize(288, 244)
        board.setMinimumSize(QSize(288, 244))
        board.setStyleSheet(u"QFrame#card_frame{\n"
"	border-radius: 10px;\n"
"	background-color: #1f1f23;\n"
"}\n"
"\n"
"QFrame#card_frame:hover{\n"
"	background-color: #333333;\n"
"}\n"
"\n"
"QLabel{\n"
"	color: white;\n"
"}")
        self.verticalLayout = QVBoxLayout(board)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.card_frame = QFrame(board)
        self.card_frame.setObjectName(u"card_frame")
        self.card_frame.setMinimumSize(QSize(282, 238))
        self.card_frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.card_frame.setFrameShape(QFrame.StyledPanel)
        self.card_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.card_frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lbl_nombre = QLabel(self.card_frame)
        self.lbl_nombre.setObjectName(u"lbl_nombre")
        font = QFont()
        font.setFamilies([u"Inter"])
        font.setPointSize(14)
        font.setBold(True)
        self.lbl_nombre.setFont(font)

        self.horizontalLayout_4.addWidget(self.lbl_nombre)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.btn_historial = QPushButton(self.card_frame)
        self.btn_historial.setObjectName(u"btn_historial")
        font1 = QFont()
        font1.setFamilies([u"Inter"])
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.btn_historial.setFont(font1)
        self.btn_historial.setStyleSheet(u"QPushButton{\n"
"	padding: 3px 14px;\n"
"	border-radius: 5px;\n"
"	color: black;\n"
"	font: 11pt \"Inter\";\n"
"}\n"
"")

        self.horizontalLayout_4.addWidget(self.btn_historial)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.widget_tags = QWidget(self.card_frame)
        self.widget_tags.setObjectName(u"widget_tags")
        self.widget_tags.setStyleSheet(u"QLabel{\n"
"	font: 9pt \"Inter\";\n"
"	padding: 3px;\n"
"	color: white;\n"
"	background-color: #666;\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"QLabel:hover{\n"
"	background-color: #555;\n"
"}")
        self.horizontalLayout = QHBoxLayout(self.widget_tags)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addWidget(self.widget_tags)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.lbl_tarjeta = QLabel(self.card_frame)
        self.lbl_tarjeta.setObjectName(u"lbl_tarjeta")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_tarjeta.sizePolicy().hasHeightForWidth())
        self.lbl_tarjeta.setSizePolicy(sizePolicy)
        self.lbl_tarjeta.setMinimumSize(QSize(260, 181))
        self.lbl_tarjeta.setPixmap(QPixmap(u":/board/images/board.png"))

        self.verticalLayout_2.addWidget(self.lbl_tarjeta)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.widget_sensores = QWidget(self.card_frame)
        self.widget_sensores.setObjectName(u"widget_sensores")

        self.verticalLayout_2.addWidget(self.widget_sensores)


        self.verticalLayout.addWidget(self.card_frame)


        self.retranslateUi(board)

        QMetaObject.connectSlotsByName(board)
    # setupUi

    def retranslateUi(self, board):
        board.setWindowTitle(QCoreApplication.translate("board", u"Form", None))
        self.lbl_nombre.setText(QCoreApplication.translate("board", u"Nombre", None))
        self.btn_historial.setText(QCoreApplication.translate("board", u"Historial", None))
        self.lbl_tarjeta.setText("")
    # retranslateUi

