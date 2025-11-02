from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit,
    QFileDialog, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
import os
from backend import backend
from pathlib import Path

class UploadPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.job_input = None
        self.parent = parent
        self.resume_path = None
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #0f172a; color: #e2e8f0; font-family: 'Segoe UI';")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setFixedWidth(600)
        card.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-radius: 20px;
                padding: 40px;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 10)
        shadow.setColor(QColor(0, 0, 0, 100))
        card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("PrepTalk")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Upload your resume and paste the job description below.")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #94a3b8;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        upload_btn = QPushButton("Upload Resume (PDF)")
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                border-radius: 10px;
                padding: 12px 20px;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #818cf8;
            }
        """)
        upload_btn.clicked.connect(self.select_pdf)

        self.resume_label = QLabel("No file selected")
        self.resume_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.resume_label.setStyleSheet("color: #94a3b8;")

        job_label = QLabel("Job Description")
        job_label.setFont(QFont("Segoe UI", 14))
        job_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.job_input = QTextEdit()
        self.job_input.setPlaceholderText("Paste the job description here")
        self.job_input.setStyleSheet("""
            QTextEdit {
                background-color: #0f172a;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 10px;
                color: #e2e8f0;
            }
        """)

        start_btn = QPushButton("Start Interview")
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                border-radius: 10px;
                padding: 12px 20px;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #16a34a;
            }
        """)
        start_btn.clicked.connect(self.start_interview)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(5)
        layout.addWidget(upload_btn)
        layout.addWidget(self.resume_label)
        layout.addWidget(job_label)
        layout.addWidget(self.job_input)
        layout.addSpacing(10)
        layout.addWidget(start_btn)

        main_layout.addWidget(card)

    def select_pdf(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("PDF files (*.pdf)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.resume_path = selected_files[0]
                filename = os.path.basename(self.resume_path)
                self.resume_label.setText(f"{filename} uploaded")
                print(f"Selected PDF path: {self.resume_path}")

    def start_interview(self):
        job_text = self.job_input.toPlainText()

        if not self.resume_path:
            self.resume_label.setText("Upload a resume before starting.")
            return

        if not job_text.strip():
            self.resume_label.setText("Paste a job description before starting.")
            return

        backend.submit_resume_pdf(Path(self.resume_path))
        backend.submit_job_description(job_text)

        if self.parent:
            self.parent.start_interview(self.resume_path, job_text)