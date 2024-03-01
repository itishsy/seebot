# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'flow_debug.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QTabWidget,
    QTableView, QWidget)

class Ui_frm_flow_debug(object):
    def setupUi(self, frm_flow_debug):
        if not frm_flow_debug.objectName():
            frm_flow_debug.setObjectName(u"frm_flow_debug")
        frm_flow_debug.resize(555, 847)
        self.tab_flow = QTabWidget(frm_flow_debug)
        self.tab_flow.setObjectName(u"tab_flow")
        self.tab_flow.setGeometry(QRect(0, 0, 551, 841))
        self.tab_flow_step = QWidget()
        self.tab_flow_step.setObjectName(u"tab_flow_step")
        self.tbl_step = QTableView(self.tab_flow_step)
        self.tbl_step.setObjectName(u"tbl_step")
        self.tbl_step.setGeometry(QRect(0, 0, 541, 811))
        self.tab_flow.addTab(self.tab_flow_step, "")
        self.tab_flow_vars = QWidget()
        self.tab_flow_vars.setObjectName(u"tab_flow_vars")
        self.tbl_vars = QTableView(self.tab_flow_vars)
        self.tbl_vars.setObjectName(u"tbl_vars")
        self.tbl_vars.setGeometry(QRect(0, 0, 541, 811))
        self.tab_flow.addTab(self.tab_flow_vars, "")

        self.retranslateUi(frm_flow_debug)

        self.tab_flow.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(frm_flow_debug)
    # setupUi

    def retranslateUi(self, frm_flow_debug):
        frm_flow_debug.setWindowTitle(QCoreApplication.translate("frm_flow_debug", u"seebot", None))
        self.tab_flow.setTabText(self.tab_flow.indexOf(self.tab_flow_step), QCoreApplication.translate("frm_flow_debug", u"\u6d41\u7a0b\u6b65\u9aa4", None))
        self.tab_flow.setTabText(self.tab_flow.indexOf(self.tab_flow_vars), QCoreApplication.translate("frm_flow_debug", u"\u6d41\u7a0b\u53d8\u91cf", None))
    # retranslateUi

