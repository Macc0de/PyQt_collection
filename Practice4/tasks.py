from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QListWidget, QCheckBox, QLineEdit,
                               QFormLayout, QPushButton, QMessageBox, QGridLayout, QTabWidget, QDial)
from PySide6.QtGui import QMouseEvent, QDrag
from PySide6.QtCore import Slot, Qt, QMimeData


# (((1)))
class Schedule(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        layout = QGridLayout()

        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
        times = ["09:00 - 10:35", "10:45 - 12:20", "12:30 - 14:05", "15:05 - 16:40"]
        subjects = {
            (0, 0): "",
            (0, 1): "Диффуры Лекция",
            (0, 2): "PyQt Лекция",
            (0, 3): "ИТ21: PyQt Практика\nИТ22: Тестирование",
            (1, 0): "C# Лекция",
            (1, 1): "C# Практика",
            (1, 2): "Теорвер Лекция",
            (2, 0): "",
            (2, 1): "Алгоритмы Лекция",
            (2, 2): "ИТ21: КомпСети Семинар\nИТ22: Алгоритмы Практика",
            (2, 3): "ИТ21: Алгоритмы Практика\nИТ22: КомпСети Семинар",
            (3, 0): "ИТ21: ТеорВер Практика\nИТ22: Диффуры Практика",
            (3, 1): "ИТ21: Диффуры Практика\nИТ22: ТеорВер Практика",
            (4, 0): "",
            (4, 1): "Физра",
            (4, 2): "Этика",
            (4, 3): "Тестирование"
        }

        for i, day in enumerate(days):
            layout.addWidget(QLabel(day), 0, i + 1)
        for j, time in enumerate(times):
            layout.addWidget(QLabel(time), j + 1, 0)
        for (i, j), subject in subjects.items():
            layout.addWidget(QLabel(subject), j + 1, i + 1)  # столбец, строка

        layout.setSpacing(20)
        self.setLayout(layout)


# (((2)))
class Account(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        layout = QFormLayout()

        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.middle_name = QLineEdit()
        layout.addRow("Имя:", self.first_name)
        layout.addRow("Фамилия:", self.last_name)
        layout.addRow("Отчество:", self.middle_name)

        self.email = QLineEdit()
        self.phone = QLineEdit()
        layout.addRow("Email:", self.email)
        layout.addRow("Телефон:", self.phone)

        self.topics = QListWidget()
        self.topics.addItems(["Новости", "Погода", "Отдых", "Природа", "Образование"])
        self.topics.setSelectionMode(QListWidget.MultiSelection)
        self.topics.setFixedHeight(100)
        self.topics.setFixedWidth(200)
        layout.addRow("Темы:", self.topics)

        self.privacy = QCheckBox("Согласен на обработку персональных данных")
        layout.addRow(self.privacy)
        self.ad = QCheckBox("Согласен на получение рассылки")
        layout.addRow(self.ad)

        self.submit_button = QPushButton("Отправить")
        self.submit_button.clicked.connect(self.validation)
        layout.addRow(self.submit_button)

        self.setLayout(layout)

    @Slot()
    def validation(self):
        if not self.first_name.text() or not self.last_name.text() or not self.middle_name.text():
            self.show_error("Поля ввода должны быть заполнеными!")
            return

        if not self.email.text() or not self.phone.text():
            self.show_error("Введите email и номер телефона!")
            return

        sample = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(sample, self.email.text()):
            self.show_error("Введите корректный Email!")
            return

        if not self.phone.text().isdigit():
            self.show_error("Номер телефона должен содержать только цифры!")
            return

        if not self.privacy.isChecked():
            self.show_error("Вы должны быть согласны на обработку персональных данных!")
            return

        QMessageBox.information(self, "Ответ", "Форма корректна!")

    def show_error(self, text):
        QMessageBox.critical(self, "Ошибка", text)


# (((3)))
class DragWidget(QDial):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")
        self.setRange(0, 10)
        self.setNotchesVisible(True)
        self.resize(100, 100)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.position().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if (event.position().toPoint() - self.drag_start_position).manhattanLength() < 10:
            return

        drag = QDrag(self)
        mime_data = QMimeData()  # Данные, связанные с перетаскиваемым объектом
        drag.setMimeData(mime_data)

        pixmap = self.grab()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.position().toPoint() - self.rect().topLeft())

        drag.exec(Qt.MoveAction)


class Click(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            x, y = event.position().toPoint().x(), event.position().toPoint().y()

            if y < self.height() / 2:  # Только в верхней половине
                dial = DragWidget(self)
                dial.move(int(x) - dial.width() // 2, int(y) - dial.height() // 2)
                dial.show()

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        pos = event.position().toPoint()

        if pos.y() >= self.height() / 2:
            source = event.source()
            new_x = int(pos.x()) - source.width() // 2
            new_y = int(pos.y()) - source.height() // 2

            source.move(new_x, new_y)
            source.show()

            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()


class Window(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.schedule = Schedule()
        self.account = Account()
        self.click = Click()

        self.addTab(self.schedule, "Расписание")
        self.addTab(self.account, "Форма")
        self.addTab(self.click, "Перемещаемый виджет")

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
