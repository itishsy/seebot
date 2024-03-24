from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QFormLayout, QComboBox, QCheckBox, QLineEdit, QMessageBox
from PySide6.QtCore import Qt, QObject, QRect
from PySide6.QtGui import QBrush, QColor

from seebot.ide.editor import Ui_frm_step_edit
import json
import copy


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
        self.btn_run.clicked.connect(self.on_run_click)

    def show(self) -> None:
        super(EditorWin, self).show()
        if hasattr(self, 'step'):
            self.setWindowTitle('编辑步骤 【' + self.action_name + '】')
        else:
            self.setWindowTitle('新增步骤 【' + self.action_name + '】')
        self.ori_step = copy.deepcopy(self.step)
        self.other_steps = self.fetch_all_other_step()
        self.load_step_data()
        self.fetch_cond_data()

        size1 = len(self.step["targetArgsVOS"])
        size2 = len(self.step["actionArgsVOS"])
        print(self.grb_action.geometry())
        print(self.fol_action.geometry())
        if size1 < 6 and size2 > 6:
            offsize = 70
            # self.fol_target.setVerticalSpacing(size1)
            self.grb_target.setFixedHeight(self.grb_target.height() - offsize)
            # self.fol_action.setVerticalSpacing(size2)
            self.grb_action.setGeometry(self.grb_action.geometry().x(), self.grb_action.geometry().y() - offsize,
                                        self.grb_action.geometry().width(), self.grb_action.geometry().height() + 80)
            # self.grb_action.setFixedHeight(self.grb_action.height() + 30)
            rect = QRect()
            rect.adjust(self.fol_action.geometry().x(), self.fol_action.geometry().y(),
                                        self.fol_action.geometry().width(), self.fol_action.geometry().height() + 80)
            # self.fol_action.setVerticalSpacing(size2)
            self.fol_action.setGeometry(rect)
            # self.fol_action.setSizeConstraint()
            print(self.grb_action.geometry())
            print(self.fol_action.geometry())

        self.load_dynamic_data('target')
        self.load_dynamic_data('action')

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
                        for step_name in self.other_steps:
                            fid.addItem(step_name, step_name)
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

    def fetch_all_other_step(self):
        steps = []
        tbl_steps = self.base.tb if hasattr(self.base, 'tb') else self.base
        row_count = tbl_steps.rowCount()
        for i in range(row_count):
            name = tbl_steps.item(i, 0).text()
            if name != self.step['stepName']:
                steps.append(name)
        return steps

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
            if ori_args[field_key] != new_val:
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
            self.step_item.setText(self.step['stepName'])
            self.step_item.setData(1, self.step)
            brush = QBrush(QColor(255, 255, 204))
            self.step_item.setBackground(brush)
            self.base.changed = True
            print(self.step)
        else:
            self.step['number'] = self.step['number'] + 1
            self.base.add_step_ok()
        self.close()

    def on_run_click(self):
        print('run_click')
