import sys
from PyQt6.QtWidgets import QApplication

from backend.backend import initialize, deinitialize
from frontend.frontend import MainWindow

def main():
    initialize()
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: #1e1e2f;
            color: #f0f0f0;
            font-family: 'Segoe UI', Arial;
            font-size: 14px;
        }

        QLabel {
            font-size: 16px;
            padding: 8px;
        }

        QTextEdit {
            background-color: #2b2b3c;
            color: #f0f0f0;
            border: 1px solid #3b3b4f;
            border-radius: 8px;
            padding: 6px;
        }

        QPushButton {
            background-color: #4f46e5;
            color: white;
            border: none;
            padding: 10px 18px;
            border-radius: 8px;
            font-weight: 600;
        }

        QPushButton:hover {
            background-color: #6366f1;
        }

        QPushButton:pressed {
            background-color: #4338ca;
        }
    """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    deinitialize()

if __name__ == "__main__":
    main()
