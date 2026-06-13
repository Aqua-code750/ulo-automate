import sys
import os
from dotenv import load_dotenv

# Load environment before anything else
load_dotenv()

from PySide6.QtWidgets import QApplication
from ui.main_window import UloMainWindow
from database import engine, Base

def main():
    # Initialize the database
    Base.metadata.create_all(bind=engine)
    
    # Start the PySide6 Native GUI
    app = QApplication(sys.argv)
    window = UloMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
