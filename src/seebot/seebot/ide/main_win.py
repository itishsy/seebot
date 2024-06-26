from PySide6.QtWidgets import (QApplication, QWidget, QFrame, QMainWindow,  QTableWidget, QTreeWidget, QTableWidgetItem, QLabel, QTreeWidgetItem, QMessageBox, QMenu)
from PySide6.QtCore import (Qt, QEvent, QObject, QPoint, QByteArray, QDataStream, QModelIndex,QIODevice, QMimeData)
from PySide6.QtGui import QGuiApplication, QCursor, QCloseEvent, QDropEvent, QMouseEvent, QDragEnterEvent, QDragLeaveEvent, \
    QDrag, QPixmap, QPainter, QPen, QIcon, QBrush, QColor

from seebot.ide.main import Ui_frm_flow_config
from seebot.ide.login_win import LoginWin
import seebot.ide.editor_win as editor
from seebot.ide.storage import Storage
from seebot.ide.service import Service


import json
import os


role = Qt.ItemDataRole.UserRole


class MainWin(QMainWindow, Ui_frm_flow_config):
    def __init__(self, parent=None):
        self.username = None
        self.service = None
        self.storage = Storage()

        super(MainWin, self).__init__(parent)
        self.setupUi(self)

        self.tbl_args.setColumnWidth(0, 100)
        self.tbl_args.setColumnWidth(1, 230)

        self.btn_save.clicked.connect(self.on_save_click)
        self.btn_run.clicked.connect(self.on_run_click)
        self.btn_sync.clicked.connect(self.on_sync_click)
        self.btn_reload.clicked.connect(self.load_step_data)

        self.trw_actions.setDragEnabled(True)
        self.trw_actions.setAcceptDrops(False)
        self.trw_actions.setDragDropMode(QTreeWidget.DragDropMode.DragOnly)

        self.trw_steps.setAcceptDrops(True)
        self.trw_steps.setDragEnabled(True)
        self.trw_steps.setDragDropMode(QTreeWidget.DragDropMode.DragDrop)

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
            res = self.service.find_action()
            if res["code"] == 401:
                self.win = LoginWin()
                self.win.pre_win = self
                self.win.show()
            else:
                self.actions = res["data"]
                super(MainWin, self).show()
                self.setWindowTitle('seebot-ide 连接到 ' + self.service.server)
                # self.btn_sync.hide()
                self.load_action_tree()
                self.load_app_combo()
                # setattr(self.trw_steps, 'changed', False)

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

        apps = self.service.find_all_app()
        for item in apps:
            self.cmb_app.addItem(item['appName'], item)
        res = self.storage.find_value('session_app')
        if len(res) != 0:
            res = res.split('`')
        if len(res) == 3:
            self.cmb_app.setCurrentText(res[0])
            self.on_app_change()
            self.cmb_flow.setCurrentText(res[1])
            self.cmb_task.setCurrentText(res[2])
        self.cmb_app.currentTextChanged.connect(self.on_app_change)

    def on_app_change(self):
        self.cmb_flow.clear()
        self.cmb_flow.addItem("==请选择==")
        self.cmb_task.clear()
        self.cmb_task.addItem("==请选择==")
        app_code = self.cmb_app.currentData()['appCode']
        if app_code is not None:
            data = self.service.find_flow(app_code)
            for item in data["data"]:
                self.cmb_flow.addItem(item['flowName'], item)
            self.cmb_flow.currentIndexChanged.connect(self.on_flow_change)

            data = self.service.find_task(app_code)
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
        if cache_flow is not None and cache_flow['status'] == 0:
            msg_code = QMessageBox.question(self, "选择数据源", "本地流程与服务器不一致，【是】加载本地，【否】加载服务器", QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
            if msg_code == QMessageBox.StandardButton.No:
                self.storage.update_flow_status(flow_code, 2)
        self.load_step_data()
        self.storage.upset_key_value('session_app', self.cmb_app.currentText() + '`' + self.cmb_flow.currentText() + '`' + self.cmb_task.currentText())

    def on_task_change(self):
        task_code = self.cmb_task.currentData()["taskCode"]
        if task_code is not None:
            self.load_task_data()
            self.storage.upset_key_value('session_app', self.cmb_app.currentText() + '`' + self.cmb_flow.currentText() + '`' + self.cmb_task.currentText())

    def load_action_tree(self):
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
                    child.setData(0, role, a['actionCode'])
                    child.setToolTip(0, a['comment'])
                    top.addChild(child)
        self.trw_actions.addTopLevelItems(group_items)
        self.trw_actions.expandAll()
        # self.trw_actions.itemClicked.connect(self.action_item_clicked)

    # def action_item_clicked(self, item, column):
    #     item.setData(column, role, 123)

    def load_steps_tree(self, steps):
        self.trw_steps.setColumnCount(2)
        self.trw_steps.setHeaderHidden(True)
        group_items = []
        top = QTreeWidgetItem()
        for step in steps:
            level = step['level']
            name = step['stepName']
            action = self.get_action_by_code(step['actionCode'])
            action_name = action['actionName']
            if level == 0:
                top = QTreeWidgetItem()
                top.setText(0, name)
                top.setFirstColumnSpanned(True)
                top.setData(0, role, step)
                top.setText(1, action_name)
                group_items.append(top)
            else:
                child = QTreeWidgetItem()
                child.setText(0, name)
                child.setData(0, role, step)
                child.setText(1, action_name)
                top.addChild(child)
        self.trw_steps.addTopLevelItems(group_items)
        self.trw_steps.expandAll()
        # self.trw_steps.setStyleSheet(f"QTreeView::item{{height: 25px; }}")
        # self.trw_steps.doubleClicked.connect(self.double_click_event)
        self.trw_steps.mouseDoubleClickEvent = self.double_click_event
        self.trw_steps.itemChanged.connect(self.step_item_changed)
        # self.trw_steps.viewport().installEventFilter(self)
        # self.trw_steps.dropEvent = self.drop_event

        # self.trw_steps.setFrameShape(QFrame.Shape.Box)
        style = """
                    QTreeWidget {
                        color: #2c0606;
                        border: 1px solid #ccc;
                        font: 290 10pt "Microsoft YaHei UI";
                    }
                    QTreeWidget::item {
                        height: 26px;
                    }
                    QTreeWidget::item:selected {
                        background-color: #0078d7;
                        color: white;
                    }
                    QTreeWidget::branch: closed:has - children
                    {
                        image: url('icon/add.png');
                    }
                    QTreeWidget::branch: open:has - children
                    {
                        image: url('icon/close.png');
                    }
                """

        self.trw_steps.setStyleSheet(style)
        self.trw_steps.setColumnWidth(0, 320)
        self.trw_steps.setColumnWidth(1, 100)

    def double_click_event(self, event):
        index = self.trw_steps.indexAt(event.pos())
        if index.isValid():
            item = self.trw_steps.itemFromIndex(index)
            self.open_editor(item)

    def open_editor(self, item=None):
        if item is None:
            pass
        else:
            data = item.data(0, role)
            print(data)
            self.win = editor.EditorWin()
            self.win.step = data
            self.win.base = self
            self.win.action_name = item.text(1)
            self.win.step_item = item
            self.win.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.win.show()

    def step_item_changed(self, item, column):
        data = item.data(0, role)
        if data:
            print("item data:" + str(data))
            if isinstance(data, dict):
                return
            action = self.get_action_by_code(data)
            if action:
                item.setData(0, role, self.init_step(action['actionCode'],0))
                action_name = item.text(0)
                item.setText(0, '<' + action_name + '>')
                item.setText(1, action_name)
                self.open_editor(item)
            else:
                return

        brush = QBrush(QColor(255, 255, 204))
        item.setBackground(0, brush)
        item.setBackground(1, brush)
        print("item text:" + str(item.text(0)))
        items = self.trw_steps.selectedItems()
        if items is not None and len(items) > 0:
            selected_item = items[0]
            selected_data = selected_item.data(0, role)
            if selected_data is not None:
                child_count = selected_item.childCount()
                if child_count > 0:
                    for i in range(child_count):
                        new_child = QTreeWidgetItem()
                        new_child.setText(0, selected_item.child(i).text(0))
                        new_child.setText(1, selected_item.child(i).text(1))
                        new_child.setData(0, role, selected_item.child(i).data(0, role))
                        new_child.setBackground(0, brush)
                        new_child.setBackground(1, brush)
                        item.addChild(new_child)
                    self.trw_steps.expandItem(item)
                else:
                    item.setData(0, role, selected_data)
                self.remove_item(selected_item, column)

    def remove_item(self, item, column):
        if item.parent() is None:  # Check if it is a top-level item
            self.trw_steps.takeTopLevelItem(self.trw_steps.indexOfTopLevelItem(item))
            print(f"Removed top-level item: {item.text(column)}")
        else:
            parent = item.parent()
            parent.removeChild(item)
            print(f"Removed child item: {item.text(column)}")
        self.trw_steps.setCurrentItem(None)

    def init_step(self, action_code, number):
        target_args = self.service.find_target_args(action_code)
        action_args = self.service.find_action_args(action_code)
        return {'id': None, 'flowCode': None, 'groupCode': None, 'stepCode': None, 'stepName': '',
                'actionCode': action_code, 'actionArgs': '{}', 'targetArgs': '{}', 'number': number,
                'level': 1, 'status': 1, 'failedRetry': None, 'failedStrategy': 0, 'failedSkipTo': '',
                'skipTo': '', 'falseSkipTo': None, 'skipCondition': '', 'waitBefore': None,
                'waitAfter': None, 'timeout': 10, 'type': None, 'openEdit': None,
                'actionArgsVOS': action_args["data"], 'targetArgsVOS': target_args["data"], 'trueSkipTo': ''}


    def fetch_steps(self):
        steps = []
        for i in range(self.trw_steps.topLevelItemCount()):
            top_item = self.trw_steps.topLevelItem(i)
            print(top_item.text(0))
            top_data = top_item.data(0, role)
            if top_data is not None:
                top_data['number'] = len(steps) + 1
                steps.append(top_data)
            for j in range(top_item.childCount()):
                child_item = top_item.child(j)
                child_data = child_item.data(0, role)
                if child_data is not None:
                    child_data['number'] = len(steps) + 1
                    steps.append(child_data)
        return steps

    def load_step_data(self):
        flow_code = self.cmb_flow.currentData()['flowCode']
        cache_flow = self.storage.find_flow(flow_code)
        if cache_flow is None:
            steps = self.service.find_step(flow_code)
        else:
            steps = json.loads(cache_flow['steps'])

        self.trw_steps.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.trw_steps.customContextMenuRequested.connect(self.show_context_menu)
        if cache_flow is not None and cache_flow['status'] == 0:
            self.btn_sync.show()
            # self.btn_sync.setStyleSheet("color:" + QColor(255, 0, 0).name())
        else:
            self.btn_sync.hide()
            # self.btn_sync.setStyleSheet("color:" + QColor(244, 204, 204).name())
        self.trw_steps.clear()
        self.load_steps_tree(steps)

    def load_task_data(self):
        setattr(self.trw_steps, 'changed', False)
        self.tbl_args.setRowCount(0)
        app_code = self.cmb_app.currentData()['appCode']
        task_code = self.cmb_task.currentData()['taskCode']
        if task_code is not None:
            data = self.service.find_task_args(app_code, task_code)
            for item in data["data"]:
                rows = self.tbl_args.rowCount()
                self.tbl_args.insertRow(rows)
                item_name = QTableWidgetItem(str(item['argsKey']))
                self.tbl_args.setItem(rows, 0, item_name)
                item_value = QTableWidgetItem(str(item['argsValue']))
                self.tbl_args.setItem(rows, 1, item_value)

    def show_context_menu(self, pos):
        item = self.trw_steps.itemAt(pos)
        if item is None or item not in self.trw_steps.selectedItems():
            return

        menu = QMenu(self.trw_steps)
        edit_action = menu.addAction('编辑')
        menu.addSeparator()
        run_to_action = menu.addAction('运行到此步骤')
        run_this_action = menu.addAction('运行此步骤')
        run_from_action = menu.addAction('此步骤开始运行')
        menu.addSeparator()
        delete_action = menu.addAction('删除')
        action = menu.exec(self.trw_steps.viewport().mapToGlobal(pos))
        if action == edit_action:
            self.on_edit_click()
        elif action == run_to_action:
            QMessageBox.information(self, "操作", "运行到此步骤")
        elif action == run_this_action:
            QMessageBox.information(self, "操作", "运行此步骤")
        elif action == run_from_action:
            QMessageBox.information(self, "操作", "此步骤开始运行")
        elif action == delete_action:
            items = self.trw_steps.selectedItems()
            if items:
                msg_code = QMessageBox.question(self, "删除确认",
                                                "是否删除步骤【"+items[0].text(0)+"】及其子步骤",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if msg_code == QMessageBox.StandardButton.Yes:
                    self.remove_item(items[0], 0)

    def on_edit_click(self):
        items = self.trw_steps.selectedItems()
        if items:
            self.open_editor(items[0])
        else:
            QMessageBox.critical(self, "请选择", "请先选择一行")

    def get_action_by_code(self, code):
        for act in self.actions:
            if act['actionCode'] == code:
                return act

    def on_save_click(self):
        if self.trw_steps.changed:
            steps = self.fetch_steps()
            for i in range(len(steps)):
                steps[i]['number'] = i + 1
            flow_code = self.cmb_flow.currentData()["flowCode"]
            self.storage.upset_flow(flow_code, steps)
            QMessageBox.information(self, "结果", '操作成功')
            self.load_step_data()

    def on_run_click(self):
        app = self.cmb_app.currentData()
        flow = self.cmb_flow.currentData()
        task = self.cmb_task.currentData()

        app_args = json.loads(app['appArgs'])

        flow_args = {"appCode": app['appCode'],
                    "flowCode": flow['flowCode'],
                    "flowName": flow['flowName'],
                    "declareSystem": flow['declareSystem'],
                    "addrName": app_args['addrName'],
                    "addrId": app_args['addrId'],
                    "businessType": app_args['businessType'],
                    "taskCode": task["taskCode"],
                    "taskStatus": task['status'],
                    "clientId": task['clientId'],
                    "machineCode": task['machineCode']
                    }
        chrome_args = {
            "driverPath": os.path.abspath(".") + "\\robot\\chrome\\driver\\chromedriver.exe".replace('\r', '\\r'),
            "pluginPath": os.path.abspath(".") + "\\robot\\chrome\\plugin\\chrome".replace('\r', '\\r'),
            "sourcePath": os.path.abspath(".") + "\\robot\\chrome\\source\\chrome.exe".replace('\r', '\\r')
        }
        args_count = self.tbl_args.rowCount()
        for i in range(args_count):
            flow_args.update({self.tbl_args.item(i, 0).text(): self.tbl_args.item(i, 1).text()})

        flow_steps = self.fetch_steps()

        res = self.service.debug_flow_step(flow_steps, flow_args, chrome_args)
        if res['code'] == 200:
            QMessageBox.information(self, "结果", '启动成功')
        else:
            QMessageBox.information(self, "失败", res['message'])

    def on_sync_click(self):
        msg_code = QMessageBox.question(self, "同步确认框", "同步将覆盖服务器流程，是否继续",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if msg_code == QMessageBox.StandardButton.Yes:
            flow_code = self.cmb_flow.currentData()["flowCode"]
            res = self.service.sync_flow_steps(flow_code)
            if res:
                self.load_step_data()
            QMessageBox.information(self, "结果", '同步成功' if res else '同步失败')
