from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from backend.backend import prompt_gemini

class InterviewPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.recording = False
        self.resume = ""
        self.job = ""

        layout = QVBoxLayout()

        self.question_label = QLabel("Waiting for AI to generate your question...")
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setWordWrap(True)
        layout.addWidget(self.question_label)

        self.record_button = QPushButton("Start Recording")
        self.record_button.clicked.connect(self.toggle_recording)
        layout.addWidget(self.record_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.next_button = QPushButton("Next Question")
        self.next_button.clicked.connect(self.next_question)
        layout.addWidget(self.next_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def load_interview(self, resume, job):
        self.resume = resume
        self.job = job
        self.question_label.setText("Question1")

    def toggle_recording(self):
        if not self.recording:
            self.record_button.setText("Stop Recording")
            print("Recording started...")
        else:
            self.record_button.setText("Start Recording")
            print("Recording stopped.")
        self.recording = not self.recording

    def next_question(self):
        self.question_label.setText("Question2")
