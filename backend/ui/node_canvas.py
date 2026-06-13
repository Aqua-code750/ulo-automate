from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit
from PySide6.QtCore import Signal
from NodeGraphQt import NodeGraph, BaseNode

class BaseTaskNode(BaseNode):
    __identifier__ = 'ulo.nodes'
    NODE_NAME = 'Task Node'

    def __init__(self):
        super(BaseTaskNode, self).__init__()
        self.add_input('in', color=(180, 80, 180))
        self.add_output('out', color=(180, 80, 180))
        self.add_text_input('task_desc', 'Task', tab='Properties')

class NodeCanvasWidget(QWidget):
    node_selected = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        self.toolbar = QHBoxLayout()
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Describe automation...")
        self.generate_btn = QPushButton("Generate")
        self.voice_btn = QPushButton("🎤 Voice")
        self.optimize_btn = QPushButton("✨ Optimize")
        
        self.toolbar.addWidget(self.prompt_input)
        self.toolbar.addWidget(self.generate_btn)
        self.toolbar.addWidget(self.voice_btn)
        self.toolbar.addWidget(self.optimize_btn)
        
        # Add execution button to toolbar
        self.execute_btn = QPushButton("🚀 Execute Workflow")
        self.execute_btn.setStyleSheet("background-color: #40965a; font-weight: bold;")
        self.toolbar.addWidget(self.execute_btn)
        
        self.layout.addLayout(self.toolbar)

        # Node Graph
        self.graph = NodeGraph()
        self.graph.register_node(BaseTaskNode)
        
        # Apply n8n style graph colors
        self.graph.set_background_color(30, 30, 30)
        self.graph.set_grid_color(45, 45, 45)
        
        self.graph_widget = self.graph.widget
        self.layout.addWidget(self.graph_widget)
        
        # Connect to NodeGraphQt's native drop signal
        self.graph.data_dropped.connect(self._on_data_dropped)
        
        # Connect Signals
        self.generate_btn.clicked.connect(self.on_generate_clicked)
        self.voice_btn.clicked.connect(self.on_voice_clicked)
        self.execute_btn.clicked.connect(self.on_execute_clicked)
        
        # Node selection signal
        self.graph.node_selected.connect(self._on_node_selected)
        self.graph.node_selection_changed.connect(self._on_selection_changed)

    def _on_node_selected(self, node):
        self.node_selected.emit(node)
        
    def _on_selection_changed(self):
        selected_nodes = self.graph.selected_nodes()
        if not selected_nodes:
            self.node_selected.emit(None)
        elif len(selected_nodes) == 1:
            self.node_selected.emit(selected_nodes[0])

    def on_execute_clicked(self):
        import threading
        from executor import WorkflowExecutor
        
        # Reset colors before execution
        for node in self.graph.all_nodes():
            node.set_color(30, 30, 30)

        # Graph traversal extraction
        nodes_list = []
        edges_list = []
        for node in self.graph.all_nodes():
            custom_props = getattr(node, 'custom_props', {})
            nodes_list.append({
                "id": node.id,
                "type": node.get_property('task_desc'),
                "props": custom_props
            })
            # Capture connections from outputs
            for out_port in node.outputs().values():
                for connected_port in out_port.connected_ports():
                    edges_list.append({
                        "source": node.id,
                        "target": connected_port.node().id
                    })
            
        workflow_data = {"nodes": nodes_list, "edges": edges_list}

        def _on_success(node_id):
            node = self.graph.get_node_by_id(node_id)
            if node:
                node.set_color(40, 150, 90) # Green
                
        def _on_error(node_id, err):
            node = self.graph.get_node_by_id(node_id)
            if node:
                node.set_color(200, 50, 50) # Red
                node.set_property('task_desc', f"Error: {err}")

        executor = WorkflowExecutor(workflow_data, _on_success, _on_error)
        
        # Run in thread so UI doesn't freeze
        t = threading.Thread(target=executor.run)
        t.start()

    def _on_data_dropped(self, mime_data, pos):
        try:
            if mime_data.hasText():
                text = mime_data.text()
                
                # Create node at the drop position
                n = self.graph.create_node('ulo.nodes.BaseTaskNode', name=text, pos=[pos.x(), pos.y()])
                n.set_property('task_desc', text)
                n.set_color(30, 30, 30)
                n.set_text_color(255, 255, 255)
                
                if "Trigger" in text:
                    n.set_color(40, 150, 90)
                elif "AI" in text:
                    n.set_color(150, 60, 200)
                elif "Action" in text:
                    n.set_color(40, 100, 200)
        except Exception as e:
            with open('drop_error.txt', 'w') as f:
                f.write(str(e))

    def on_generate_clicked(self):
        prompt = self.prompt_input.text()
        if prompt:
            self.generate_from_prompt(prompt)
            
    def on_voice_clicked(self):
        from .voice_module import listen_in_background
        self.prompt_input.setText("Listening...")
        self.prompt_input.setEnabled(False)
        self.voice_btn.setEnabled(False)
        
        def _callback(text, error):
            self.prompt_input.setEnabled(True)
            self.voice_btn.setEnabled(True)
            if text:
                self.prompt_input.setText(text)
                self.generate_from_prompt(text)
            else:
                self.prompt_input.setText(f"Error: {error}")
                
        listen_in_background(_callback)

    def generate_from_prompt(self, prompt: str):
        import ai_generator
        # Call the AI logic natively (blocking the GUI temporarily for prototype, ideally use QThread)
        try:
            workflow_def = ai_generator.generate_workflow(prompt)
            self.add_generated_nodes(workflow_def)
        except Exception as e:
            print(f"Failed to generate: {e}")

    def add_generated_nodes(self, nodes_data):
        # Clear existing nodes except start
        self.graph.clear_session()
        start_node = self.graph.create_node('ulo.nodes.BaseTaskNode', name='Start Workflow', pos=[0, 0])
        start_node.set_property('task_desc', 'Initialize')

        prev_node = start_node
        x_offset = 200
        for i, step in enumerate(nodes_data.get('nodes', [])):
            n = self.graph.create_node('ulo.nodes.BaseTaskNode', name=f"Step {i+1}", pos=[x_offset, 0])
            n.set_property('task_desc', step.get('description', 'Unknown Task'))
            prev_node.set_output(0, n.input(0))
            prev_node = n
            x_offset += 200

