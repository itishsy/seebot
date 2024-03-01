# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'flow_config.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGroupBox, QHeaderView,
    QPushButton, QSizePolicy, QTabWidget, QTableWidget,
    QTableWidgetItem, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_frm_flow_config(object):
    def setupUi(self, frm_flow_config):
        if not frm_flow_config.objectName():
            frm_flow_config.setObjectName(u"frm_flow_config")
        frm_flow_config.resize(863, 840)
        self.tab_flow = QTabWidget(frm_flow_config)
        self.tab_flow.setObjectName(u"tab_flow")
        self.tab_flow.setGeometry(QRect(330, 10, 531, 771))
        self.tab_flow_step = QWidget()
        self.tab_flow_step.setObjectName(u"tab_flow_step")
        self.tbl_steps = QTableWidget(self.tab_flow_step)
        if (self.tbl_steps.columnCount() < 2):
            self.tbl_steps.setColumnCount(2)
        font = QFont()
        font.setBold(True)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font);
        self.tbl_steps.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font);
        self.tbl_steps.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tbl_steps.setObjectName(u"tbl_steps")
        self.tbl_steps.setGeometry(QRect(0, 0, 521, 741))
        self.tbl_steps.setMouseTracking(True)
        self.tbl_steps.setAcceptDrops(True)
        self.tbl_steps.setMidLineWidth(1)
        self.tbl_steps.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.tbl_steps.setDragEnabled(True)
        self.tbl_steps.setDragDropOverwriteMode(True)
        self.tbl_steps.setDragDropMode(QAbstractItemView.InternalMove)
        self.tbl_steps.setDefaultDropAction(Qt.MoveAction)
        self.tbl_steps.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_steps.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_steps.setTextElideMode(Qt.ElideLeft)
        self.tbl_steps.horizontalHeader().setProperty("showSortIndicator", False)
        self.tab_flow.addTab(self.tab_flow_step, "")
        self.tab_flow_vars = QWidget()
        self.tab_flow_vars.setObjectName(u"tab_flow_vars")
        self.tbl_args = QTableWidget(self.tab_flow_vars)
        if (self.tbl_args.columnCount() < 3):
            self.tbl_args.setColumnCount(3)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tbl_args.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tbl_args.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tbl_args.setHorizontalHeaderItem(2, __qtablewidgetitem4)
        self.tbl_args.setObjectName(u"tbl_args")
        self.tbl_args.setGeometry(QRect(0, 0, 521, 741))
        self.tbl_args.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl_args.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_args.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tab_flow.addTab(self.tab_flow_vars, "")
        self.btn_run = QPushButton(frm_flow_config)
        self.btn_run.setObjectName(u"btn_run")
        self.btn_run.setGeometry(QRect(10, 800, 75, 31))
        self.btn_save = QPushButton(frm_flow_config)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setGeometry(QRect(780, 800, 75, 31))
        self.btn_debug = QPushButton(frm_flow_config)
        self.btn_debug.setObjectName(u"btn_debug")
        self.btn_debug.setGeometry(QRect(90, 800, 75, 31))
        self.gbx_action = QGroupBox(frm_flow_config)
        self.gbx_action.setObjectName(u"gbx_action")
        self.gbx_action.setGeometry(QRect(10, 10, 311, 771))
        self.trw_actions = QTreeWidget(self.gbx_action)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.trw_actions.setHeaderItem(__qtreewidgetitem)
        self.trw_actions.setObjectName(u"trw_actions")
        self.trw_actions.setGeometry(QRect(10, 30, 291, 731))
        self.trw_actions.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.trw_actions.setDragEnabled(True)
        self.trw_actions.setDragDropOverwriteMode(True)
        self.trw_actions.setDragDropMode(QAbstractItemView.DragOnly)
        self.trw_actions.setDefaultDropAction(Qt.MoveAction)

        self.retranslateUi(frm_flow_config)

        self.tab_flow.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(frm_flow_config)
    # setupUi

    def retranslateUi(self, frm_flow_config):
        frm_flow_config.setWindowTitle(QCoreApplication.translate("frm_flow_config", u"seebot", None))
        ___qtablewidgetitem = self.tbl_steps.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("frm_flow_config", u"\u6b65\u9aa4\u540d\u79f0", None));
        ___qtablewidgetitem1 = self.tbl_steps.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("frm_flow_config", u"\u64cd\u4f5c\u7c7b\u578b", None));
        self.tab_flow.setTabText(self.tab_flow.indexOf(self.tab_flow_step), QCoreApplication.translate("frm_flow_config", u"\u6d41\u7a0b\u6b65\u9aa4", None))
        ___qtablewidgetitem2 = self.tbl_args.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("frm_flow_config", u"\u7c7b\u578b", None));
        ___qtablewidgetitem3 = self.tbl_args.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("frm_flow_config", u"\u540d\u79f0\uff08Key\uff09", None));
        ___qtablewidgetitem4 = self.tbl_args.horizontalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("frm_flow_config", u"\u503c\uff08Value\uff09", None));
        self.tab_flow.setTabText(self.tab_flow.indexOf(self.tab_flow_vars), QCoreApplication.translate("frm_flow_config", u"\u6d41\u7a0b\u53d8\u91cf", None))
        self.btn_run.setText(QCoreApplication.translate("frm_flow_config", u"\u8fd0\u884c", None))
        self.btn_save.setText(QCoreApplication.translate("frm_flow_config", u"\u4fdd\u5b58", None))
        self.btn_debug.setText(QCoreApplication.translate("frm_flow_config", u"\u8c03\u8bd5", None))
        self.gbx_action.setTitle(QCoreApplication.translate("frm_flow_config", u"\u64cd\u4f5c\u6307\u4ee4", None))
    # retranslateUi

