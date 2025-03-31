from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, \
    QDateEdit, QTextEdit
from PySide6.QtCore import Slot
from datetime import datetime


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    @Slot()
    def calculate(self):
        birth_date = self.birthday.date()

        birth_datetime = datetime(birth_date.year(), birth_date.month(), birth_date.day(), 0, 0)
        current_datetime = datetime.now()

        age_years = current_datetime.year - birth_datetime.year
        if (birth_datetime.month, birth_datetime.day) > (current_datetime.month, current_datetime.day):
            age_years -= 1

        age_hours = int((current_datetime - birth_datetime).total_seconds() // 3600)
        age_seconds = int((current_datetime - birth_datetime).total_seconds())
        if age_years < 0 or age_hours < 0:
            self.text.setText("Некорректная дата рождения")
            return

        result = (
            f'<b><i><h3 style="font-family:consolas; color:yellow;">Вам {age_years} лет</h3></i></b>'
            f'<i><h2 style="font-family:arial; color:red;">Вам {age_hours} часов</h2></i>'
            f'<u><h1 style="font-family:comic sans ms; color:pink;">Вам {age_seconds} секунд</h1></u>'
        )

        self.text.setHtml(result)

    def setup(self):
        self.setWindowTitle("Task2")

        layout = QHBoxLayout()
        self.label = QLabel("Введите дату рождения: ")
        layout.addWidget(self.label)

        self.birthday = QDateEdit()
        self.birthday.setCalendarPopup(True)
        self.birthday.dateChanged.connect(self.calculate)
        layout.addWidget(self.birthday)

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

        self.setLayout(layout)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    app.exec()
