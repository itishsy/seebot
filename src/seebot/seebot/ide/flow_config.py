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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGroupBox,
    QHeaderView, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QTabWidget, QTableView,
    QTableWidget, QTableWidgetItem, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_frm_flow_config(object):
    def setupUi(self, frm_flow_config):
        if not frm_flow_config.objectName():
            frm_flow_config.setObjectName(u"frm_flow_config")
        frm_flow_config.resize(1140, 845)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frm_flow_config.sizePolicy().hasHeightForWidth())
        frm_flow_config.setSizePolicy(sizePolicy)
        self.tab_flow = QTabWidget(frm_flow_config)
        self.tab_flow.setObjectName(u"tab_flow")
        self.tab_flow.setGeometry(QRect(330, 70, 531, 711))
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
        self.tbl_steps.setGeometry(QRect(0, 0, 521, 681))
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
        self.tbl_args.setGeometry(QRect(0, 0, 521, 681))
        self.tbl_args.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl_args.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_args.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tab_flow.addTab(self.tab_flow_vars, "")
        self.btn_run = QPushButton(frm_flow_config)
        self.btn_run.setObjectName(u"btn_run")
        self.btn_run.setGeometry(QRect(10, 800, 75, 31))
        self.btn_save = QPushButton(frm_flow_config)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setGeometry(QRect(1054, 800, 71, 31))
        self.btn_sync = QPushButton(frm_flow_config)
        self.btn_sync.setObjectName(u"btn_sync")
        self.btn_sync.setGeometry(QRect(930, 800, 111, 31))
        font1 = QFont()
        font1.setItalic(False)
        font1.setUnderline(True)
        self.btn_sync.setFont(font1)
        self.btn_sync.setAutoFillBackground(False)
        self.gbx_action = QGroupBox(frm_flow_config)
        self.gbx_action.setObjectName(u"gbx_action")
        self.gbx_action.setGeometry(QRect(10, 70, 311, 711))
        self.trw_actions = QTreeWidget(self.gbx_action)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.trw_actions.setHeaderItem(__qtreewidgetitem)
        self.trw_actions.setObjectName(u"trw_actions")
        self.trw_actions.setGeometry(QRect(10, 20, 291, 681))
        self.trw_actions.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.trw_actions.setDragEnabled(True)
        self.trw_actions.setDragDropOverwriteMode(True)
        self.trw_actions.setDragDropMode(QAbstractItemView.DragOnly)
        self.trw_actions.setDefaultDropAction(Qt.MoveAction)
        self.groupBox = QGroupBox(frm_flow_config)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 1121, 51))
        self.lab_app = QLabel(self.groupBox)
        self.lab_app.setObjectName(u"lab_app")
        self.lab_app.setGeometry(QRect(10, 20, 53, 15))
        self.cmb_app = QComboBox(self.groupBox)
        self.cmb_app.addItem("")
        self.cmb_app.addItem("")
        self.cmb_app.setObjectName(u"cmb_app")
        self.cmb_app.setGeometry(QRect(50, 10, 231, 31))
        self.lab_flow = QLabel(self.groupBox)
        self.lab_flow.setObjectName(u"lab_flow")
        self.lab_flow.setGeometry(QRect(320, 20, 53, 15))
        self.cmb_flow = QComboBox(self.groupBox)
        self.cmb_flow.addItem("")
        self.cmb_flow.addItem("")
        self.cmb_flow.setObjectName(u"cmb_flow")
        self.cmb_flow.setGeometry(QRect(360, 10, 251, 31))
        self.lab_account = QLabel(self.groupBox)
        self.lab_account.setObjectName(u"lab_account")
        self.lab_account.setGeometry(QRect(650, 20, 53, 15))
        self.cmb_task = QComboBox(self.groupBox)
        self.cmb_task.addItem("")
        self.cmb_task.addItem("")
        self.cmb_task.setObjectName(u"cmb_task")
        self.cmb_task.setGeometry(QRect(690, 10, 311, 31))
        self.btn_reload = QPushButton(self.groupBox)
        self.btn_reload.setObjectName(u"btn_reload")
        self.btn_reload.setGeometry(QRect(1030, 10, 75, 31))
        self.btn_suspend = QPushButton(frm_flow_config)
        self.btn_suspend.setObjectName(u"btn_suspend")
        self.btn_suspend.setGeometry(QRect(90, 800, 81, 31))
        self.btn_continue = QPushButton(frm_flow_config)
        self.btn_continue.setObjectName(u"btn_continue")
        self.btn_continue.setGeometry(QRect(180, 800, 81, 31))
        self.btn_back = QPushButton(frm_flow_config)
        self.btn_back.setObjectName(u"btn_back")
        self.btn_back.setGeometry(QRect(270, 800, 81, 31))
        self.btn_next = QPushButton(frm_flow_config)
        self.btn_next.setObjectName(u"btn_next")
        self.btn_next.setGeometry(QRect(360, 800, 81, 31))
        self.btn_stop = QPushButton(frm_flow_config)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setGeometry(QRect(450, 800, 71, 31))
        self.gbx_vars = QGroupBox(frm_flow_config)
        self.gbx_vars.setObjectName(u"gbx_vars")
        self.gbx_vars.setGeometry(QRect(860, 70, 271, 381))
        self.tbl_vars = QTableView(self.gbx_vars)
        self.tbl_vars.setObjectName(u"tbl_vars")
        self.tbl_vars.setGeometry(QRect(10, 20, 251, 351))
        self.gbx_logs = QGroupBox(frm_flow_config)
        self.gbx_logs.setObjectName(u"gbx_logs")
        self.gbx_logs.setGeometry(QRect(860, 460, 271, 321))
        self.lis_logs = QListWidget(self.gbx_logs)
        self.lis_logs.setObjectName(u"lis_logs")
        self.lis_logs.setEnabled(True)
        self.lis_logs.setGeometry(QRect(10, 20, 251, 291))

        self.retranslateUi(frm_flow_config)

        self.tab_flow.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(frm_flow_config)
    # setupUi

    def retranslateUi(self, frm_flow_config):
        frm_flow_config.setWindowTitle(QCoreApplication.translate("frm_flow_config", u"seebot-ide", None))
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
        self.tab_flow.setTabText(self.tab_flow.indexOf(self.tab_flow_vars), QCoreApplication.translate("frm_flow_config", u"\u542f\u52a8\u53c2\u6570", None))
        self.btn_run.setText(QCoreApplication.translate("frm_flow_config", u"\u8fd0\u884c", None))
        self.btn_save.setText(QCoreApplication.translate("frm_flow_config", u"\u4fdd\u5b58", None))
        self.btn_sync.setText(QCoreApplication.translate("frm_flow_config", u"\u540c\u6b65\u5230\u670d\u52a1\u5668", None))
        self.gbx_action.setTitle(QCoreApplication.translate("frm_flow_config", u"\u64cd\u4f5c\u6307\u4ee4", None))
        self.groupBox.setTitle("")
        self.lab_app.setText(QCoreApplication.translate("frm_flow_config", u"\u5e94\u7528\uff1a", None))
        self.cmb_app.setItemText(0, QCoreApplication.translate("frm_flow_config", u"\u5e7f\u5dde-\u793e\u4fdd", None))
        self.cmb_app.setItemText(1, QCoreApplication.translate("frm_flow_config", u"\u5e7f\u5dde-\u516c\u79ef\u91d1", None))

        self.lab_flow.setText(QCoreApplication.translate("frm_flow_config", u"\u6d41\u7a0b\uff1a", None))
        self.cmb_flow.setItemText(0, QCoreApplication.translate("frm_flow_config", u"\u5e7f\u5dde\u793e\u4fdd\u5355\u5de5\u4f24\u589e\u5458", None))
        self.cmb_flow.setItemText(1, QCoreApplication.translate("frm_flow_config", u"\u5e7f\u5dde\u793e\u4fdd\u51cf\u5458", None))

        self.cmb_flow.setCurrentText(QCoreApplication.translate("frm_flow_config", u"\u5e7f\u5dde\u793e\u4fdd\u5355\u5de5\u4f24\u589e\u5458", None))
        self.lab_account.setText(QCoreApplication.translate("frm_flow_config", u"\u8d26\u6237\uff1a", None))
        self.cmb_task.setItemText(0, QCoreApplication.translate("frm_flow_config", u"\u5e7f\u5dde\u5357\u4ed5\u90a6\u4eba\u529b\u8d44\u6e90\u6709\u9650\u516c\u53f8-123929", None))
        self.cmb_task.setItemText(1, QCoreApplication.translate("frm_flow_config", u"\u5e7f\u5dde\u4ed5\u90a6\u4eba\u529b\u8d44\u6e90\u6709\u9650\u516c\u53f8-123923", None))

        self.cmb_task.setCurrentText(QCoreApplication.translate("frm_flow_config", u"\u5e7f\u5dde\u5357\u4ed5\u90a6\u4eba\u529b\u8d44\u6e90\u6709\u9650\u516c\u53f8-123929", None))
        self.btn_reload.setText(QCoreApplication.translate("frm_flow_config", u"\u5237\u65b0", None))
        self.btn_suspend.setText(QCoreApplication.translate("frm_flow_config", u"\u6682\u505c", None))
        self.btn_continue.setText(QCoreApplication.translate("frm_flow_config", u"\u7ee7\u7eed", None))
        self.btn_back.setText(QCoreApplication.translate("frm_flow_config", u"\u4e0a\u4e00\u6b65", None))
        self.btn_next.setText(QCoreApplication.translate("frm_flow_config", u"\u4e0b\u4e00\u6b65", None))
        self.btn_stop.setText(QCoreApplication.translate("frm_flow_config", u"\u505c\u6b62", None))
        self.gbx_vars.setTitle(QCoreApplication.translate("frm_flow_config", u"\u8fd0\u884c\u65f6\u53d8\u91cf", None))
        self.gbx_logs.setTitle(QCoreApplication.translate("frm_flow_config", u"\u6267\u884c\u65e5\u5fd7", None))
    # retranslateUi

