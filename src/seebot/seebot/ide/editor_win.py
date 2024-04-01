from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QFormLayout, QComboBox, QCheckBox, QLineEdit, QMessageBox
from PySide6.QtCore import Qt, QObject, QRect
from PySide6.QtGui import QBrush, QColor

from seebot.ide.editor import Ui_frm_step_edit
import json
import copy

role = Qt.ItemDataRole.UserRole


class EditorWin(QMainWindow, Ui_frm_step_edit):
    def __init__(self, parent=None):
        super(EditorWin, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())
        # self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowMinMaxButtonsHint)
        self.target_fields = []
        self.target_cond_data = {}
        self.action_fields = []
        self.action_cond_data = {}
        self.changed_fields = []
        self.btn_save.clicked.connect(self.on_save_click)
        self.btn_close.clicked.connect(self.close)
        self.btn_run.clicked.connect(self.on_run_click)

    def show(self) -> None:
        super(EditorWin, self).show()
        if hasattr(self, 'step'):
            self.setWindowTitle('编辑步骤 【' + self.action_name + '】')
        else:
            self.setWindowTitle('新增步骤 【' + self.action_name + '】')
        self.ori_step = copy.deepcopy(self.step)
        self.other_steps = self.base.fetch_steps()
        self.load_step_data()
        self.fetch_cond_data()

        target_args = self.step["targetArgsVOS"]
        action_args = self.step["actionArgsVOS"]
        t_size = len(target_args)
        a_size = len(action_args)
        if t_size > 6 or a_size > 6:
            if self.real_long_size(target_args) or self.real_long_size(action_args):
                offset = (a_size - t_size) * 20
                if offset > 0:
                    offset = 80 if offset > 80 else offset
                else:
                    offset = -80 if offset < -80 else offset
                self.grb_target.setGeometry(
                    QRect(self.grb_target.geometry().x(),
                          self.grb_target.geometry().y(),
                          self.grb_target.geometry().width(),
                          self.grb_target.geometry().height() - offset))
                self.formLayoutWidget_3.setGeometry(
                    QRect(self.formLayoutWidget_3.geometry().x(),
                          self.formLayoutWidget_3.geometry().y(),
                          self.formLayoutWidget_3.geometry().width(),
                          self.formLayoutWidget_3.geometry().height() - offset))
                self.grb_action.setGeometry(
                    QRect(self.grb_action.geometry().x(),
                          self.grb_action.geometry().y() - offset,
                          self.grb_action.geometry().width(),
                          self.grb_action.geometry().height() + offset))
                self.formLayoutWidget_4.setGeometry(
                    QRect(self.formLayoutWidget_4.geometry().x(),
                          self.formLayoutWidget_4.geometry().y(),
                          self.formLayoutWidget_4.geometry().width(),
                          self.formLayoutWidget_4.geometry().height() + offset))

        self.load_dynamic_data('target')
        self.load_dynamic_data('action')

    @staticmethod
    def real_long_size(args):
        if len(args) > 6:
            for arg in args:
                if 'cond' in arg and len(arg['cond'].strip()) > 0:
                    cond = json.loads(arg['cond'])
                    if isinstance(cond, dict):
                        for key, value in cond.items():
                            if len(value.split(',')) > 6:
                                return True
        return False

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
                    current_text = self.step[key]
                    if key in ['skipTo', 'failedSkipTo']:
                        for step in self.other_steps:
                            fid.addItem(step['stepName'], step['stepName'])
                    if self.step[key] is not None:
                        fid.setCurrentText(str(current_text))
                else:
                    fid.editingFinished.connect(self.editing_finished)
                    if self.step[key] is not None:
                        fid.setText(str(self.step[key]))

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
        label.setMinimumWidth(100)
        # label.setMinimumSize(100, 50)
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

        # if self.changed_nothing:
        #     if hasattr(self, 'step_item'):
        #         ori_step = self.step_item.data(1)
        #     else:
        #         ori_step = self.init_step()

        if len(fid_name_arr) > 1:
            vos_name = fid_name_arr[0]
            field_key = fid_name_arr[1]

            args_key = vos_name.replace('VOS', '')
            args = json.loads(self.step[args_key])
            args[field_key] = new_val
            self.step[args_key] = json.dumps(args, ensure_ascii=False)

            ori_args = json.loads(self.ori_step[args_key])
            if not hasattr(ori_args, field_key) or ori_args[field_key] != new_val:
                self.changed_fields.append(sender.objectName())

            for item in self.step[vos_name]:
                if item['fieldKey'] == field_key:
                    item['fieldValue'] = new_val
                    break
        else:
            self.step[fid_name] = new_val
            if self.ori_step[fid_name] != new_val:
                self.changed_fields.append(fid_name)

    def on_save_click(self):
        if len(self.changed_fields) == 0:
            self.close()
            return

        if self.step['stepName'] in self.other_steps:
            QMessageBox.information(self, "结果", '步骤名称不能重复')
            return

        int_fields = ['timeout', 'waitBefore', 'waitAfter', 'failedRetry']
        intersection = [x for x in self.changed_fields if x in int_fields]
        if len(intersection) > 0:
            for fid in intersection:
                val = getattr(self, 'fid_' + fid).text()
                if not val.isdigit():
                    QMessageBox.information(self, "结果", '请填写数字。'+fid)
                    return

        if hasattr(self, 'step_item'):
            self.step_item.setText(0, self.step['stepName'])
            self.step_item.setData(0, role, self.step)
            brush = QBrush(QColor(255, 255, 204))
            self.step_item.setBackground(0, brush)
            self.step_item.setBackground(1, brush)
            self.base.changed = True
            print(self.step)
        else:
            self.step['number'] = self.step['number'] + 1
            self.base.add_step_ok()
        self.close()

    def on_run_click(self):
        print('run_click')
