# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'board_mini.ui'
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
    QSizePolicy, QSpacerItem, QWidget)
from . import resources_rc

class Ui_board_mini(object):
    def setupUi(self, board_mini):
        if not board_mini.objectName():
            board_mini.setObjectName(u"board_mini")
        board_mini.resize(384, 78)
        board_mini.setMaximumSize(QSize(16777215, 78))
        board_mini.setStyleSheet(u"QFrame#mini_frame{\n"
"	border-radius: 10px;\n"
"	background-color: #1f1f23;\n"
"}\n"
"\n"
"QFrame#mini_frame:hover{\n"
"	background-color: #333333;\n"
"}\n"
"\n"
"QLabel{\n"
"	color: white;\n"
"}")
        self.horizontalLayout = QHBoxLayout(board_mini)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.mini_frame = QFrame(board_mini)
        self.mini_frame.setObjectName(u"mini_frame")
        self.mini_frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.mini_frame.setFrameShape(QFrame.StyledPanel)
        self.mini_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.mini_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lbl_tarjeta = QLabel(self.mini_frame)
        self.lbl_tarjeta.setObjectName(u"lbl_tarjeta")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_tarjeta.sizePolicy().hasHeightForWidth())
        self.lbl_tarjeta.setSizePolicy(sizePolicy)
        self.lbl_tarjeta.setPixmap(QPixmap(u":/board/images/board_small.png"))

        self.horizontalLayout_2.addWidget(self.lbl_tarjeta)

        self.lbl_nombre = QLabel(self.mini_frame)
        self.lbl_nombre.setObjectName(u"lbl_nombre")
        font = QFont()
        font.setFamilies([u"Inter"])
        font.setPointSize(12)
        self.lbl_nombre.setFont(font)

        self.horizontalLayout_2.addWidget(self.lbl_nombre)

        self.widget_tags = QWidget(self.mini_frame)
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
        self.horizontalLayout_3 = QHBoxLayout(self.widget_tags)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_2.addWidget(self.widget_tags)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.widget_sensores = QWidget(self.mini_frame)
        self.widget_sensores.setObjectName(u"widget_sensores")

        self.horizontalLayout_2.addWidget(self.widget_sensores)


        self.horizontalLayout.addWidget(self.mini_frame)


        self.retranslateUi(board_mini)

        QMetaObject.connectSlotsByName(board_mini)
    # setupUi

    def retranslateUi(self, board_mini):
        board_mini.setWindowTitle(QCoreApplication.translate("board_mini", u"Form", None))
        self.lbl_tarjeta.setText("")
        self.lbl_nombre.setText(QCoreApplication.translate("board_mini", u"Nombre", None))
    # retranslateUi

