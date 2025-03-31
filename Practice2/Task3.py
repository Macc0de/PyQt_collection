from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def calculator(self, operation):
        try:
            num1 = int(self.input1.text())
            num2 = int(self.input2.text())

            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "*":
                result = num1 * num2
            elif operation == "/":
                if num2 == 0:
                    raise ZeroDivisionError
                result = round(num1 / num2, 2)
            elif operation == "^":
                result = pow(num1, num2)
                self.output.setText(f"{num1}<sup>{num2}</sup> = {result}")
                return

            self.output.setText(f"{num1} {operation} {num2} = {result}")

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите числа!")
        except ZeroDivisionError:
            QMessageBox.warning(self, "Ошибка", "Нельзя делить на 0!")

    def setup(self):
        self.setWindowTitle("Task3")

        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.output = QLabel("Ответ")
        self.output.setStyleSheet("font-size: 25px; font-weight: bold; color: pink;")

        self.button_plus = QPushButton("➕", self)
        self.button_minus = QPushButton("➖", self)
        self.button_multiply = QPushButton("✖️", self)
        self.button_divide = QPushButton("➗", self)
        self.button_power = QPushButton("⬆️", self)

        self.button_plus.clicked.connect(lambda: self.calculator("+"))
        self.button_minus.clicked.connect(lambda: self.calculator("-"))
        self.button_multiply.clicked.connect(lambda: self.calculator("*"))
        self.button_divide.clicked.connect(lambda: self.calculator("/"))
        self.button_power.clicked.connect(lambda: self.calculator("^"))

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input1)
        input_layout.addWidget(self.input2)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.button_plus)
        button_layout.addWidget(self.button_minus)
        button_layout.addWidget(self.button_multiply)
        button_layout.addWidget(self.button_divide)
        button_layout.addWidget(self.button_power)

        layout = QVBoxLayout()
        layout.addLayout(input_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.output)

        self.setLayout(layout)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    app.exec()
