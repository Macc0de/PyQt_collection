from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QApplication, QPushButton, QMainWindow


class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Привет!")
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout = QVBoxLayout()
        message = QLabel(self.get_message())
        layout.addWidget(message)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

    def get_message(self):
        return "Диалог открылся, так и надо?"

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        button = QPushButton("Открою диалог")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self, s):
        dlg = CustomDialog()
        if dlg.exec():
            print('Получаю данные от диалога, нашла вот такой текст:', dlg.get_message())
        else:
            print("Отмена")


app = QApplication([])
window = Window()
window.show()
app.exec()
