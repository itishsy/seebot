import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsTextItem
import pygraphviz as pgv

class FlowchartWidget(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.G = pgv.AGraph(strict=False, directed=True)

        self.nodes = {}
        self.edges = []

        self.dragging = False
        self.drag_item = None

    def add_node(self, label, shape='box', x=0, y=0):
        node_id = f"node_{len(self.nodes)}"
        self.nodes[node_id] = label
        self.G.add_node(node_id, label=label, shape=shape)
        item = QGraphicsTextItem(label)
        item.setPos(x, y)
        self.scene.addItem(item)

    def add_edge(self, start_node, end_node, label=''):
        edge_id = f"edge_{len(self.edges)}"
        self.edges.append(edge_id)
        self.G.add_edge(start_node, end_node, label=label)

    def mousePressEvent(self, event):
        items = self.items(event.pos())
        for item in items:
            if isinstance(item, QGraphicsTextItem):
                self.dragging = True
                self.drag_item = item

    def mouseMoveEvent(self, event):
        if self.dragging and self.drag_item:
            pos = event.pos()
            self.drag_item.setPos(pos)

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.drag_item = None

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QMainWindow()
    flowchart_widget = FlowchartWidget()
    window.setCentralWidget(flowchart_widget)

    flowchart_widget.add_node("Start", shape='ellipse', x=50, y=50)
    flowchart_widget.add_node("Step 1", shape='box', x=200, y=50)
    flowchart_widget.add_node("Step 2", shape='box', x=350, y=50)
    flowchart_widget.add_node("End", shape='ellipse', x=500, y=50)

    flowchart_widget.add_edge("Start", "Step 1", label='Start to Step 1')
    flowchart_widget.add_edge("Step 1", "Step 2", label='Step 1 to Step 2')
    flowchart_widget.add_edge("Step 2", "End", label='Step 2 to End')

    window.show()

    sys.exit(app.exec())
