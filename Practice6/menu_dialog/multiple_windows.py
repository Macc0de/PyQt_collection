from random import randint

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget


class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel(f"Another Window {randint(0, 100)}")
        layout.addWidget(self.label)
        self.setLayout(layout)
        # self.setWindowModality(Qt.ApplicationModal)

    def set_text(self, text):
        self.label.setText(text)

    def get_number(self):
        return self.label.text().split()[-1]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window1 = AnotherWindow()
        self.window2 = AnotherWindow()

        column = QVBoxLayout()
        button1 = QPushButton("Push for Window 1")
        button1.clicked.connect(lambda checked: self.toggle_window(self.window1))
        column.addWidget(button1)

        button2 = QPushButton("Push for Window 2")
        button2.clicked.connect(lambda checked: self.toggle_window(self.window2))
        column.addWidget(button2)

        w = QWidget()
        w.setLayout(column)
        self.setCentralWidget(w)

    def toggle_window(self, window):
        if window.isVisible():
            window.hide()
            print(f'Number was {window.get_number()}')
        else:
            window.show()
            window.set_text(f"New text {randint(0, 100)}")


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
