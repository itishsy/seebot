from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QFormLayout, QComboBox, QCheckBox, QLineEdit
from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QBrush, QColor

from seebot.ide.api import Api
from seebot.ide.step_editor import Ui_frm_step_edit
import json


class StepEditorWin(QMainWindow, Ui_frm_step_edit):
    def __init__(self, parent=None):
        super(StepEditorWin, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())
        # self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowMinMaxButtonsHint)
        self.target_fields = []
        self.target_cond_data = {}
        self.action_fields = []
        self.action_cond_data = {}
        self.changed_nothing = True
        self.btn_save.clicked.connect(self.on_save_click)
        self.btn_run.clicked.connect(self.on_run_click)

    def show(self) -> None:
        super(StepEditorWin, self).show()
        if hasattr(self, 'step'):
            self.setWindowTitle('编辑步骤 【' + self.action_name + '】')
        else:
            self.setWindowTitle('新增步骤 【' + self.action_name + '】')
            self.step = self.init_step()
        self.load_step_data()
        self.fetch_cond_data()
        self.load_dynamic_data('target')
        self.load_dynamic_data('action')

    def init_step(self):
        api = Api()
        target_args = api.find_target_args(self.action_code)
        action_args = api.find_action_args(self.action_code)
        return {'id': None, 'flowCode': None, 'groupCode': None, 'stepCode': None, 'stepName': '',
                'actionCode': self.action_code, 'actionArgs': '{}', 'targetArgs': '{}', 'number': self.number,
                'level': 1, 'status': 1, 'failedRetry': None, 'failedStrategy': 0, 'failedSkipTo': '',
                'skipTo': '登录成功?', 'falseSkipTo': None, 'skipCondition': '', 'waitBefore': None,
                'waitAfter': None, 'timeout': 10, 'type': None, 'openEdit': None,
                'actionArgsVOS': action_args["data"], 'targetArgsVOS': target_args["data"], 'trueSkipTo': ''}

    def load_step_data(self):
        print(self.step)

        for key in self.step.keys():
            fid_name = "fid_"+key
            if hasattr(self, fid_name):
                fid = getattr(self, fid_name)
                if isinstance(fid, QCheckBox):
                    fid.stateChanged.connect(self.editing_finished)
                    if key in ['status']:
                        fid.setChecked(False if self.step[key] == 1 else True)
                    else:
                        fid.setChecked(True if self.step[key] == 1 else False)
                elif isinstance(fid, QComboBox):
                    fid.currentTextChanged.connect(self.editing_finished)
                    if self.step[key] is not None:
                        fid.setCurrentText(str(self.step[key]))
                else:
                    fid.editingFinished.connect(self.editing_finished)
                    if self.step[key] is not None:
                        fid.setText(str(self.step[key]))


        # self.fid_stepName.setText(self.step['stepName'])
        # if self.step['status'] != 1:
        #     self.fid_status.setChecked(True)
        #
        #
        # self.fid_stepName.editingFinished.connect(self.editing_finished)
        # self.fid_status.editingFinished.connect(self.editing_finished)

    def load_dynamic_data(self, region):
        args_vos = self.step[region + "ArgsVOS"]

        if args_vos is None or len(args_vos) == 0:
            label = QLabel(self.tab_target)
            label.setText('操作' + self.action_name)
            self.fol_target.setWidget(0,  QFormLayout.LabelRole, label)
            return

        for item in args_vos:
            field_key = item['fieldKey']
            if self.is_cond_field(field_key, region):
                continue

            field = self.add_dynamic_field(region + 'ArgsVOS.' + field_key, item['fieldType'], item['fieldName'])
            if isinstance(field, QComboBox):
                current_text = ''
                for cb_item in item['robotDataDicts']:
                    field.addItem(cb_item['dictName'], cb_item['dictCode'])
                    if 'fieldValue' in item and item['fieldValue'] == cb_item['dictCode']:
                        current_text = cb_item['dictName']
                field.addItem('', '')
                field.setCurrentText(current_text)
                # else:
                #     field.setCurrentText('')
                if item['cond'] != '':
                    field.currentTextChanged.connect(self.on_dynamic_combo_change)
                    field.currentTextChanged.emit(current_text)
                field.currentIndexChanged.connect(self.editing_finished)
            else:
                if 'fieldValue' in item:
                    field.setText(item['fieldValue'])
                field.editingFinished.connect(self.editing_finished)

    def fetch_cond_data(self):
        for item in self.step["targetArgsVOS"]:
            if item['cond'] != '':
                self.target_cond_data = json.loads(item['cond'])

        for item in self.step["actionArgsVOS"]:
            if item['cond'] != '':
                self.action_cond_data = json.loads(item['cond'])

    def on_dynamic_combo_change(self, arg1):
        sender = self.sender()
        if sender is None or sender.parent() is None or sender.parent().parent() is None:
            print("ui元素层级异常")

        region = sender.parent().parent().objectName().split('_')[1]
        combo = None
        dynamic_fields = self.action_fields if region == 'action' else self.target_fields
        if arg1 == '' and sender is not None:
            for field in dynamic_fields:
                if field.objectName().split('_')[1] != sender.objectName().split('_')[1]:
                    field.setParent(None)
            return
        for f in dynamic_fields:
            if not isinstance(f, QLabel) and hasattr(f, 'currentText') and f.currentText() == arg1:
                combo = f
                break

        if combo is not None and combo.currentData() != '':
            cond_data = self.action_cond_data if region == 'action' else self.target_cond_data
            show_fields = []
            if combo.currentData() in cond_data:
                show_fields = cond_data[combo.currentData()].split(',')
            current_field_key = combo.objectName().split('_')[1]
            for field in dynamic_fields:
                if field.objectName().split('_')[1] != current_field_key:
                    # self.fol_target.removeWidget(field)
                    # self.fol_action.removeWidget(field)
                    field.setParent(None)
            for item in self.step[region + 'ArgsVOS']:
                field_key = item['fieldKey']
                if field_key in show_fields:
                    cond_field = self.add_dynamic_field(region + 'ArgsVOS.' + field_key, item['fieldType'], item['fieldName'])
                    if isinstance(cond_field, QComboBox):
                        if item['robotDataDicts'] is not None:
                            for cb_item in item['robotDataDicts']:
                                cond_field.addItem(cb_item['dictName'], cb_item['dictCode'])
                            cond_field.addItem('', '')
                            if 'fieldValue' in item and item['fieldValue'] is not None:
                                cond_field.setCurrentText(item['fieldValue'])
                        cond_field.currentIndexChanged.connect(self.editing_finished)
                    else:
                        if 'fieldValue' in item:
                            cond_field.setText(item['fieldValue'])
                        cond_field.editingFinished.connect(self.editing_finished)

    def is_cond_field(self, key, region):
        cond_data = self.action_cond_data if region == 'action' else self.target_cond_data
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

        if field_key.startswith('action'):
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

    def editing_finished(self):
        sender = self.sender()
        print(sender.objectName())
        fid_name = sender.objectName().replace('fid_', '')
        fid_name_arr = fid_name.split('.')

        if isinstance(sender, QComboBox):
            new_val = sender.currentData()
        elif isinstance(sender, QCheckBox):
            if fid_name in ['status']:
                new_val = 0 if sender.isChecked() else 1
            else:
                new_val = 1 if sender.isChecked() else 0
        else:
            new_val = sender.text()

        if self.changed_nothing:
            if hasattr(self, 'step_item'):
                ori_step = self.step_item.data(1)
            else:
                ori_step = self.init_step()

        if len(fid_name_arr) > 1:
            vos_name = fid_name_arr[0]
            field_key = fid_name_arr[1]

            args_key = vos_name.replace('VOS', '')
            args = json.loads(self.step[args_key])
            args[field_key] = new_val
            self.step[args_key] = json.dumps(args, ensure_ascii=False)

            if self.changed_nothing:
                ori_args = json.loads(ori_step[args_key])
                self.changed_nothing = ori_args[field_key] == new_val

            for item in self.step[vos_name]:
                if item['fieldKey'] == field_key:
                    item['fieldValue'] = new_val
                    break
        else:
            self.step[fid_name] = new_val
            if self.changed_nothing:
                self.changed_nothing = ori_step[fid_name] == new_val

    def on_save_click(self):
        if self.changed_nothing:
            self.close()
            return

        if hasattr(self, 'step_item'):
            self.step_item.setText(self.step['stepName'])
            self.step_item.setData(1, self.step)
            brush = QBrush(QColor(255, 255, 204))
            self.step_item.setBackground(brush)
            print(self.step)
        else:
            self.step['number'] = self.step['number'] + 1
            self.base.add_step_ok()
        self.close()

    def on_run_click(self):
        print('run_click')
