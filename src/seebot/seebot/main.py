import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QCoreApplication

from seebot.ide.index_win import IndexWin


if __name__ == '__main__':
    # QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = IndexWin()
    win.show()
    sys.exit(app.exec())

