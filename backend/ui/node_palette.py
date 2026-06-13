from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QLabel
from PySide6.QtCore import Qt, QMimeData, QByteArray
from PySide6.QtGui import QDrag

class NodeListWidget(QListWidget):
    def startDrag(self, supportedActions):
        item = self.currentItem()
        if not item:
            return
            
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(item.text())
        drag.setMimeData(mime_data)
        drag.exec(supportedActions)

class NodePaletteWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        self.title = QLabel("Nodes")
        self.title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        self.layout.addWidget(self.title)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search nodes...")
        self.search_bar.setStyleSheet("background-color: #2b2b2b; color: white; border: 1px solid #444; border-radius: 4px; padding: 5px;")
        self.search_bar.textChanged.connect(self.filter_nodes)
        self.layout.addWidget(self.search_bar)

        self.list_widget = NodeListWidget()
        self.list_widget.setStyleSheet("background-color: #1e1e1e; border: none; outline: none; color: #d4d4d4;")
        self.list_widget.setDragEnabled(True)
        self.list_widget.viewport().setAcceptDrops(False)
        self.list_widget.setDropIndicatorShown(False)
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.list_widget.setSpacing(4)
        
        self.layout.addWidget(self.list_widget)
        
        self._populate_nodes()

    def _populate_nodes(self):
        nodes = [
            # Triggers
            "Trigger: Webhook",
            "Trigger: Schedule",
            "Trigger: Email Received",
            "Trigger: Slack Message",
            "Trigger: File Uploaded",
            "Trigger: Database Row Added",
            "Trigger: API Rate Limit Drop",
            "Trigger: Server Metric Alert",
            "Trigger: Discord Mention",
            "Trigger: Twitter/X Mention",
            "Trigger: GitHub Push",
            "Trigger: GitHub PR Created",
            
            # Data & Logic
            "Logic: If/Else",
            "Logic: Loop",
            "Logic: Switch",
            "Logic: Filter",
            "Logic: Map",
            "Logic: Merge",
            "Logic: Delay / Wait",
            "Data: Parse JSON",
            "Data: Parse CSV",
            "Data: Format Date",
            "Data: Regex Match",
            
            # AI & ML
            "AI: Gemini Generate",
            "AI: Vision Analyze",
            "AI: OpenAI ChatGPT",
            "AI: Claude Anthropic",
            "AI: Local LLM (Ollama)",
            "AI: Text to Speech",
            "AI: Speech to Text",
            "AI: Image Generation (Stable Diffusion)",
            "AI: Sentiment Analysis",
            "AI: Document Extraction (OCR)",
            "AI: Translate Text",
            
            # Actions: System & Dev
            "Action: HTTP Request",
            "Action: Execute Python Code",
            "Action: Execute Bash Command",
            "Action: Execute PowerShell",
            "Action: Read File",
            "Action: Write File",
            "Action: Query PostgreSQL",
            "Action: Query MongoDB",
            "Action: Query Redis",
            "Action: GraphQL Request",
            
            # Actions: Integrations
            "Action: Send Email",
            "Action: Send SMS (Twilio)",
            "Action: Post to Slack",
            "Action: Discord Webhook",
            "Action: Create Jira Ticket",
            "Action: Update Notion Page",
            "Action: Create Trello Card",
            "Action: Charge Stripe Customer",
            "Action: Create Google Calendar Event",
            "Action: Upload to S3 Bucket",
            
            # Actions: Media
            "Action: Resize Image",
            "Action: Convert to PDF",
            "Action: Crop Video",
            "Action: Extract Audio",
            
            # AI Agents (ReAct Loop)
            "Agent: Create Persona",
            "Agent: Chat Memory",
            "Agent: Attach Tool",
            "Agent: Summarize Thread",
            
            # Additional Office Utilities
            "Office: Generate Word Document",
            "Office: Read Excel (xlsx)",
            "Office: Write Excel (xlsx)",
            "Office: Extract PDF Text",
            "Office: Send Microsoft Teams Message",
            "Office: Read Outlook Email",
            
            # Data Formatting & Crypto
            "Data: Encode Base64",
            "Data: Decode Base64",
            "Data: Generate UUID",
            "Data: Hash (SHA-256)",
            "Data: HMAC Signature",
            
            # Security & DevSecOps
            "Security: Veracode SAST Scan",
            "Security: Veracode Get Flaws",
            "Security: CrowdStrike Falcon Alert",
            "Security: CrowdStrike Contain Host",
            
            # Advanced Control Flow
            "Logic: Try/Catch",
            "Logic: Fork/Join",
            "Logic: Throttle/Rate Limit",
            "Logic: Set Variable",
            "Logic: Get Variable"
        ]
        for node_name in nodes:
            item = QListWidgetItem(node_name)
            item.setBackground(Qt.transparent)
            # Add some padding visually
            item.setSizeHint(item.sizeHint().expandedTo(item.sizeHint() * 1.5))
            self.list_widget.addItem(item)

    def filter_nodes(self, text):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def filter_nodes(self, text):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(text.lower() not in item.text().lower())
