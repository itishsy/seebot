from PySide6.QtWidgets import QMainWindow, QMessageBox
import urllib.parse as urlparse

from seebot.ide.index import Ui_frm_index
from seebot.ide.flow_config_win import FlowConfigWin
from seebot.ide.services import Services

import seebot.utils.aes as aes


class IndexWin(QMainWindow, Ui_frm_index):
    def __init__(self, parent=None):
        super(IndexWin, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.btn_login.clicked.connect(self.on_login_click)

    def show(self) -> None:
        super(IndexWin, self).show()
        self.service = Services()
        res = self.service.find_setting('remember_me')
        if len(res) != 0:
            res = res.split('`')
        if len(res) == 3:
            self.ckb_remember.setChecked(True)
            self.cmb_server.setCurrentText(res[0])
            self.inp_username.setText(res[1])
            self.inp_password.setText(res[2])

    def on_login_click(self):
        server = self.cmb_server.currentText()
        username = self.inp_username.text()
        password = self.inp_password.text()
        pwd = urlparse.quote(aes.encrypt(password), 'utf-8')
        self.service.server(server)
        if username == '' or password == '':
            QMessageBox.information(self, "提示", "请输入用户名和密码")
        else:
            res = self.service.login(username, pwd)
            if res is True:
                val = server + '`' + username + '`' + password if self.ckb_remember.isChecked() else ''
                self.service.upset_setting('remember_me', val)
                self.close()
                self.win = FlowConfigWin()
                self.win.service = self.service
                self.win.show()
            else:
                QMessageBox.critical(self, "失败", res)
