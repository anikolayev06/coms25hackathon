import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

from backend.backend import initialize, deinitialize
from frontend.frontend import MainWindow

def main():
    initialize()
    app = QApplication(sys.argv)

    app.setFont(QFont("Segoe UI", 10))

    app.setStyleSheet("""
        QWidget {
            background-color: #0a0e27;
            color: #ffffff;
            font-family: 'Segoe UI', 'Roboto', Arial;
        }

        QLabel {
            font-size: 16px;
            padding: 8px;
        }

        QTextEdit {
            background-color: rgba(30, 41, 59, 0.8);
            color: #f1f5f9;
            border: 2px solid rgba(100, 116, 139, 0.3);
            border-radius: 12px;
            padding: 12px;
            selection-background-color: #6366f1;
        }

        QTextEdit:focus {
            border: 2px solid #6366f1;
            background-color: rgba(30, 41, 59, 1);
        }

        QPushButton {
            background-color: #6366f1;
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 15px;
            min-height: 24px;
        }

        QPushButton:hover {
            background-color: #818cf8;
        }

        QPushButton:pressed {
            background-color: #4f46e5;
        }

        QPushButton:disabled {
            background-color: #475569;
            color: #94a3b8;
        }
    """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    deinitialize()

if __name__ == "__main__":
    main()
