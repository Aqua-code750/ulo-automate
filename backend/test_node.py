from PySide6.QtWidgets import QApplication
import sys
app = QApplication(sys.argv)
from NodeGraphQt import NodeGraph, BaseNode

class BaseTaskNode(BaseNode):
    __identifier__ = 'ulo.nodes'
    NODE_NAME = 'Task Node'

graph = NodeGraph()
graph.register_node(BaseTaskNode)
print(graph.registered_nodes())
