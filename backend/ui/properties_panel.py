from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                               QTextEdit, QScrollArea, QFormLayout, QComboBox, 
                               QCheckBox, QPushButton, QTabWidget)
from PySide6.QtCore import Qt
import json

class PropertiesPanelWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        self.title = QLabel("Properties")
        self.title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff; padding-bottom: 10px;")
        self.layout.addWidget(self.title)

        # Main Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #444;
                border-radius: 4px;
                background: #1e1e1e;
            }
            QTabBar::tab {
                background: #2b2b2b;
                color: #888;
                border: 1px solid #444;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #1e1e1e;
                color: #ffffff;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected {
                background: #3a3a3a;
                color: #ddd;
            }
        """)
        self.layout.addWidget(self.tabs)

        # Tab 1: Configuration (Scroll Area)
        self.config_tab = QWidget()
        self.config_layout = QVBoxLayout(self.config_tab)
        self.config_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.content_widget = QWidget()
        self.form_layout = QFormLayout(self.content_widget)
        self.form_layout.setContentsMargins(10, 10, 10, 10)
        self.form_layout.setLabelAlignment(Qt.AlignLeft)
        self.form_layout.setVerticalSpacing(12)
        
        # Premium input styles
        self.input_style = """
            QLineEdit, QTextEdit, QComboBox {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Segoe UI', Inter, sans-serif;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 1px solid #7289da;
                background-color: #333333;
            }
            QLabel { 
                color: #d4d4d4; 
                font-weight: 600; 
                font-family: 'Segoe UI', Inter, sans-serif;
            }
            QCheckBox {
                color: #d4d4d4;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
                border: 1px solid #444;
                background: #2b2b2b;
            }
            QCheckBox::indicator:checked {
                background: #7289da;
                border: 1px solid #7289da;
            }
        """
        self.content_widget.setStyleSheet(self.input_style)
        self.scroll.setWidget(self.content_widget)
        self.config_layout.addWidget(self.scroll)
        
        # Tab 2: Output Viewer
        self.output_tab = QWidget()
        self.output_layout = QVBoxLayout(self.output_tab)
        self.output_layout.setContentsMargins(10, 10, 10, 10)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: #121212;
                color: #a6e22e;
                font-family: Consolas, monospace;
                border: 1px solid #333;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        self.output_text.setText("{ // Execute workflow to see output\n}")
        self.output_layout.addWidget(self.output_text)
        
        self.tabs.addTab(self.config_tab, "Config")
        self.tabs.addTab(self.output_tab, "Output")
        
        self.current_node = None
        self.inputs = {}
        self.payload = {}
        
        # Placeholder
        self._add_placeholder()

    def set_execution_results(self, payload):
        self.payload = payload
        self._refresh_output()

    def _add_placeholder(self):
        lbl = QLabel("Select a node on the canvas to configure it.")
        lbl.setStyleSheet("color: #888; font-style: italic;")
        self.form_layout.addRow(lbl)

    def set_node(self, node):
        self.current_node = node
        # Clear form
        while self.form_layout.count():
            child = self.form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.inputs.clear()
        
        if not node:
            self._add_placeholder()
            return
            
        task_type = node.get_property('task_desc')
        self.title.setText(f"{task_type}")
        
        # Build dynamic form based on node type
        self._build_form(task_type)
        
        # Save button
        save_btn = QPushButton("Save Properties")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #7289da; 
                color: white; 
                border: none; 
                padding: 10px; 
                border-radius: 6px; 
                font-weight: bold; 
                margin-top: 15px;
            }
            QPushButton:hover { background-color: #5b6eae; }
        """)
        save_btn.clicked.connect(self.save_properties)
        self.form_layout.addRow(save_btn)
        
        self._refresh_output()

    def _refresh_output(self):
        if not self.current_node:
            self.output_text.setText("{ // No node selected\n}")
            return
            
        node_id = self.current_node.id
        node_key = f"node_{node_id}"
        
        if node_key in self.payload:
            node_result = self.payload[node_key]
            self.output_text.setText(json.dumps(node_result, indent=2))
            self.tabs.setCurrentIndex(1) # Switch to output tab
        else:
            self.output_text.setText("{ // No execution data for this node yet.\n  // Click 'Execute Workflow' to run.\n}")

    def _build_form(self, task_type):
        # We fetch existing custom properties from the node if they exist
        custom_props = {}
        if hasattr(self.current_node, 'custom_props'):
            custom_props = self.current_node.custom_props
            
        def add_field(key, label, widget_type="text", placeholder=""):
            val = custom_props.get(key, "")
            lbl = QLabel(label)
            if widget_type == "text":
                widget = QLineEdit(str(val))
                widget.setPlaceholderText(placeholder)
            elif widget_type == "textarea":
                widget = QTextEdit()
                widget.setPlainText(str(val))
                widget.setPlaceholderText(placeholder)
                widget.setMaximumHeight(100)
            elif widget_type == "bool":
                widget = QCheckBox()
                widget.setChecked(bool(val))
            
            self.inputs[key] = widget
            self.form_layout.addRow(lbl, widget)
            
        # Global fields
        add_field("node_name", "Node Name", "text", "e.g., Step 1")

        # Specific fields
        if "Slack" in task_type:
            add_field("webhook_url", "Slack Webhook URL", "text", "https://hooks.slack.com/...")
            add_field("channel", "Channel", "text", "#general")
            add_field("message", "Message Payload", "textarea", "Hello world!")
            add_field("username", "Bot Username", "text", "UloBot")
        elif "HTTP" in task_type:
            add_field("method", "HTTP Method", "text", "GET, POST, PUT...")
            add_field("url", "URL", "text", "https://api.example.com")
            add_field("headers", "Headers (JSON)", "textarea", '{"Authorization": "Bearer..."}')
            add_field("body", "Body Payload", "textarea", "...")
        elif "Python" in task_type:
            add_field("code", "Python Code", "textarea", "print('hello')\\nresult = {'status': 'ok'}")
        elif "Bash" in task_type:
            add_field("command", "Bash Command", "text", "ls -la")
        elif "AI" in task_type or "Gemini" in task_type or "OpenAI" in task_type or "Agent" in task_type:
            add_field("api_key", "API Key (optional if in .env)", "text", "sk-...")
            add_field("prompt", "Prompt / Instructions", "textarea", "Analyze this text...")
            add_field("model", "Model Override", "text", "gpt-4 or gemini-1.5-flash")
            add_field("temperature", "Temperature", "text", "0.7")
        elif "Email" in task_type:
            add_field("to_email", "To", "text", "recipient@example.com")
            add_field("subject", "Subject", "text", "Subject")
            add_field("body", "Body", "textarea", "Message body")
        elif "Agent" in task_type:
            add_field("agent_role", "Agent Persona / Role", "textarea", "You are an expert Data Analyst...")
            add_field("model", "Model", "text", "gpt-4")
            add_field("api_key", "API Key (optional if in .env)", "text", "sk-...")
            add_field("max_iterations", "Max Iterations", "text", "5")
            add_field("tools", "Allowed Tools (comma separated)", "text", "python,http,slack")
        elif "Office" in task_type:
            if "Word" in task_type:
                add_field("file_path", "Output File Path", "text", "C:/data/report.docx")
                add_field("template_path", "Template Path (Optional)", "text", "C:/data/template.docx")
                add_field("input_data", "Input Data (JSON Object)", "textarea", '{"name": "Alice", "date": "2026-06-13"}')
            else:
                add_field("file_path", "File Path", "text", "C:/data/report.xlsx")
                add_field("sheet_name", "Sheet Name", "text", "Sheet1")
                if "Write" in task_type:
                    add_field("input_data", "Input Data (JSON 2D Array)", "textarea", '[[ "Name", "Age" ], [ "Alice", 30 ]]')
                else:
                    add_field("cell_range", "Cell Range", "text", "A1:D10")
        elif "Integration" in task_type:
            if "GitHub" in task_type:
                add_field("api_key", "GitHub PAT Token", "text", "ghp_...")
                add_field("repo", "Repository (owner/repo)", "text", "torvalds/linux")
                add_field("action", "Action (get_repo, create_issue)", "text", "create_issue")
                add_field("payload", "Issue Data (JSON)", "textarea", '{"title": "Bug found", "body": "Details..."}')
            elif "Jira" in task_type:
                add_field("email", "Jira Email", "text", "user@domain.com")
                add_field("api_key", "Jira API Token", "text", "...")
                add_field("domain", "Jira Domain", "text", "your-domain.atlassian.net")
                add_field("payload", "Ticket Data (JSON)", "textarea", '{"project": "PROJ", "summary": "Fix bug"}')
            elif "Stripe" in task_type:
                add_field("api_key", "Stripe Secret Key", "text", "sk_test_...")
                add_field("action", "Action (create_customer, create_charge)", "text", "create_customer")
                add_field("payload", "Data (JSON)", "textarea", '{"email": "jenny@example.com"}')
            elif "Discord" in task_type:
                add_field("webhook_url", "Discord Webhook URL", "text", "https://discord.com/api/webhooks/...")
                add_field("payload", "Message Data (JSON)", "textarea", '{"content": "Hello World!"}')
            elif "Notion" in task_type:
                add_field("api_key", "Notion Integration Token", "text", "secret_...")
                add_field("database_id", "Database ID", "text", "...")
                add_field("payload", "Page Properties (JSON)", "textarea", '{"Name": {"title": [{"text": {"content": "Tuscan Kale"}}]}}')
            elif "Trello" in task_type:
                add_field("api_key", "Trello API Key", "text", "...")
                add_field("token", "Trello Token", "text", "...")
                add_field("list_id", "List ID", "text", "...")
                add_field("payload", "Card Data (JSON)", "textarea", '{"name": "New Card"}')
            elif "Slack" in task_type:
                add_field("api_key", "Slack Bot Token", "text", "xoxb-...")
                add_field("channel", "Channel ID", "text", "C123456")
                add_field("message", "Message Text", "textarea", "Hello from Ulo!")
            elif "Mailchimp" in task_type:
                add_field("api_key", "Mailchimp API Key", "text", "...-usX")
                add_field("list_id", "Audience List ID", "text", "...")
                add_field("payload", "Subscriber Data (JSON)", "textarea", '{"email_address": "user@test.com", "status": "subscribed"}')
            elif "Zendesk" in task_type:
                add_field("domain", "Zendesk Subdomain", "text", "subdomain")
                add_field("email", "Agent Email", "text", "agent@domain.com")
                add_field("api_key", "Zendesk API Token", "text", "...")
                add_field("payload", "Ticket Data (JSON)", "textarea", '{"ticket": {"subject": "Help", "comment": { "body": "Details" }}}')
            elif "Shopify" in task_type:
                add_field("store", "Shopify Store Name", "text", "your-store")
                add_field("api_key", "Admin API Access Token", "text", "shpat_...")
                add_field("action", "Action (get_products, get_orders)", "text", "get_products")
        elif "Security" in task_type or "Veracode" in task_type or "Falcon" in task_type:
            add_field("api_id", "API ID / Client ID", "text", "vera_id_...")
            add_field("api_key", "API Key / Secret", "text", "vera_key_...")
            if "Veracode" in task_type:
                add_field("app_name", "Application Name", "text", "my-secure-app")
            if "Falcon" in task_type:
                add_field("host_id", "Target Host ID", "text", "aid_12345")
        elif "JSON" in task_type or "CSV" in task_type or "Data" in task_type:
            add_field("input_data", "Input Data", "text", "{{ payload['node_X']['result'] }}")
        elif "Logic" in task_type:
            add_field("variable_name", "Variable Name", "text", "my_var")
            add_field("condition", "Condition expression", "text", "payload['count'] > 10")
        else:
            add_field("description", "Description", "textarea", "Generic node description")

    def save_properties(self):
        if not self.current_node: return
        props = {}
        for key, widget in self.inputs.items():
            if isinstance(widget, QLineEdit):
                props[key] = widget.text()
            elif isinstance(widget, QTextEdit):
                props[key] = widget.toPlainText()
            elif isinstance(widget, QCheckBox):
                props[key] = widget.isChecked()
                
        self.current_node.custom_props = props
        print(f"Saved properties for {self.current_node.id}: {props}")
