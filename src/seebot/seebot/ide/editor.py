# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'editor.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QGroupBox, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QTabWidget, QWidget)

class Ui_frm_step_edit(object):
    def setupUi(self, frm_step_edit):
        if not frm_step_edit.objectName():
            frm_step_edit.setObjectName(u"frm_step_edit")
        frm_step_edit.setWindowModality(Qt.ApplicationModal)
        frm_step_edit.resize(416, 497)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frm_step_edit.sizePolicy().hasHeightForWidth())
        frm_step_edit.setSizePolicy(sizePolicy)
        frm_step_edit.setAutoFillBackground(True)
        self.tab_step = QTabWidget(frm_step_edit)
        self.tab_step.setObjectName(u"tab_step")
        self.tab_step.setGeometry(QRect(10, 70, 401, 381))
        self.tab_step.setBaseSize(QSize(0, 0))
        self.tab_step.setFocusPolicy(Qt.ClickFocus)
        self.tab_step.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.tab_step.setAcceptDrops(False)
        self.tab_step.setLayoutDirection(Qt.LeftToRight)
        self.tab_step.setTabPosition(QTabWidget.North)
        self.tab_step.setTabShape(QTabWidget.Triangular)
        self.tab_step.setElideMode(Qt.ElideNone)
        self.tab_step.setDocumentMode(False)
        self.tab_target = QWidget()
        self.tab_target.setObjectName(u"tab_target")
        self.grb_target = QGroupBox(self.tab_target)
        self.grb_target.setObjectName(u"grb_target")
        self.grb_target.setGeometry(QRect(10, 10, 381, 171))
        self.formLayoutWidget_3 = QWidget(self.grb_target)
        self.formLayoutWidget_3.setObjectName(u"formLayoutWidget_3")
        self.formLayoutWidget_3.setGeometry(QRect(10, 20, 361, 141))
        self.fol_target = QFormLayout(self.formLayoutWidget_3)
        self.fol_target.setObjectName(u"fol_target")
        self.fol_target.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.fol_target.setContentsMargins(0, 0, 0, 0)
        self.grb_action = QGroupBox(self.tab_target)
        self.grb_action.setObjectName(u"grb_action")
        self.grb_action.setGeometry(QRect(10, 180, 381, 181))
        self.formLayoutWidget_4 = QWidget(self.grb_action)
        self.formLayoutWidget_4.setObjectName(u"formLayoutWidget_4")
        self.formLayoutWidget_4.setGeometry(QRect(10, 20, 361, 151))
        self.fol_action = QFormLayout(self.formLayoutWidget_4)
        self.fol_action.setObjectName(u"fol_action")
        self.fol_action.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.fol_action.setHorizontalSpacing(8)
        self.fol_action.setVerticalSpacing(8)
        self.fol_action.setContentsMargins(0, 0, 0, 0)
        self.tab_step.addTab(self.tab_target, "")
        self.tab_trans = QWidget()
        self.tab_trans.setObjectName(u"tab_trans")
        self.groupBox = QGroupBox(self.tab_trans)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 381, 181))
        self.groupBox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.formLayoutWidget = QWidget(self.groupBox)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 20, 361, 158))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.Label = QLabel(self.formLayoutWidget)
        self.Label.setObjectName(u"Label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.Label)

        self.fid_skipTo = QComboBox(self.formLayoutWidget)
        self.fid_skipTo.addItem("")
        self.fid_skipTo.setObjectName(u"fid_skipTo")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.fid_skipTo)

        self.Label_2 = QLabel(self.formLayoutWidget)
        self.Label_2.setObjectName(u"Label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.Label_2)

        self.fid_timeout = QLineEdit(self.formLayoutWidget)
        self.fid_timeout.setObjectName(u"fid_timeout")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.fid_timeout)

        self.Label_3 = QLabel(self.formLayoutWidget)
        self.Label_3.setObjectName(u"Label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.Label_3)

        self.fid_skipCondition = QLineEdit(self.formLayoutWidget)
        self.fid_skipCondition.setObjectName(u"fid_skipCondition")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.fid_skipCondition)

        self.Label_4 = QLabel(self.formLayoutWidget)
        self.Label_4.setObjectName(u"Label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.Label_4)

        self.fid_waitBefore = QLineEdit(self.formLayoutWidget)
        self.fid_waitBefore.setObjectName(u"fid_waitBefore")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.fid_waitBefore)

        self.Label_5 = QLabel(self.formLayoutWidget)
        self.Label_5.setObjectName(u"Label_5")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.Label_5)

        self.fid_waitAfter = QLineEdit(self.formLayoutWidget)
        self.fid_waitAfter.setObjectName(u"fid_waitAfter")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.fid_waitAfter)

        self.groupBox_2 = QGroupBox(self.tab_trans)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 200, 381, 161))
        self.formLayoutWidget_2 = QWidget(self.groupBox_2)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(10, 20, 361, 121))
        self.formLayout_2 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setHorizontalSpacing(6)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.Label_6 = QLabel(self.formLayoutWidget_2)
        self.Label_6.setObjectName(u"Label_6")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.Label_6)

        self.fid_failedStrategy = QComboBox(self.formLayoutWidget_2)
        self.fid_failedStrategy.addItem("")
        self.fid_failedStrategy.addItem("")
        self.fid_failedStrategy.addItem("")
        self.fid_failedStrategy.setObjectName(u"fid_failedStrategy")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.fid_failedStrategy)

        self.Label_7 = QLabel(self.formLayoutWidget_2)
        self.Label_7.setObjectName(u"Label_7")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.Label_7)

        self.fid_failedSkipTo = QComboBox(self.formLayoutWidget_2)
        self.fid_failedSkipTo.addItem("")
        self.fid_failedSkipTo.setObjectName(u"fid_failedSkipTo")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.fid_failedSkipTo)

        self.Label_8 = QLabel(self.formLayoutWidget_2)
        self.Label_8.setObjectName(u"Label_8")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.Label_8)

        self.fid_failedRetry = QLineEdit(self.formLayoutWidget_2)
        self.fid_failedRetry.setObjectName(u"fid_failedRetry")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.fid_failedRetry)

        self.tab_step.addTab(self.tab_trans, "")
        self.btn_run = QPushButton(frm_step_edit)
        self.btn_run.setObjectName(u"btn_run")
        self.btn_run.setGeometry(QRect(210, 460, 111, 31))
        self.btn_save = QPushButton(frm_step_edit)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setGeometry(QRect(330, 460, 75, 31))
        self.groupBox_3 = QGroupBox(frm_step_edit)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 10, 401, 51))
        self.fid_stepName = QLineEdit(self.groupBox_3)
        self.fid_stepName.setObjectName(u"fid_stepName")
        self.fid_stepName.setGeometry(QRect(10, 10, 381, 31))
        self.fid_status = QCheckBox(frm_step_edit)
        self.fid_status.setObjectName(u"fid_status")
        self.fid_status.setGeometry(QRect(10, 470, 61, 19))
        font = QFont()
        font.setPointSize(10)
        self.fid_status.setFont(font)

        self.retranslateUi(frm_step_edit)

        self.tab_step.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(frm_step_edit)
    # setupUi

    def retranslateUi(self, frm_step_edit):
        frm_step_edit.setWindowTitle(QCoreApplication.translate("frm_step_edit", u"seebot", None))
        self.grb_target.setTitle(QCoreApplication.translate("frm_step_edit", u"\u76ee\u6807\u5bf9\u8c61", None))
        self.grb_action.setTitle(QCoreApplication.translate("frm_step_edit", u"\u884c\u4e3a\u53c2\u6570", None))
        self.tab_step.setTabText(self.tab_step.indexOf(self.tab_target), QCoreApplication.translate("frm_step_edit", u"\u64cd\u4f5c\u5bf9\u8c61", None))
        self.groupBox.setTitle(QCoreApplication.translate("frm_step_edit", u"\u6267\u884c\u53c2\u6570", None))
        self.Label.setText(QCoreApplication.translate("frm_step_edit", u"\u6267\u884c\u6210\u529f\u8df3\u8f6c", None))
        self.fid_skipTo.setItemText(0, "")

        self.Label_2.setText(QCoreApplication.translate("frm_step_edit", u"\u8d85\u65f6\u65f6\u95f4(s)", None))
        self.fid_timeout.setPlaceholderText(QCoreApplication.translate("frm_step_edit", u"10\u79d2", None))
        self.Label_3.setText(QCoreApplication.translate("frm_step_edit", u"\u8df3\u8fc7\u6b64\u6b65\u9aa4\u6761\u4ef6", None))
        self.fid_skipCondition.setPlaceholderText(QCoreApplication.translate("frm_step_edit", u"\u65e0", None))
        self.Label_4.setText(QCoreApplication.translate("frm_step_edit", u"\u6267\u884c\u524d\u7b49\u5f85(s)", None))
        self.fid_waitBefore.setPlaceholderText(QCoreApplication.translate("frm_step_edit", u"\u4e0d\u7b49\u5f85", None))
        self.Label_5.setText(QCoreApplication.translate("frm_step_edit", u"\u6267\u884c\u540e\u7b49\u5f85(s)", None))
        self.fid_waitAfter.setPlaceholderText(QCoreApplication.translate("frm_step_edit", u"\u4e0d\u7b49\u5f85", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("frm_step_edit", u"\u5f02\u5e38\u5904\u7406", None))
        self.Label_6.setText(QCoreApplication.translate("frm_step_edit", u"\u51fa\u73b0\u5f02\u5e38\u65f6", None))
        self.fid_failedStrategy.setItemText(0, QCoreApplication.translate("frm_step_edit", u"\u4e2d\u6b62\u6d41\u7a0b", None))
        self.fid_failedStrategy.setItemText(1, QCoreApplication.translate("frm_step_edit", u"\u5ffd\u7565", None))
        self.fid_failedStrategy.setItemText(2, QCoreApplication.translate("frm_step_edit", u"\u8df3\u8f6c", None))

        self.Label_7.setText(QCoreApplication.translate("frm_step_edit", u"\u5f02\u5e38\u8df3\u8f6c\u81f3", None))
        self.fid_failedSkipTo.setItemText(0, "")

        self.Label_8.setText(QCoreApplication.translate("frm_step_edit", u"\u5931\u8d25\u91cd\u8bd5\u6b21\u6570(s)", None))
        self.fid_failedRetry.setPlaceholderText(QCoreApplication.translate("frm_step_edit", u"\u4e0d\u91cd\u8bd5", None))
        self.tab_step.setTabText(self.tab_step.indexOf(self.tab_trans), QCoreApplication.translate("frm_step_edit", u"\u6d41\u8f6c\u63a7\u5236", None))
        self.btn_run.setText(QCoreApplication.translate("frm_step_edit", u"\u8fd0\u884c\u6b64\u6b65\u9aa4", None))
        self.btn_save.setText(QCoreApplication.translate("frm_step_edit", u"\u78ba\u5b9a", None))
        self.groupBox_3.setTitle("")
        self.fid_stepName.setPlaceholderText(QCoreApplication.translate("frm_step_edit", u"\u6b65\u9aa4\u540d\u79f0", None))
        self.fid_status.setText(QCoreApplication.translate("frm_step_edit", u"\u7981\u7528", None))
    # retranslateUi

