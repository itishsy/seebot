import sys
from PySide6.QtWidgets import QApplication

from seebot.ide.index_win import IndexWin


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = IndexWin()
    win.show()
    sys.exit(app.exec())

