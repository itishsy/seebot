import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene,QGraphicsItem, QGraphicsRectItem
from PySide6.QtCore import Qt


class DraggableRectItem(QGraphicsRectItem):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.setBrush(Qt.lightGray)
        self.setFlag(QGraphicsItem.ItemIsMovable)


class DragDropExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drag and Drop Example")
        self.setGeometry(100, 100, 600, 400)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        rect1 = DraggableRectItem(50, 50, 100, 50)
        rect2 = DraggableRectItem(200, 200, 150, 100)

        self.scene.addItem(rect1)
        self.scene.addItem(rect2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DragDropExample()
    window.show()
    sys.exit(app.exec())
