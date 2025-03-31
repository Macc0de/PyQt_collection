from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QCheckBox, QDialog, QLabel
from PySide6.QtCore import Signal


class Dialog(QDialog):
    checkbox_state = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Диалог с чекбоксом")

        self.layout = QVBoxLayout(self)

        self.checkbox = QCheckBox("Соглашаюсь", self)
        self.layout.addWidget(self.checkbox)

        self.ok_button = QPushButton("ОК", self)
        self.ok_button.clicked.connect(self.send_state)
        self.layout.addWidget(self.ok_button)

    def send_state(self):
        self.checkbox_state.emit(self.checkbox.isChecked())
        self.accept()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Главное окно")

        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)

        self.button = QPushButton("Открыть диалог")
        self.button.clicked.connect(self.open_dialog)
        layout.addWidget(self.button)

        self.label = QLabel()
        layout.addWidget(self.label)

    def open_dialog(self):
        dialog = Dialog()
        dialog.checkbox_state.connect(self.handle_checkbox)
        dialog.exec()

    def handle_checkbox(self, checked):
        self.label.setText("Выбран" if checked else "Не выбран")


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
