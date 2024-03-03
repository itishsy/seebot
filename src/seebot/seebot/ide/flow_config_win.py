from PySide6.QtWidgets import (QApplication, QWidget, QMainWindow, QTableWidget, QTreeWidget, QTableWidgetItem, QLabel, QTreeWidgetItem, QMessageBox, QMenu)
from PySide6.QtCore import (Qt, QEvent, QObject, QPoint, QByteArray, QDataStream, QIODevice, QMimeData)
from PySide6.QtGui import QGuiApplication, QCursor, QCloseEvent, QDropEvent, QMouseEvent, QDragEnterEvent, QDragLeaveEvent, QDrag, QPixmap, QPainter, QPen

from seebot.ide.flow_config import Ui_frm_flow_config
import seebot.ide.flow_debug_win as debug
import seebot.ide.flow_running_win as running
import seebot.ide.step_editor_win as editor
from seebot.ide.api import Api

import seebot.utils.sqlite as db

api = Api()


class FlowConfigWin(QMainWindow, Ui_frm_flow_config):
    def __init__(self, parent=None):
        super(FlowConfigWin, self).__init__(parent)
        self.setupUi(self)
        self.app_code = None
        self.flow_code = None
        self.task_code = None
        # self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowSystemMenuHint)
        screen_height = QGuiApplication.screenAt(QCursor().pos()).geometry().height()
        if self.size().height() > screen_height:
            self.setFixedSize(self.size().width(), screen_height - 60)
        else:
            self.setFixedSize(self.size())
        self.tbl_steps.setColumnWidth(0, 360)
        self.tbl_steps.setColumnWidth(1, 120)
        self.tbl_args.setColumnWidth(1, 130)
        self.tbl_args.setColumnWidth(2, 260)

        # self.tbl_steps.mouseReleaseEvent = self.tableDragEvent.mouseReleaseEvent

    def show(self) -> None:
        super(FlowConfigWin, self).show()
        self.load_action_tree()
        self.load_app_data()
        # self.load_step_data()
        self.btn_save.clicked.connect(self.on_save_click)
        self.btn_run.clicked.connect(self.on_run_click)
        self.btn_debug.clicked.connect(self.on_debug_click)
        self.tbl_steps.setAcceptDrops(True)
        self.tbl_steps.doubleClicked.connect(self.on_edit_click)
        self.tableDragEvent = TableRowDrag()
        self.tableDragEvent.table(self.tbl_steps)
        self.tableDragEvent.tree(self.trw_actions)
        self.tbl_steps.installEventFilter(self.tableDragEvent)
        self.tbl_steps.dropEvent = self.tableDragEvent.dropEvent
        self.tbl_steps.dragEnterEvent = self.tableDragEvent.dragEnterEvent

    def closeEvent(self, event: QCloseEvent) -> None:
        self.close()
        # self.pre_win.show()

    def load_app_data(self):
        data = api.find_app()
        self.cmb_app.clear()
        self.cmb_app.addItem("==请选择==")
        self.cmb_flow.clear()
        self.cmb_flow.addItem("==请选择==")
        for item in data["data"]:
            self.cmb_app.addItem(item['appName'], item['appCode'])
        res = db.query("select value from setting where key='remember_app'")
        if len(res) > 0:
            sta = res[0]['value'].split('`')
            if len(sta) == 3:
                self.cmb_app.setCurrentText(sta[0])
                self.on_app_change()
                self.cmb_flow.setCurrentText(sta[1])
                self.app_code = self.cmb_flow.currentData()
                self.cmb_task.setCurrentText(sta[2])
                self.task_code = self.cmb_task.currentData()
        self.cmb_app.currentTextChanged.connect(self.on_app_change)

    def on_app_change(self):
        self.app_code = self.cmb_app.currentData()
        self.cmb_flow.clear()
        self.cmb_flow.addItem("==请选择==")
        self.cmb_task.clear()
        self.cmb_task.addItem("==请选择==")
        if self.app_code is not None:
            data = api.find_flow(self.app_code)
            for item in data["data"]:
                self.cmb_flow.addItem(item['flowName'], item['flowCode'])
            self.cmb_flow.currentIndexChanged.connect(self.on_flow_change)

            data = api.find_task(self.app_code)
            for item in data["data"]:
                if item['companyName'] is not None and item['accountNumber'] is not None:
                    text = item['companyName']+'('+item['accountNumber']+')'
                    self.cmb_task.addItem(text, item['taskCode'])
            self.cmb_task.currentIndexChanged.connect(self.on_task_change)

    def on_flow_change(self):
        self.flow_code = self.cmb_flow.currentData()
        self.data_mode = 'server'
        if self.flow_code is not None:
            self.load_step_data()

    def on_task_change(self):
        self.task_code = self.cmb_task.currentData()
        if self.task_code is not None:
            self.load_task_data()


    def load_action_tree(self):
        self.actions = api.find_action()["data"]
        self.trw_actions.setColumnWidth(0, 200)
        self.trw_actions.setHeaderHidden(True)
        group = []
        for act in self.actions:
            if act['groupName'] not in group:
                group.append(str(act['groupName']))
        group_items = []
        for group_name in group:
            top = QTreeWidgetItem()
            top.setText(0, group_name)
            group_items.append(top)
            for a in self.actions:
                if a['groupName'] == group_name:
                    child = QTreeWidgetItem()
                    child.setText(0, str(a['actionName']))
                    child.setData(0, 1, a['actionCode'])
                    child.setToolTip(0, a['comment'])
                    top.addChild(child)
        self.trw_actions.addTopLevelItems(group_items)
        self.trw_actions.expandAll()
        self.trw_actions.setDragEnabled(True)
        self.tree_item_drag = TreeItemDrag()
        self.tree_item_drag.tree(self.trw_actions)
        # self.startDrag = self.trw_actions.startDrag
        self.trw_actions.dragLeaveEvent = self.tree_item_drag.dragLeaveEvent

    def load_step_data(self):
        self.tbl_steps.setRowCount(0)
        if self.data_mode == 'server':
            data = api.find_step(self.flow_code)
            self.steps = data["data"]
        else:
            sql = "SELECT step_code as stepCode, step_name as stepName, action_code as actionCode, number FROM flow_step"
            self.steps = db.query(sql)

        for step in self.steps:
            self.append_row(step)
        self.tbl_steps.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tbl_steps.customContextMenuRequested.connect(self.show_context_menu)

    def load_task_data(self):
        self.tbl_args.setRowCount(0)
        if self.task_code is not None:
            data = api.find_task_args(self.app_code, self.task_code)
            for item in data["data"]:
                self.append_args_row(item['formName'], item['argsKey'], item['argsValue'])

    def show_context_menu(self, pos):
        item = self.tbl_steps.itemAt(pos)
        if item is None or item not in self.tbl_steps.selectedItems():
            return

        menu = QMenu(self.tbl_steps)
        edit_action = menu.addAction('编辑')
        menu.addSeparator()
        add_action = menu.addAction('插入')
        menu.addSeparator()
        run_this_action = menu.addAction('运行此步骤')
        run_from_action = menu.addAction('此步骤开始运行')
        menu.addSeparator()
        delete_action = menu.addAction('删除')
        action = menu.exec(self.tbl_steps.viewport().mapToGlobal(pos))
        if action == edit_action:
            self.on_edit_click()
        elif action == add_action:
            self.on_edit_click()
        elif action == run_this_action:
            QMessageBox.information(self, "操作", "运行此步骤")
        elif action == run_from_action:
            QMessageBox.information(self, "操作", "此处开始运行")
        elif action == delete_action:
            QMessageBox.information(self, "操作", "删除")

    def append_row(self, step):
        name = step['stepName']
        action = self.get_action_by_code(step['actionCode'])
        rows = self.tbl_steps.rowCount()
        self.tbl_steps.insertRow(rows)
        item_name = QTableWidgetItem(str(name))
        item_name.setData(1, step)
        self.tbl_steps.setItem(rows, 0, item_name)
        item_type = QTableWidgetItem(str(action['actionName']))
        item_type.setToolTip(str(action['comment']))
        item_type.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tbl_steps.setItem(rows, 1, item_type)

    def append_args_row(self, type, key, value):
        rows = self.tbl_args.rowCount()
        self.tbl_args.insertRow(rows)
        item_type = QTableWidgetItem(str(type))
        self.tbl_args.setItem(rows, 0, item_type)
        item_name = QTableWidgetItem(str(key))
        self.tbl_args.setItem(rows, 1, item_name)
        item_value = QTableWidgetItem(str(value))
        self.tbl_args.setItem(rows, 2, item_value)

    def on_edit_click(self):
        items = self.tbl_steps.selectedItems()
        if items:
            self.win = editor.StepEditorWin()
            self.win.step = items[0].data(1)
            self.win.action_name = items[1].text()
            self.win.step_item = items[0]
            self.win.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.win.show()
        else:
            QMessageBox.critical(self, "请选择", "请先选择一行")

    # def get_step(self,code):
    #     for item in self.steps:
    #         if item['stepCode'] == code:
    #             return item

    def get_action_by_code(self, code):
        for act in self.actions:
            if act['actionCode'] == code:
                return act

    def on_save_click(self):
        print(self.steps)

    def on_run_click(self):
        self.win = running.FlowRunningWin()
        self.win.pre_win = self
        self.hide()
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() - self.win.frameGeometry().width()
        y = screen.height() - self.win.frameGeometry().height()
        self.win.move(x, y)
        self.win.show()

    def on_debug_click(self):
        self.win = debug.FlowDebugWin()
        self.win.pre_win = self
        self.hide()
        self.win.show()


class TableRowDrag(QTableWidget):

    def table(self, table):
        self.tb = table

    def tree(self, tree):
        self.tr = tree

    def dropEvent(self, event: QDropEvent) -> None:
        self.target_row = self.tb.indexAt(event.pos()).row()
        print('drag from tree: row:' + str(self.target_row))

        if hasattr(self, 'source_row'):
            if self.target_row == self.source_row:
                return

            if self.target_row == -1:
                self.target_row = self.tb.rowCount()

            items = self.get_moving_items()
            self.tb.removeRow(self.source_row)
            self.tb.insertRow(self.source_row)
            start = min(self.target_row, self.source_row)
            end = max(self.target_row, self.source_row)
            for row in range(start, end):
                self.tb.removeRow(row)
                self.tb.insertRow(row)
            for item in items:
                self.tb.setItem(start, 0, item[0])
                self.tb.setItem(start, 1, item[1])
                start = start + 1
            self.tb.selectRow(self.target_row)
            del self.source_row
        else:
            self.tb.selectRow(self.target_row)
            tr_item = self.tr.currentItem()
            if tr_item is not None:
                print(tr_item.text(0))
                print(tr_item.data(0, 1))
                self.add_step(tr_item.data(0, 1), tr_item.text(0), self.target_row)

    def eventFilter(self, object: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.ChildAdded:
            self.source_row = object.currentRow()
            return False
        else:
            # if(event.type() == 10):
            #     tr_item = self.tr.currentItem()
            #     if tr_item is not None:
            #         print(tr_item.text(0))
            return super(TableRowDrag, self).eventFilter(object, event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        row = self.tb.indexAt(event.pos())
        print('mouseMoveEvent, row:' + str(row))
        super(TableRowDrag, self).mouseMoveEvent(event)

    # def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    #     row = self.tb.indexAt(event.pos())
    #     print('dragLeaveEvent, row:' + str(row))
    #     super(TableRowDrag, self).mouseReleaseEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        # row = self.tb.indexAt(event.pos())
        # print('dragEnterEvent, row:' + str(row))
        event.acceptProposedAction()

    def get_moving_items(self):
        items = []
        if self.target_row < self.source_row:
            items.append([self.tb.takeItem(self.source_row,0), self.tb.takeItem(self.source_row,1)])
            for row in range(self.target_row, self.source_row):
                items.append([self.tb.takeItem(row,0),self.tb.takeItem(row,1)])
        else:
            source = [self.tb.takeItem(self.source_row,0), self.tb.takeItem(self.source_row,1)]
            for row in range(self.source_row+1, self.target_row+1):
                items.append([self.tb.takeItem(row,0),self.tb.takeItem(row,1)])
            items.append(source)
        return items

    def add_step(self, action_code, action_name, rows):
        self.win = editor.StepEditorWin()
        self.win.action_code = action_code
        self.win.action_name = action_name
        self.win.number = rows
        self.win.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.win.show()

class TreeItemDrag(QTreeWidget):
    def tree(self, tree):
        self.tree = tree

    def dragLeaveEvent(self, event: QDragLeaveEvent) -> None:
        item = self.tree.currentItem()
        print(item.text(0))
