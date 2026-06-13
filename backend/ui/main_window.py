from PySide6.QtWidgets import QMainWindow, QSplitter, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from .node_canvas import NodeCanvasWidget
from .node_palette import NodePaletteWidget
from .properties_panel import PropertiesPanelWidget

class UloMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ULO AUTOMATE")
        self.resize(1200, 800)

        # Global n8n-style Dark Theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QPushButton {
                background-color: #f25b22;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff6d55;
            }
            QLineEdit {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 5px;
            }
        """)

        # Splitter Layout
        self.splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.splitter)

        self.palette_widget = NodePaletteWidget()
        self.builder_tab = NodeCanvasWidget()
        self.properties_widget = PropertiesPanelWidget()

        self.splitter.addWidget(self.palette_widget)
        self.splitter.addWidget(self.builder_tab)
        self.splitter.addWidget(self.properties_widget)

        # Set initial sizes (Sidebar 250px, Canvas 600px, Properties 350px)
        self.splitter.setSizes([250, 600, 350])
        
        # Connect signals
        self.builder_tab.node_selected.connect(self.properties_widget.set_node)
        self.builder_tab.execution_finished.connect(self.properties_widget.set_execution_results)

