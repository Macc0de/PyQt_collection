from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QLabel, QButtonGroup
from PySide6.QtCore import Slot


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    @Slot()
    def switch(self):
        for radio in self.radio_buttons:
            if radio.isChecked():
                self.label.setText(self.seasons[radio.text()])  # По ключу
                break

    def setup(self):
        self.setWindowTitle("Task1")

        self.label = QLabel()
        self.radio_group = QButtonGroup(self)

        self.seasons = {
            "Весна": "Все цветет",
            "Лето": "Тепло, каникулы и море",
            "Осень": "Переход от лета к зиме",
            "Зима": "Холодное время года"
        }

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        self.radio_buttons = []  # Состоит из radio
        for season, info in self.seasons.items():
            radio = QRadioButton(season)
            radio.toggled.connect(self.switch)
            layout.addWidget(radio)
            self.radio_group.addButton(radio)
            self.radio_buttons.append(radio)

        self.radio_buttons[3].setChecked(True)
        self.switch()

        self.setLayout(layout)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    app.exec()
