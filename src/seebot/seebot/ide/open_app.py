# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'open_app.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
    QPushButton, QSizePolicy, QWidget)

class Ui_frm_open(object):
    def setupUi(self, frm_open):
        if not frm_open.objectName():
            frm_open.setObjectName(u"frm_open")
        frm_open.resize(400, 300)
        self.lab_flow = QLabel(frm_open)
        self.lab_flow.setObjectName(u"lab_flow")
        self.lab_flow.setGeometry(QRect(40, 110, 53, 15))
        self.lab_account = QLabel(frm_open)
        self.lab_account.setObjectName(u"lab_account")
        self.lab_account.setGeometry(QRect(40, 160, 53, 15))
        self.cmb_app = QComboBox(frm_open)
        self.cmb_app.addItem("")
        self.cmb_app.addItem("")
        self.cmb_app.setObjectName(u"cmb_app")
        self.cmb_app.setGeometry(QRect(100, 50, 251, 31))
        self.lab_app = QLabel(frm_open)
        self.lab_app.setObjectName(u"lab_app")
        self.lab_app.setGeometry(QRect(40, 60, 53, 15))
        self.btn_open = QPushButton(frm_open)
        self.btn_open.setObjectName(u"btn_open")
        self.btn_open.setGeometry(QRect(280, 230, 71, 31))
        self.cmb_flow = QComboBox(frm_open)
        self.cmb_flow.addItem("")
        self.cmb_flow.addItem("")
        self.cmb_flow.setObjectName(u"cmb_flow")
        self.cmb_flow.setGeometry(QRect(100, 100, 251, 31))
        self.cmb_task = QComboBox(frm_open)
        self.cmb_task.addItem("")
        self.cmb_task.addItem("")
        self.cmb_task.setObjectName(u"cmb_task")
        self.cmb_task.setGeometry(QRect(100, 150, 251, 31))
        self.ckb_remember = QCheckBox(frm_open)
        self.ckb_remember.setObjectName(u"ckb_remember")
        self.ckb_remember.setGeometry(QRect(40, 230, 80, 19))

        self.retranslateUi(frm_open)

        QMetaObject.connectSlotsByName(frm_open)
    # setupUi

    def retranslateUi(self, frm_open):
        frm_open.setWindowTitle(QCoreApplication.translate("frm_open", u"seebot \u6253\u5f00\u6d41\u7a0b", None))
        self.lab_flow.setText(QCoreApplication.translate("frm_open", u"\u6d41\u7a0b\uff1a", None))
        self.lab_account.setText(QCoreApplication.translate("frm_open", u"\u4efb\u52a1\uff1a", None))
        self.cmb_app.setItemText(0, QCoreApplication.translate("frm_open", u"\u5e7f\u5dde-\u793e\u4fdd", None))
        self.cmb_app.setItemText(1, QCoreApplication.translate("frm_open", u"\u5e7f\u5dde-\u516c\u79ef\u91d1", None))

        self.lab_app.setText(QCoreApplication.translate("frm_open", u"\u5e94\u7528\uff1a", None))
        self.btn_open.setText(QCoreApplication.translate("frm_open", u"\u6253\u5f00", None))
        self.cmb_flow.setItemText(0, QCoreApplication.translate("frm_open", u"\u5e7f\u5dde\u793e\u4fdd\u5355\u5de5\u4f24\u589e\u5458", None))
        self.cmb_flow.setItemText(1, QCoreApplication.translate("frm_open", u"\u5e7f\u5dde\u793e\u4fdd\u51cf\u5458", None))

        self.cmb_flow.setCurrentText(QCoreApplication.translate("frm_open", u"\u5e7f\u5dde\u793e\u4fdd\u5355\u5de5\u4f24\u589e\u5458", None))
        self.cmb_task.setItemText(0, QCoreApplication.translate("frm_open", u"\u5e7f\u5dde\u5357\u4ed5\u90a6\u4eba\u529b\u8d44\u6e90\u6709\u9650\u516c\u53f8-123929", None))
        self.cmb_task.setItemText(1, QCoreApplication.translate("frm_open", u"\u5e7f\u5dde\u4ed5\u90a6\u4eba\u529b\u8d44\u6e90\u6709\u9650\u516c\u53f8-123923", None))

        self.cmb_task.setCurrentText(QCoreApplication.translate("frm_open", u"\u5e7f\u5dde\u5357\u4ed5\u90a6\u4eba\u529b\u8d44\u6e90\u6709\u9650\u516c\u53f8-123929", None))
        self.ckb_remember.setText(QCoreApplication.translate("frm_open", u"\u8bb0\u4f4f\u9009\u62e9", None))
    # retranslateUi

