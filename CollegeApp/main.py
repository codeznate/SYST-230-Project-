"""
-> Main program to run everything together.
"""

from PySide6.QtWidgets import QApplication
from app_window import MajorApp
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MajorApp()
    window.show()
    sys.exit(app.exec())