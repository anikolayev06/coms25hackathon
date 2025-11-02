import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

from backend.backend import initialize, deinitialize
from frontend.frontend import MainWindow


def main():
    initialize()
    app = QApplication(sys.argv)

    app.setFont(QFont("Segoe UI Variable", 10))

    app.setStyleSheet("""
        QWidget {
            background-color: interlinear(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #0a0e27,
                stop:1 #10142f
            );
            color: #e2e8f0;
            font-family: 'Segue UI Variable', 'Roboto', 'Inter', Arial;
            font-size: 15px;
        }

        QMainWindow {
            border: none;
        }

        QLabel {
            font-size: 16px;
            padding: 6px;
            color: #f8faff;
        }

        QLabel#title {
            font-size: 36px;
            font-weight: 800;
            letter-spacing: 1px;
            color: #ffffff;
        }

        QLabel#subtitle {
            font-size: 14px;
            color: #a5b4fc;
        }

        QTextEdit {
            background-color: rgba(17, 24, 39, 0.9);
            color: #f1f5f9;
            border: 2px solid rgba(99, 102, 241, 0.3);
            border-radius: 14px;
            padding: 14px;
            font-size: 15px;
            selection-background-color: #6366f1;
            transition: all 0.2s ease-in-out;
        }

        QTextEdit:focus {
            border: 2px solid #818cf8;
            background-color: rgba(17, 24, 39, 1);
            box-shadow: 0 0 12px rgba(99, 102, 241, 0.4);
        }

        QPushButton {
            background-color: #6366f1;
            color: #ffffff;
            border: none;
            padding: 12px 28px;
            border-radius: 14px;
            font-weight: 600;
            font-size: 15px;
            transition: all 0.2s ease-in-out;
            min-width: 140px;
        }

        QPushButton:hover {
            background-color: #818cf8;
            transform: scale(1.03);
        }

        QPushButton:pressed {
            background-color: #4f46e5;
            transform: scale(0.98);
        }

        QPushButton:disabled {
            background-color: #475569;
            color: #94a3b8;
        }

        QScrollBar:vertical {
            background: #1e293b;
            width: 12px;
            border-radius: 6px;
        }

        QScrollBar::handle:vertical {
            background: #6366f1;
            border-radius: 6px;
        }

        QScrollBar::handle:vertical:hover {
            background: #818cf8;
        }

        QFrame {
            background-color: rgba(30, 41, 59, 0.8);
            border-radius: 20px;
            border: 1px solid rgba(148, 163, 184, 0.15);
        }

        QToolTip {
            background-color: #1e293b;
            color: #e2e8f0;
            border: 1px solid #475569;
            padding: 6px;
            border-radius: 8px;
        }
    """)

    window = MainWindow()
    window.setStyleSheet("""
        QMainWindow {
            background-color: transparent;
        }
    """)
    window.showMaximized()

    sys.exit(app.exec())
    deinitialize()


if __name__ == "__main__":
    main()
