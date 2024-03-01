from PySide6.QtWidgets import QMainWindow, QMessageBox
import urllib.parse as urlparse

from seebot.ide.index import Ui_frm_index
from seebot.ide.open_app_win import OpenAppWin
from seebot.ide.api import Api

import seebot.utils.aes as aes
import seebot.utils.sqlite as db


class IndexWin(QMainWindow, Ui_frm_index):
    def __init__(self, parent=None):
        super(IndexWin, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.btn_login.clicked.connect(self.on_login_click)

    def show(self) -> None:
        super(IndexWin, self).show()
        res = db.query("select value from setting where key='remember_me'")
        if len(res) > 0:
            sta = res[0]['value'].split('`')
            if len(sta) == 3:
                self.ckb_remember.setChecked(True)
                self.cmb_server.setCurrentText(sta[0])
                self.inp_username.setText(sta[1])
                self.inp_password.setText(sta[2])

    def on_login_click(self):
        server = self.cmb_server.currentText()
        username = self.inp_username.text()
        password = self.inp_password.text()
        pwd = urlparse.quote(aes.encrypt(password), 'utf-8')
        api = Api()
        api.server(server)
        if username == '' or password == '':
            QMessageBox.information(self, "提示", "请输入用户名和密码")
        else:
            res = api.login(username, pwd)
            if res is True:
                db.execute("delete from setting where key='remember_me'")
                if self.ckb_remember.isChecked():
                    val = server + '`' + username + '`' + password
                    db.execute("insert into setting(key, value) values('remember_me','"+val+"')")
                self.win = OpenAppWin()
                self.win.show()
                self.close()
            else:
                QMessageBox.critical(self, "失败", res)
