from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt6.QtCore import Qt

class UploadPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def start_interview(self):
        pass
