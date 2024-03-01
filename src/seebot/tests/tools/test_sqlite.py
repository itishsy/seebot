from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel
from PySide6.QtWidgets import *

import sys

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.db = QSqlDatabase.database("QSQLITE")
        self.db.setDatabaseName("seebot.db")
        self.db.open()

        self.model = QSqlTableModel(self)
        self.model.setTable("flow_step")
        self.model.select()

        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())