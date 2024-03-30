import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt


class TreeWidgetExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.treeWidget1 = QTreeWidget()
        self.treeWidget1.setDragEnabled(True)
        self.treeWidget1.setAcceptDrops(True)
        self.treeWidget1.setDragDropMode(QTreeWidget.DragDropMode.DragOnly)

        self.treeWidget2 = QTreeWidget()
        self.treeWidget2.setAcceptDrops(True)
        self.treeWidget2.setDragDropMode(QTreeWidget.DragDropMode.DropOnly)

        # 添加一些示例项到treeWidget1
        parent_item = QTreeWidgetItem()
        parent_item.setText(0, "Parent Item 1")
        child1 = QTreeWidgetItem()
        child1.setText(0, "Child 1")
        parent_item.addChild(child1)
        child2 = QTreeWidgetItem()
        child2.setText(0, "Child 2")
        parent_item.addChild(child2)
        self.treeWidget1.addTopLevelItem(parent_item)

        # 设置拖放目标的事件处理程序
        self.treeWidget2.setDropIndicatorShown(True)
        self.treeWidget2.viewport().installEventFilter(self)

        self.setCentralWidget(self.treeWidget1)
        self.setCentralWidget(self.treeWidget2)

    def eventFilter(self, obj, event):
        if event.type() == event.Type.Drop:
            item = QTreeWidgetItem(self.treeWidget2)
            item.setText(0, event.mimeData().text())
            event.accept()
            return True
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TreeWidgetExample()
    window.show()

    sys.exit(app.exec())
