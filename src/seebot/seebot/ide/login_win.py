from PySide6.QtWidgets import QMainWindow, QMessageBox
import urllib.parse as urlparse
import json

from seebot.ide.login import Ui_frm_index
from seebot.ide.service import Service
from seebot.ide.storage import Storage
import seebot.utils.aes as aes
from seebot.utils.http import httpUtil


class LoginWin(QMainWindow, Ui_frm_index):
    def __init__(self, parent=None):
        super(LoginWin, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.btn_login.clicked.connect(self.on_login_click)
        self.storage = Storage()

    def show(self) -> None:
        super(LoginWin, self).show()
        res = self.storage.find_value('remember_me')
        if len(res) != 0:
            res = res.split('`')
        if len(res) == 3:
            self.ckb_remember.setChecked(True)
            self.cmb_server.setCurrentText(res[0])
            self.inp_username.setText(res[1])

    def on_login_click(self):
        server = self.cmb_server.currentText()
        username = self.inp_username.text()
        password = self.inp_password.text()
        if username == '' or password == '':
            QMessageBox.information(self, "提示", "请输入用户名和密码")
        else:
            pwd = urlparse.quote(aes.encrypt(password), 'utf-8')
            url = server + "/api/oauth/token?client_id=rpa&client_secret=123&grant_type=password&username=" + username + "&password=" + pwd
            res = httpUtil.post(url=url)
            data = json.loads(res.content)
            if data.get("access_token") is not None:
                token = "bearer " + data.get("access_token")
                val = server + '`' + username + '`' + token if self.ckb_session.isChecked() else ''
                self.storage.upset_key_value('session', val)
                self.close()
                self.pre_win.service = Service(server, token)
                self.pre_win.show()
            else:
                QMessageBox.critical(self, "失败", res)
