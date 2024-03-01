from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QCloseEvent

from seebot.ide.flow_debug import Ui_frm_flow_debug
import seebot.ide.flow_config_win as config


class FlowDebugWin(QMainWindow, Ui_frm_flow_debug):
    def __init__(self, parent=None):
        super(FlowDebugWin, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())

    def closeEvent(self, event: QCloseEvent) -> None:
        self.close()
        self.pre_win.show()