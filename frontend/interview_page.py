from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QScrollArea
)
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
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.question_label = QLabel("Waiting for AI to generate your question")
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setWordWrap(True)
        self.question_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.question_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.question_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #e2e8f0;
                background-color: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(100, 116, 139, 0.3);
                border-radius: 12px;
                padding: 16px;
                line-height: 1.5;
            }
        """)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.question_label)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        layout.addWidget(self.scroll_area)

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
            start_rec_success: bool = backend.start_voice_recording()

            if not start_rec_success:
                raise Exception("Failed to start recording.")
            else:
                print("Recording started.")
        else:
            self.record_button.setText("Start Recording")
            path = backend.stop_voice_recording()

            if path is None:
                raise Exception("Failed to stop recording.")
            else:
                print("Recording stopped.")

            transcript = backend.transcribe_audio(path)
            print(f"Transcript: {transcript}")

            result = backend.answer_interview_question(transcript)
            print(f"AI Response: {result}")

            self.question_label.setText(result or "No response received.")
            self.question_label.adjustSize()

        self.recording = not self.recording

    def next_question(self):
        if self.current_question_index < self.total_questions - 1:
            self.current_question_index += 1
            self.update_question_display()
        else:
            self.next_button.hide()
            self.record_button.hide()
            feedback = backend.get_interview_feedback()
            self.question_label.setText(feedback)
            self.question_label.adjustSize()

    def update_question_display(self):
        question = self.questions[self.current_question_index]
        self.question_label.setText(
            f"Question {self.current_question_index + 1} of {self.total_questions}:\n\n{question}"
        )
        self.question_label.adjustSize()