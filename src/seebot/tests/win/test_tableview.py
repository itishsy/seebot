from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

import sys


class MyTableModel(QAbstractItemModel):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)

        self._data = [] if not data else data

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 3  # 列数为3（可根据需求修改）

    # def flags(self, index):
    #     return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            headers = ['Name', 'Age', 'Gender']  # 表头名称（可根据需求修改）
            return headers[section]

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            row = index.row()
            col = index.column()
            value = str(self._data[row][col])
            return value
        return None

    # def setData(self, index, value, role):
    #     if role == Qt.EditRole:
    #         row = index.row()
    #         col = index.column()
    #         self._data[row][col] = value
    #         self.dataChanged.emit(index, index)
    #         return True


# 创建主窗口类
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Table View Example")

        layout = QVBoxLayout()

        self.table_view = QTableView()
        self.model = MyTableModel(
            [['John Doe', '20', 'Male'], ['Jane Smith', '25', 'Female'], ['Tom Johnson', '30', 'Male']])
        self.table_view.setModel(self.model)

        button_layout = QHBoxLayout()
        add_button = QPushButton('Add Row')
        delete_button = QPushButton('Delete Selected Rows')

        button_layout.addStretch()
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)

        layout.addWidget(self.table_view)
        layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        add_button.clicked.connect(lambda: self.insertRow())
        delete_button.clicked.connect(lambda: self.removeSelectedRows())

    def insertRow(self):
        model = self.table_view.model()
        combo = QComboBox()
        combo.addItems(['Male', 'Female'])
        new_row = [QLineEdit(), QLineEdit(), combo]
        model.appendRow(new_row)

    def removeSelectedRows(self):
        selected_rows = self.table_view.selectedIndexes()
        if len(selected_rows) > 0:
            model = self.table_view.model()
            indexes = sorted(selected_rows, key=lambda x: x.row(), reverse=True)
            for index in indexes:
                model.removeRow(index.row())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())