from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Slot


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    @Slot()
    def button_pressed(self):
        self.label.setText("Нажата")

    @Slot()
    def button_released(self):
        self.label.setText("Отпущена")

    def setup(self):
        self.setWindowTitle("Task1")

        self.button = QPushButton("Нажать", self)
        self.label = QLabel("Отпущена", self)

        self.button.pressed.connect(self.button_pressed)
        self.button.released.connect(self.button_released)

        layout = QHBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    app.exec()
