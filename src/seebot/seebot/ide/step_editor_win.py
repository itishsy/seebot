from PySide6.QtWidgets import QMainWindow, QWidget, QLabel,QFormLayout, QComboBox, QLineEdit
from PySide6.QtCore import Qt

from seebot.ide.api import Api
from seebot.ide.step_editor import Ui_frm_step_edit
import json


class StepEditorWin(QMainWindow, Ui_frm_step_edit):
    def __init__(self, parent=None):
        super(StepEditorWin, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())
        # self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowMinMaxButtonsHint)
        self.region = None
        self.target_fields = []
        self.target_cond_data = {}
        self.action_fields = []
        self.action_cond_data = {}
        self.btn_save.clicked.connect(self.on_save_click)
        self.btn_run.clicked.connect(self.on_run_click)

    def show(self) -> None:
        super(StepEditorWin, self).show()
        if hasattr(self,'step'):
            self.setWindowTitle('编辑 【' + self.action_name + '】')
        else:
            self.setWindowTitle('新建 【' + self.action_name + '】')
            self.step = self.init_step(self.action_code, self.number)
        self.load_step_data()
        self.load_trans_data()
        self.load_dynamic_data('target')
        self.load_dynamic_data('action')

    def init_step(self, action_code, number):
        api = Api()
        target_args = api.find_target_args(self.action_code)
        action_args = api.find_action_args(self.action_code)
        return {'id': None, 'flowCode': None, 'groupCode': None, 'stepCode': None, 'stepName': '',
                'actionCode': action_code, 'actionArgs': '', 'targetArgs': '', 'number': number,
                'level': 1, 'status': 1, 'failedRetry': None, 'failedStrategy': 0, 'failedSkipTo': '',
                'skipTo': '登录成功?', 'falseSkipTo': None, 'skipCondition': '', 'waitBefore': None,
                'waitAfter': None, 'timeout': 5, 'type': None, 'openEdit': None,
                'actionArgsVOS': action_args["data"],'targetArgsVOS': target_args["data"], 'trueSkipTo': ''}

    def load_step_data(self):
        self.let_step_name.setText(self.step['stepName'])
        if self.step['status'] != 1:
            self.ckb_status.setChecked(True)

    def load_trans_data(self):
        if self.step['timeout'] is not None:
            self.let_timeout.setText(str(self.step['timeout']))
        if self.step['skipCondition'] is not None:
            self.let_skip_condition.setText(str(self.step['skipCondition']))
        if self.step['waitBefore'] is not None:
            self.let_wait_before.setText(str(self.step['waitBefore']))
        if self.step['waitAfter'] is not None:
            self.let_wait_after.setText(str(self.step['waitAfter']))

    def load_dynamic_data(self, region):
        self.region = region
        self.target_cond_data = []
        self.action_cond_data = {}
        args_vos = self.step[region + "ArgsVOS"]
        if args_vos is not None:
            for item in args_vos:
                field_key = item['fieldKey']
                if self.is_cond_field(field_key):
                    continue

                field = self.add_dynamic_field(field_key, item['fieldType'], item['fieldName'])
                if isinstance(field, QComboBox):
                    currentText = None
                    for cb_item in item['robotDataDicts']:
                        field.addItem(cb_item['dictName'], cb_item['dictCode'])
                        if hasattr(item,'fieldValue'):
                            if item['fieldValue'] == cb_item['dictCode']:
                                currentText = cb_item['dictName']
                    if currentText is not None:
                        field.setCurrentText(currentText)
                    if item['cond'] != '':
                        field.currentTextChanged.connect(self.on_dynamic_combo_change)
                        if region == 'action':
                            self.action_cond_data = json.loads(item['cond'])
                        else:
                            self.target_cond_data = json.loads(item['cond'])
                        self.on_dynamic_combo_change(currentText)
                else:
                    if hasattr(item,'fieldValue'):
                        field.setText(item['fieldValue'])

    def on_dynamic_combo_change(self, arg1):
        combo = None
        dynamic_fields = self.action_fields if self.region == 'action' else self.target_fields
        for f in dynamic_fields:
            if not isinstance(f, QLabel) and hasattr(f,'currentText') and f.currentText() == arg1:
                combo = f
                break

        if combo is not None:
            cond_data = self.action_cond_data if self.region == 'action' else self.target_cond_data
            show_fields = cond_data[combo.currentData()].split(',')
            current_field_key = combo.objectName().split('_')[1]
            for field in dynamic_fields:
                if field.objectName().split('_')[1] != current_field_key:
                    # self.fol_target.removeWidget(field)
                    # self.fol_action.removeWidget(field)
                    field.setParent(None)
            for item in self.step[self.region + 'ArgsVOS']:
                field_key = item['fieldKey']
                if field_key in show_fields:
                    cond_field = self.add_dynamic_field(field_key, item['fieldType'], item['fieldName'])
                    if isinstance(cond_field, QComboBox) and item['robotDataDicts'] is not None:
                        for cb_item in item['robotDataDicts']:
                            cond_field.addItem(cb_item['dictName'], cb_item['dictCode'])
                        if hasattr(item,'fieldValue'):
                            cond_field.setCurrentText(item['fieldValue'])
                    else:
                        if hasattr(item,'fieldValue'):
                            cond_field.setText(item['fieldValue'])

    def is_cond_field(self, key):
        cond_data = self.action_cond_data if self.region == 'action' else self.target_cond_data
        if len(cond_data) > 0:
            for val in cond_data.values():
                if key in val.split(','):
                    return True
        return False

    def add_dynamic_field(self, field_key, field_type, field_name):
        label = QLabel(self.tab_target)
        label.setObjectName(u"lab_" + field_key)
        label.setText(field_name)
        if field_type == 'singleDropList':
            field = QComboBox(self.tab_target)
        else:
            field = QLineEdit(self.tab_target)
        field.setObjectName(u"fid_" + field_key)

        if self.region == 'action':
            i = 0 if (self.action_fields == []) else len(self.action_fields)/2
            self.fol_action.setWidget(i,  QFormLayout.LabelRole, label)
            self.fol_action.setWidget(i,  QFormLayout.FieldRole, field)
            self.action_fields.append(label)
            self.action_fields.append(field)
        else:
            i = 0 if (self.target_fields == []) else len(self.target_fields)/2
            self.fol_target.setWidget(i,  QFormLayout.LabelRole, label)
            self.fol_target.setWidget(i,  QFormLayout.FieldRole, field)
            self.target_fields.append(label)
            self.target_fields.append(field)
        return field

    def on_save_click(self):
        self.step['stepName'] = self.let_step_name.text()
        self.step_item.setText(self.let_step_name.text())
        self.step_item.setData(1, self.step)
        print()
        self.close()

    def on_run_click(self):
        print('run_click')
