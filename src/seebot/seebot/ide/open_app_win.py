from PySide6.QtWidgets import QMainWindow, QMessageBox

from seebot.ide.open_app import Ui_frm_open
import seebot.ide.flow_config_win as config
from seebot.ide.service import Api

import seebot.utils.sqlite as db


class OpenAppWin(QMainWindow, Ui_frm_open):
    def __init__(self, parent=None):
        super(OpenAppWin, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.load_data()
        self.btn_open.clicked.connect(self.on_open_click)
        self.cmb_app.currentTextChanged.connect(self.on_app_change)

    def load_data(self):
        api = Api()
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
                self.ckb_remember.setChecked(True)
                self.cmb_app.setCurrentText(sta[0])
                self.on_app_change()
                self.cmb_flow.setCurrentText(sta[1])
                self.cmb_task.setCurrentText(sta[2])
        self.actions = api.find_action()["data"]

    def on_open_click(self):
        self.win = config.FlowConfigWin()
        self.win.pre_win = self
        self.hide()
        self.win.app_name = self.cmb_app.currentText()
        self.win.app_code = self.cmb_app.currentData()
        self.win.flow_name = self.cmb_flow.currentText()
        self.win.flow_code = self.cmb_flow.currentData()
        self.win.task_code = self.cmb_task.currentData()
        self.win.data_mode = 'server'
        if self.win.flow_name == '==请选择==':
            QMessageBox.information(self, "提示", "请选择流程")
        else:
            db.execute("delete from setting where key='remember_app'")
            if self.ckb_remember.isChecked():
                val = self.win.app_name + '`' + self.win.flow_name + '`' + self.cmb_task.currentText()
                db.execute("insert into setting(key, value) values('remember_app','" + val + "')")
            self.win.actions = self.actions
        self.win.show()

    def on_app_change(self):
        app_code = self.cmb_app.currentData()
        api = Api()
        self.cmb_flow.clear()
        self.cmb_flow.addItem("==请选择==")
        self.cmb_task.clear()
        self.cmb_task.addItem("==请选择==")
        if app_code is not None:
            data = api.find_flow(app_code)
            for item in data["data"]:
                self.cmb_flow.addItem(item['flowName'], item['flowCode'])

            data = api.find_task(app_code)
            for item in data["data"]:
                if item['companyName'] is not None and item['accountNumber'] is not None:
                    text = item['companyName']+'('+item['accountNumber']+')'
                    self.cmb_task.addItem(text, item['taskCode'])