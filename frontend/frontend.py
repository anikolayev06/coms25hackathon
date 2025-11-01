import sys

from PyQt6.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("coms25")
window.setGeometry(100, 100, 400, 300)

window.show()

sys.exit(app.exec())