from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from frontend.upload_page import UploadPage
from frontend.interview_page import InterviewPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PrepTalk")
        self.setGeometry(100, 100, 600, 400)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.upload_page = UploadPage(self)
        self.interview_page = InterviewPage(self)

        self.stack.addWidget(self.upload_page)
        self.stack.addWidget(self.interview_page)

        self.stack.setCurrentWidget(self.upload_page)

    def start_interview(self, resume_text, job_text):
        self.interview_page.load_interview(resume_text, job_text)
        self.stack.setCurrentWidget(self.interview_page)