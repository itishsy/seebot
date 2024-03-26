# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_frm_index(object):
    def setupUi(self, frm_index):
        if not frm_index.objectName():
            frm_index.setObjectName(u"frm_index")
        frm_index.resize(370, 207)
        self.inp_password = QLineEdit(frm_index)
        self.inp_password.setObjectName(u"inp_password")
        self.inp_password.setGeometry(QRect(90, 100, 251, 31))
        self.inp_password.setToolTipDuration(2)
        self.inp_password.setEchoMode(QLineEdit.Password)
        self.lab_username = QLabel(frm_index)
        self.lab_username.setObjectName(u"lab_username")
        self.lab_username.setGeometry(QRect(30, 70, 53, 15))
        self.inp_username = QLineEdit(frm_index)
        self.inp_username.setObjectName(u"inp_username")
        self.inp_username.setGeometry(QRect(90, 60, 251, 31))
        self.inp_username.setToolTipDuration(1)
        self.lab_password = QLabel(frm_index)
        self.lab_password.setObjectName(u"lab_password")
        self.lab_password.setGeometry(QRect(30, 110, 53, 15))
        self.cmb_server = QComboBox(frm_index)
        self.cmb_server.addItem("")
        self.cmb_server.addItem("")
        self.cmb_server.addItem("")
        self.cmb_server.addItem("")
        self.cmb_server.setObjectName(u"cmb_server")
        self.cmb_server.setGeometry(QRect(90, 20, 251, 31))
        self.lab_server = QLabel(frm_index)
        self.lab_server.setObjectName(u"lab_server")
        self.lab_server.setGeometry(QRect(30, 30, 53, 15))
        self.btn_login = QPushButton(frm_index)
        self.btn_login.setObjectName(u"btn_login")
        self.btn_login.setGeometry(QRect(270, 160, 71, 31))
        self.btn_login.setToolTipDuration(3)
        self.ckb_session = QCheckBox(frm_index)
        self.ckb_session.setObjectName(u"ckb_session")
        self.ckb_session.setGeometry(QRect(30, 160, 80, 19))
        QWidget.setTabOrder(self.cmb_server, self.inp_username)
        QWidget.setTabOrder(self.inp_username, self.inp_password)
        QWidget.setTabOrder(self.inp_password, self.ckb_session)
        QWidget.setTabOrder(self.ckb_session, self.btn_login)

        self.retranslateUi(frm_index)

        QMetaObject.connectSlotsByName(frm_index)
    # setupUi

    def retranslateUi(self, frm_index):
        frm_index.setWindowTitle(QCoreApplication.translate("frm_index", u"seebot-ide", None))
        self.inp_password.setText("")
        self.inp_password.setPlaceholderText(QCoreApplication.translate("frm_index", u"\u8f93\u5165\u5bc6\u7801", None))
        self.lab_username.setText(QCoreApplication.translate("frm_index", u"\u7528\u6237\u540d\uff1a", None))
        self.inp_username.setText("")
        self.inp_username.setPlaceholderText(QCoreApplication.translate("frm_index", u"\u8f93\u5165\u7528\u6237\u540d", None))
        self.lab_password.setText(QCoreApplication.translate("frm_index", u"\u5bc6\u7801\uff1a", None))
        self.cmb_server.setItemText(0, QCoreApplication.translate("frm_index", u"https://rpa.seebon.com", None))
        self.cmb_server.setItemText(1, QCoreApplication.translate("frm_index", u"http://192.168.0.99:9999", None))
        self.cmb_server.setItemText(2, QCoreApplication.translate("frm_index", u"http://192.168.0.68:9999", None))
        self.cmb_server.setItemText(3, QCoreApplication.translate("frm_index", u"http://127.0.0.1:9090", None))

        self.cmb_server.setCurrentText(QCoreApplication.translate("frm_index", u"https://rpa.seebon.com", None))
        self.lab_server.setText(QCoreApplication.translate("frm_index", u"\u670d\u52a1\u5668\uff1a", None))
        self.btn_login.setText(QCoreApplication.translate("frm_index", u"\u767b\u5f55", None))
        self.ckb_session.setText(QCoreApplication.translate("frm_index", u"\u4fdd\u6301\u4f1a\u8bdd", None))
    # retranslateUi

