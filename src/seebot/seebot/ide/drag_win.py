from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QTreeWidget, QFormLayout, QComboBox, QCheckBox, QLineEdit, QMessageBox
from PySide6.QtCore import Qt, QByteArray, QRect, QObject, QEvent
from PySide6.QtGui import QDrag, QColor,QKeySequence
import sys
from seebot.ide.drag import Ui_frm_drag
import json
import copy

role = Qt.ItemDataRole.UserRole


class DragWin(QMainWindow, Ui_frm_drag):
    def __init__(self, parent=None):
        super(DragWin, self).__init__(parent)
        self.setupUi(self)

        self.treeWidget1.setDragEnabled(True)
        self.treeWidget1.setAcceptDrops(False)
        self.treeWidget1.setDragDropMode(QTreeWidget.DragDropMode.DragOnly)
        self.treeWidget2.setAcceptDrops(True)
        self.treeWidget2.setDragEnabled(True)
        # self.treeWidget2.setDefaultDropAction(True)
        self.treeWidget2.setDragDropMode(QTreeWidget.DragDropMode.DragDrop)
        # self.treeWidget2.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)

        group_items = []
        for i in range(3):
            name = 'treeWidget1_stepName' + str(i)
            top = QTreeWidgetItem()
            top.setText(0, name)
            top.setFirstColumnSpanned(True)
            group_items.append(top)
            child1 = QTreeWidgetItem()
            child1.setText(0, name + '_child1')
            top.addChild(child1)
            child2 = QTreeWidgetItem()
            child2.setText(0, name + '_child2')
            top.addChild(child2)
            child3 = QTreeWidgetItem()
            child3.setText(0, name + '_child3')
            top.addChild(child3)
        self.treeWidget1.addTopLevelItems(group_items)
        self.treeWidget1.expandAll()

        group_items = []
        for i in range(3):
            name = 'treeWidget2_stepName' + str(i)
            top = QTreeWidgetItem()
            top.setText(0, name)
            top.setData(0, role, 1)
            top.setFirstColumnSpanned(True)
            group_items.append(top)
            child1 = QTreeWidgetItem()
            child1.setText(0, name + '_child1')
            child1.setData(0, role, 1)
            top.addChild(child1)
            child2 = QTreeWidgetItem()
            child2.setText(0, name + '_child2')
            child2.setData(0, role, 1)
            top.addChild(child2)
            child3 = QTreeWidgetItem()
            child3.setText(0, name + '_child3')
            child3.setData(0, role, 1)
            top.addChild(child3)
        self.treeWidget2.addTopLevelItems(group_items)
        self.treeWidget2.expandAll()

        # self.treeWidget1.itemPressed.connect(self.start_drag)
        # self.treeWidget2.itemPressed.connect(self.item_dropped)
        # self.treeWidget2.dragEnterEvent = self.dragEnterEvent
        self.treeWidget2.itemChanged.connect(self.item_changed)

    def item_changed(self, item, column):
        items = self.treeWidget2.selectedItems()
        if items is not None and len(items) > 0:
            selected_item = items[0]
            if selected_item.data(0, role) > 0:
                child_count = selected_item.childCount()
                for i in range(child_count):
                    new_child = QTreeWidgetItem()
                    new_child.setText(0, selected_item.child(i).text(0))
                    new_child.setData(0, role, selected_item.child(i).data(0, role))
                    item.addChild(new_child)
                self.treeWidget2.expandItem(item)
                self.remove_item(selected_item, column)
        item.setData(0, role, 1)

    def remove_item(self, item, column):
        if item.parent() is None:  # Check if it is a top-level item
            self.treeWidget2.takeTopLevelItem(self.treeWidget2.indexOfTopLevelItem(item))
            print(f"Removed top-level item: {item.text(column)}")
        else:
            parent = item.parent()
            parent.removeChild(item)
            print(f"Removed child item: {item.text(column)}")
        self.treeWidget2.setCurrentItem(None)
    #
    # def dragEnterEvent(self, event):
    #     print(event)
    #     event.acceptProposedAction()

    # def dragEnterEvent(self, event):
    #     if event.mimeData().hasFormat('text/plain'):
    #         event.accept()
    #     else:
    #         event.ignore()
    #
    # def dragMoveEvent(self, event):
    #     if event.mimeData().hasFormat('text/plain'):
    #         event.setDropAction(Qt.MoveAction)
    #         event.accept()
    #     else:
    #         event.ignore()
    #
    # def dropEvent(self, event):
    #     if event.mimeData().hasFormat('text/plain'):
    #         data = event.mimeData().data('text/plain')
    #         item_text = data.decode()
    #         new_item = QTreeWidgetItem(
    #             self.treeWidget2.currentItem().parent() if self.treeWidget2.currentItem() else self.treeWidget2)
    #         new_item.setText(0, item_text)
    #         event.accept()
    #     else:
    #         event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = DragWin()
    win.show()
    sys.exit(app.exec())
