from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
import backend
from backend import backend

class InterviewPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.recording = False
        self.resume = ""
        self.job = ""
        self.current_question_index = 0
        self.total_questions = 5
        self.questions = []

        layout = QVBoxLayout()

        self.question_label = QLabel("Waiting for AI to generate your question")
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

        self.questions = [backend.ask_interview_question() for _ in range(self.total_questions)]

        self.current_question_index = 0
        self.update_question_display()

    def toggle_recording(self):
        if not self.recording:
            self.record_button.setText("Stop Recording")
            path = backend.stop_voice_recording()
            backend.transcribe_audio(path)
            print("Recording started.")
        else:
            self.record_button.setText("Start Recording")
            backend.start_voice_recording()

            print("Recording stopped.")
        self.recording = not self.recording

    def next_question(self):
        if self.current_question_index < self.total_questions - 1:
            self.current_question_index += 1
            self.update_question_display()
        else:
            self.next_button.hide()
            self.question_label.setText(backend.get_interview_feedback())

    def update_question_display(self):
        question = self.questions[self.current_question_index]
        self.question_label.setText(f"Question {self.current_question_index + 1} of {self.total_questions}:\n\n{question}")
