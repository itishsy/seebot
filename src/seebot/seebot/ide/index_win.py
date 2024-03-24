from PySide6.QtWidgets import (QApplication, QWidget, QMainWindow,  QTableWidget, QTreeWidget, QTableWidgetItem, QLabel, QTreeWidgetItem, QMessageBox, QMenu)
from PySide6.QtCore import (Qt, QEvent, QObject, QPoint, QByteArray, QDataStream, QModelIndex,QIODevice, QMimeData)
from PySide6.QtGui import QGuiApplication, QCursor, QCloseEvent, QDropEvent, QMouseEvent, QDragEnterEvent, QDragLeaveEvent, \
    QDrag, QPixmap, QPainter, QPen, QBrush, QColor

from seebot.ide.index import Ui_frm_flow_config
from seebot.ide.login_win import LoginWin
import seebot.ide.editor_win as editor
from seebot.ide.storage import Storage
from seebot.ide.service import Service


import json
import os


class IndexWin(QMainWindow, Ui_frm_flow_config):
    def __init__(self, parent=None):
        self.username = None
        self.service = None
        self.storage = Storage()

        super(IndexWin, self).__init__(parent)
        self.setupUi(self)
        self.app_code = None
        self.flow_code = None
        self.task_code = None
        self.apps = None
        self.flow_data = None
        self.task_data = None
        self.task_Args_data = None
        # self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowSystemMenuHint)
        screen_height = QGuiApplication.screenAt(QCursor().pos()).geometry().height()
        if self.size().height() > screen_height:
            self.setFixedSize(self.size().width(), screen_height - 60)
        else:
            self.setFixedSize(self.size())
        self.tbl_steps.setColumnWidth(0, 320)
        self.tbl_steps.setColumnWidth(1, 100)
        self.tbl_args.setColumnWidth(0, 80)
        self.tbl_args.setColumnWidth(1, 100)
        self.tbl_args.setColumnWidth(2, 230)
        self.btn_sync.setStyleSheet("color:" + QColor(255, 51, 204).name())
        # self.tbl_steps.mouseReleaseEvent = self.tableDragEvent.mouseReleaseEvent

    def show(self) -> None:
        if self.service is None:
            session = self.storage.find_value('session')
            if session is not None and len(session) > 0:
                ss = session.split('`')
                if len(ss) == 3:
                    self.service = Service(ss[0], ss[2])
                    self.username = ss[1]
        if self.service is None:
            self.win = LoginWin()
            self.win.pre_win = self
            self.win.show()
        else:
            super(IndexWin, self).show()
            self.setWindowTitle('seebot-ide 连接到 ' + self.service.server)
            # self.btn_sync.hide()
            self.load_action_tree()
            self.load_app_combo()
            self.btn_save.clicked.connect(self.on_save_click)
            self.btn_run.clicked.connect(self.on_run_click)
            self.btn_sync.clicked.connect(self.on_sync_click)
            self.tbl_steps.setAcceptDrops(True)
            self.tbl_steps.doubleClicked.connect(self.on_edit_click)
            self.tableDragEvent = TableRowDrag()
            self.tableDragEvent.table(self.tbl_steps)
            self.tableDragEvent.tree(self.trw_actions)
            self.tableDragEvent.service(self.service)
            self.tbl_steps.installEventFilter(self.tableDragEvent)
            self.tbl_steps.dropEvent = self.tableDragEvent.dropEvent
            self.tbl_steps.dragEnterEvent = self.tableDragEvent.dragEnterEvent
            setattr(self.tbl_steps, 'changed', False)

    def closeEvent(self, event: QCloseEvent) -> None:
        if hasattr(self, 'win'):
            self.win.close()
        self.close()
        # self.pre_win.show()

    def load_app_combo(self):
        self.cmb_app.clear()
        self.cmb_app.addItem("==请选择==")
        self.cmb_flow.clear()
        self.cmb_flow.addItem("==请选择==")
        self.cmb_task.clear()
        self.cmb_task.addItem("==请选择==")

        self.apps = self.service.find_all_app()
        for item in self.apps:
            self.cmb_app.addItem(item['appName'], item)
        res = self.storage.find_value('session_app')
        if len(res) != 0:
            res = res.split('`')
        if len(res) == 3:
            self.cmb_app.setCurrentText(res[0])
            self.on_app_change()
            self.cmb_flow.setCurrentText(res[1])
            self.cmb_task.setCurrentText(res[2])
            # self.app_code = self.cmb_app.currentData()['appCode']
            # self.flow_code = self.cmb_flow.currentData()["flowCode"]
            # self.task_code = self.cmb_task.currentData()
        self.cmb_app.currentTextChanged.connect(self.on_app_change)

    def on_app_change(self):
        self.cmb_flow.clear()
        self.cmb_flow.addItem("==请选择==")
        self.cmb_task.clear()
        self.cmb_task.addItem("==请选择==")
        app_code = self.cmb_app.currentData()['appCode']
        if app_code is not None:
            data = self.service.find_flow(app_code)
            self.flow_data = data["data"]
            for item in data["data"]:
                self.cmb_flow.addItem(item['flowName'], item)
            self.cmb_flow.currentIndexChanged.connect(self.on_flow_change)

            data = self.service.find_task(app_code)
            self.task_data = data["data"]
            for item in data["data"]:
                if item['companyName'] is not None and item['accountNumber'] is not None:
                    text = item['companyName']+'('+item['accountNumber']+')'
                    self.cmb_task.addItem(text, item)
            self.cmb_task.currentIndexChanged.connect(self.on_task_change)

    def on_flow_change(self):
        flow = self.cmb_flow.currentData()
        flow_code = flow['flowCode']
        cache_flow = self.storage.find_flow(flow_code)
        steps = self.service.find_step(flow_code)
        if cache_flow is None:
            self.storage.init_flow(flow_code, steps)
        else:
            is_sync = cache_flow['is_sync']
            updated = cache_flow['updated']
            if is_sync == 1:
                self.storage.init_flow(flow_code, steps)
            else:
                msg_code = QMessageBox.question(self, "选择流程源", "本地缓存流程未同步到服务器，【是】加载本地，【否】加载服务器", QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
                if msg_code == QMessageBox.StandardButton.No:
                    print(msg_code)
                else:
                    print(msg_code)

        self.load_step_data()
        # self.service.upset_setting('remember_app', self.cmb_app.currentText() + '`' + self.cmb_flow.currentText() + '`' + self.cmb_task.currentText())

    def on_task_change(self):
        self.task_code = self.cmb_task.currentData()
        if self.task_code is not None:
            self.load_task_data()
            self.service.upset_setting('remember_app', self.cmb_app.currentText() + '`' + self.cmb_flow.currentText() + '`' + self.cmb_task.currentText())

    def load_action_tree(self):
        self.actions = self.service.find_action()["data"]
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
        flow_code = self.cmb_flow.currentData()['flowCode']
        flow = self.storage.find_flow(flow_code)
        self.steps = json.loads(flow['steps'])
        for step in self.steps:
            self.append_row(step)
        self.tbl_steps.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tbl_steps.customContextMenuRequested.connect(self.show_context_menu)
        if flow['is_sync'] == 0:
            self.btn_sync.setText("当前流程未同步")
            self.btn_sync.setStyleSheet("color:" + QColor(255, 0, 0).name())
        else:
            self.btn_sync.setText("流程已同步")
            self.btn_sync.setStyleSheet("color:" + QColor(244, 204, 204).name())

    def load_task_data(self):
        setattr(self.tbl_steps, 'changed', False)
        self.tbl_args.setRowCount(0)
        if self.task_code is not None:
            data = self.service.find_task_args(self.app_code, self.task_code)
            self.task_Args_data = data["data"]
            for item in data["data"]:
                self.append_args_row(item['formName'], item['argsKey'], item['argsValue'])

    def show_context_menu(self, pos):
        item = self.tbl_steps.itemAt(pos)
        if item is None or item not in self.tbl_steps.selectedItems():
            return

        menu = QMenu(self.tbl_steps)
        edit_action = menu.addAction('编辑')
        menu.addSeparator()
        run_to_action = menu.addAction('运行到此步骤')
        run_this_action = menu.addAction('运行此步骤')
        run_from_action = menu.addAction('此步骤开始运行')
        menu.addSeparator()
        delete_action = menu.addAction('删除')
        action = menu.exec(self.tbl_steps.viewport().mapToGlobal(pos))
        if action == edit_action:
            self.on_edit_click()
        elif action == run_to_action:
            QMessageBox.information(self, "操作", "运行到此步骤")
        elif action == run_this_action:
            QMessageBox.information(self, "操作", "运行此步骤")
        elif action == run_from_action:
            QMessageBox.information(self, "操作", "此步骤开始运行")
        elif action == delete_action:
            idx = self.tbl_steps.selectedIndexes()
            row = idx[0].row().real
            self.tbl_steps.removeRow(row)
            self.tbl_steps.changed = False

    def append_row(self, step):
        if 'stepName' not in step:
            return

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
        self.tbl_steps.changed = True

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
            self.win = editor.EditorWin()
            self.win.step = items[0].data(1)
            self.win.base = self.tbl_steps
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
        if self.tbl_steps.changed:
            steps = []
            row_count = self.tbl_steps.rowCount()
            for i in range(row_count):
                data = self.tbl_steps.item(i, 0).data(1)
                data['number'] = i + 1
                steps.append(data)
            print(steps)
            res = self.service.save_flow_steps(self.flow_code, steps)
            QMessageBox.information(self, "结果", '保存成功' if res else '保存失败')
            self.load_step_data()

    def on_run_click(self):
        #self.win = running.FlowRunningWin()
        #screen = QApplication.primaryScreen().geometry()
        #x = screen.width() - self.win.frameGeometry().width()
        #y = screen.height() - self.win.frameGeometry().height()
        #self.win.move(x, 0)
        #self.win.show()
        self.current_app = None
        self.current_flow = None
        self.current_task = None
        for item in self.apps:
            if item['appCode'] == self.app_code:
                self.current_app = item
                continue
        for item in self.flow_data:
            if item['flowCode'] == self.flow_code:
                self.current_flow = item
                continue
        for item in self.task_data:
            if item['taskCode'] == self.task_code:
                self.current_task = item
                continue
        self.app_args = json.loads(self.current_app['appArgs'])

        flow_args = {"appCode": self.app_code,
                    "flowCode": self.flow_code,
                    "flowName": self.current_flow['flowName'],
                    "declareSystem": self.current_flow['declareSystem'],
                    "addrName": self.app_args['addrName'],
                    "addrId": self.app_args['addrId'],
                    "businessType": self.app_args['businessType'],
                    "taskCode": self.task_code,
                    "taskStatus": self.current_task['status'],
                    "clientId": self.current_task['clientId'],
                    "machineCode": self.current_task['machineCode']
                    }
        chrome_args = {
            "driverPath": os.path.abspath(".") + "\\robot\\chrome\\driver\\chromedriver.exe".replace('\r', '\\r'),
            "pluginPath": os.path.abspath(".") + "\\robot\\chrome\\plugin\\chrome".replace('\r', '\\r'),
            "sourcePath": os.path.abspath(".") + "\\robot\\chrome\\source\\chrome.exe".replace('\r', '\\r')
        }
        for item in self.task_Args_data:
            flow_args.update({item['argsKey']: item['argsValue']})

        res = self.service.debug_flow_step(self.flow_code, flow_args, chrome_args)
        if res['code'] == 200:
            QMessageBox.information(self, "结果", '启动成功')
        else:
            QMessageBox.information(self, "失败", res['message'])

    def on_sync_click(self):
        res = self.service.sync_flow_steps(self.flow_code)
        if res:
            self.load_step_data()
        QMessageBox.information(self, "结果", '同步成功' if res else '同步失败')


class TableRowDrag(QTableWidget):

    def table(self, table):
        self.tb = table

    def tree(self, tree):
        self.tr = tree

    def service(self, service):
        self.service = service

    def dropEvent(self, event: QDropEvent) -> None:
        self.target_row = self.tb.indexAt(event.pos()).row()
        # print('drag from tree: row:' + str(self.target_row))

        self.tb.changed = True
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
            brush = QBrush(QColor(255, 204, 204))
            self.tb.item(self.target_row, 0).setBackground(brush)
            self.tb.item(self.target_row, 1).setBackground(brush)
            # self.tb.selectRow(self.target_row)
            self.tb.clearSelection()
            del self.source_row
            self.refresh_number()
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
        self.win.step = self.init_step(action_code, rows)
        self.win.action_name = action_name
        self.win.number = rows
        self.win.base = self
        self.win.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.win.show()

    def init_step(self, action_code, number):
        target_args = self.service.find_target_args(action_code)
        action_args = self.service.find_action_args(action_code)
        return {'id': None, 'flowCode': None, 'groupCode': None, 'stepCode': None, 'stepName': '',
                'actionCode': action_code, 'actionArgs': '{}', 'targetArgs': '{}', 'number': number,
                'level': 1, 'status': 1, 'failedRetry': None, 'failedStrategy': 0, 'failedSkipTo': '',
                'skipTo': '登录成功?', 'falseSkipTo': None, 'skipCondition': '', 'waitBefore': None,
                'waitAfter': None, 'timeout': 10, 'type': None, 'openEdit': None,
                'actionArgsVOS': action_args["data"], 'targetArgsVOS': target_args["data"], 'trueSkipTo': ''}

    def add_step_ok(self):
        if hasattr(self, 'win'):
            step = self.win.step
            new_number = step['number']
            if new_number == self.win.number + 1:
                row_count = self.tb.rowCount()
                self.tb.insertRow(row_count)
                for i in reversed(range(new_number, row_count)):
                    self.tb.setItem(i+1, 0, self.tb.takeItem(i, 0))
                    self.tb.setItem(i+1, 1, self.tb.takeItem(i, 1))

                brush = QBrush(QColor(255, 204, 255))
                item_0 = QTableWidgetItem(str(step['stepName']))
                item_0.setData(1, step)
                item_0.setBackground(brush)
                self.tb.setItem(new_number, 0, item_0)
                item_1 = QTableWidgetItem(str(self.win.action_name))
                item_1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item_1.setBackground(brush)
                self.tb.setItem(new_number, 1, item_1)
                self.tb.clearSelection()
                print(self.win.number)
                print(step['number'])
                self.refresh_number()
                self.tb.changed = True

    def refresh_number(self):
        row_count = self.tb.rowCount()
        for i in range(row_count):
            data = self.tb.item(i, 0).data(1)
            data['number'] = i + 1
            self.tb.item(i, 0).setData(1, data)


class TreeItemDrag(QTreeWidget):
    def tree(self, tree):
        self.tree = tree

    def dragLeaveEvent(self, event: QDragLeaveEvent) -> None:
        item = self.tree.currentItem()
        print(item.text(0))
