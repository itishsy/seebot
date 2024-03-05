from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QCloseEvent

from seebot.ide.flow_running import Ui_frm_flow_running
import seebot.ide.flow_config_win as config


class FlowRunningWin(QMainWindow, Ui_frm_flow_running):
    def __init__(self, parent=None):
        super(FlowRunningWin, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())

    def closeEvent(self, event: QCloseEvent) -> None:
        self.close()
