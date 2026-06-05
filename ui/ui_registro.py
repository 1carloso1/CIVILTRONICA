# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'registro.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_registro(object):
    def setupUi(self, registro):
        if not registro.objectName():
            registro.setObjectName(u"registro")
        registro.resize(389, 328)
        registro.setStyleSheet(u"QWidget#registro{\n"
"	background-color: #1f1f23;\n"
"}\n"
"\n"
"QWidget{\n"
"	font-family: \"Inter\", \"Verdana\", \"sans-serif\";\n"
"	font-size: 10pt;\n"
"}\n"
"\n"
"QLabel{\n"
"	color: #F0F0F0;\n"
"	font-weight: bold;\n"
"}\n"
"\n"
"QCheckBox{\n"
"	color: #F0F0F0;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"	color: black;\n"
"}\n"
"\n"
"QTextBrowser{\n"
"	background-color: #1f1f23;\n"
"	color: #f1c40f;\n"
"}\n"
"\n"
"QPushButton{\n"
"	color: black;\n"
"}")
        self.verticalLayout = QVBoxLayout(registro)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(11)
        self.le_nombre = QLineEdit(registro)
        self.le_nombre.setObjectName(u"le_nombre")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.le_nombre)

        self.le_id = QLineEdit(registro)
        self.le_id.setObjectName(u"le_id")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.le_id)

        self.cb_grupo = QComboBox(registro)
        self.cb_grupo.setObjectName(u"cb_grupo")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.cb_grupo)

        self.le_etiquetas = QLineEdit(registro)
        self.le_etiquetas.setObjectName(u"le_etiquetas")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.le_etiquetas)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(14)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.chkb_temperatura = QCheckBox(registro)
        self.chkb_temperatura.setObjectName(u"chkb_temperatura")

        self.horizontalLayout.addWidget(self.chkb_temperatura)

        self.chkb_humedad = QCheckBox(registro)
        self.chkb_humedad.setObjectName(u"chkb_humedad")

        self.horizontalLayout.addWidget(self.chkb_humedad)


        self.formLayout.setLayout(4, QFormLayout.ItemRole.FieldRole, self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(14)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.icon_nombre = QLabel(registro)
        self.icon_nombre.setObjectName(u"icon_nombre")

        self.horizontalLayout_3.addWidget(self.icon_nombre)

        self.lbl_nombre = QLabel(registro)
        self.lbl_nombre.setObjectName(u"lbl_nombre")

        self.horizontalLayout_3.addWidget(self.lbl_nombre)


        self.formLayout.setLayout(0, QFormLayout.ItemRole.LabelRole, self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(14)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.icon_id = QLabel(registro)
        self.icon_id.setObjectName(u"icon_id")

        self.horizontalLayout_4.addWidget(self.icon_id)

        self.lbl_id = QLabel(registro)
        self.lbl_id.setObjectName(u"lbl_id")

        self.horizontalLayout_4.addWidget(self.lbl_id)


        self.formLayout.setLayout(1, QFormLayout.ItemRole.LabelRole, self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(14)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.icon_grupo = QLabel(registro)
        self.icon_grupo.setObjectName(u"icon_grupo")

        self.horizontalLayout_5.addWidget(self.icon_grupo)

        self.lbl_grupo = QLabel(registro)
        self.lbl_grupo.setObjectName(u"lbl_grupo")

        self.horizontalLayout_5.addWidget(self.lbl_grupo)


        self.formLayout.setLayout(2, QFormLayout.ItemRole.LabelRole, self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(14)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.icon_tags = QLabel(registro)
        self.icon_tags.setObjectName(u"icon_tags")

        self.horizontalLayout_6.addWidget(self.icon_tags)

        self.lbl_etiquetas = QLabel(registro)
        self.lbl_etiquetas.setObjectName(u"lbl_etiquetas")

        self.horizontalLayout_6.addWidget(self.lbl_etiquetas)


        self.formLayout.setLayout(3, QFormLayout.ItemRole.LabelRole, self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(14)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.icon_sensores = QLabel(registro)
        self.icon_sensores.setObjectName(u"icon_sensores")

        self.horizontalLayout_7.addWidget(self.icon_sensores)

        self.lbl_sensores = QLabel(registro)
        self.lbl_sensores.setObjectName(u"lbl_sensores")

        self.horizontalLayout_7.addWidget(self.lbl_sensores)


        self.formLayout.setLayout(4, QFormLayout.ItemRole.LabelRole, self.horizontalLayout_7)


        self.verticalLayout.addLayout(self.formLayout)

        self.tb_errores = QTextBrowser(registro)
        self.tb_errores.setObjectName(u"tb_errores")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_errores.sizePolicy().hasHeightForWidth())
        self.tb_errores.setSizePolicy(sizePolicy)
        self.tb_errores.setFrameShape(QFrame.NoFrame)

        self.verticalLayout.addWidget(self.tb_errores)

        self.btn_registrar = QPushButton(registro)
        self.btn_registrar.setObjectName(u"btn_registrar")

        self.verticalLayout.addWidget(self.btn_registrar)


        self.retranslateUi(registro)

        QMetaObject.connectSlotsByName(registro)
    # setupUi

    def retranslateUi(self, registro):
        registro.setWindowTitle(QCoreApplication.translate("registro", u"Registro de dispositivo", None))
        self.chkb_temperatura.setText(QCoreApplication.translate("registro", u"Temperatura", None))
        self.chkb_humedad.setText(QCoreApplication.translate("registro", u"Humedad", None))
        self.icon_nombre.setText("")
        self.lbl_nombre.setText(QCoreApplication.translate("registro", u"Nombre", None))
        self.icon_id.setText("")
        self.lbl_id.setText(QCoreApplication.translate("registro", u"ID", None))
        self.icon_grupo.setText("")
        self.lbl_grupo.setText(QCoreApplication.translate("registro", u"Grupo", None))
        self.icon_tags.setText("")
        self.lbl_etiquetas.setText(QCoreApplication.translate("registro", u"Etiquetas", None))
        self.icon_sensores.setText("")
        self.lbl_sensores.setText(QCoreApplication.translate("registro", u"Sensores", None))
        self.tb_errores.setHtml(QCoreApplication.translate("registro", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Inter','Verdana','sans-serif'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.btn_registrar.setText(QCoreApplication.translate("registro", u"Registrar", None))
    # retranslateUi

