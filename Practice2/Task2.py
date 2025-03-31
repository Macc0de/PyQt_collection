from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.counter = 0  # Модель
        self.setup()

    def increase(self):
        self.counter += 1
        self.text.setText(f"Счётчик: {self.counter}")

    def reset(self):
        self.counter = 0
        self.text.setText(f"Счётчик: {self.counter}")

    def setup(self):
        self.setWindowTitle("Task2")
        # Вид
        self.text = QLabel(f"Счётчик: {self.counter}")
        self.button_increase = QPushButton("Увеличить", self)
        self.button_reset = QPushButton("Сбросить", self)
        # Контроллер
        self.button_increase.clicked.connect(self.increase)
        self.button_reset.clicked.connect(self.reset)

        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.button_increase)
        layout.addWidget(self.button_reset)
        self.setLayout(layout)

        # self.resize(200, 150)

        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    app.exec()
