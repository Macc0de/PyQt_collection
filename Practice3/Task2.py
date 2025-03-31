from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QSlider, QDial, \
    QSpinBox, QCheckBox, QVBoxLayout, QFrame
from PySide6.QtCore import Slot, Qt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    @Slot()
    def total_cost(self):
        total = 0
        for product, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                count_slider = self.sliders[product].value()
                count_spin = self.spin_boxes[product].value()
                count_dial = self.dials[product].value()

                count = max(count_slider, count_spin, count_dial)

                price = self.products[product]
                total += price * count

                self.cost_labels[product].setText(f"{price * count} руб.")

        self.label.setText(f"Общая стоимость: {total} руб.")

        for product, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                checkbox.setStyleSheet("font-weight: bold")
            else:
                checkbox.setStyleSheet("")

    def setup(self):
        self.setWindowTitle("Task2")

        self.products = {
            "Хлеб": 23,
            "Мясо": 200,
            "Капуста": 60,
            "Яйца": 90
        }

        layout = QVBoxLayout()
        self.label = QLabel("Общая стоимость: 0 руб.")
        layout.addWidget(self.label)

        self.checkboxes = {}
        self.sliders = {}
        self.spin_boxes = {}
        self.dials = {}
        self.cost_labels = {}

        for product, price in self.products.items():
            product_layout = QHBoxLayout()

            self.label.setFrameStyle(QFrame.Panel)  # для метки
            self.label.setLineWidth(2)

            checkbox = QCheckBox(product)  # checkbox + название
            checkbox.stateChanged.connect(self.total_cost)  # toggled
            product_layout.addWidget(checkbox)
            self.checkboxes[product] = checkbox  # по ключу записывает значение

            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 10)
            slider.valueChanged.connect(self.total_cost)
            product_layout.addWidget(slider)
            self.sliders[product] = slider

            spin_box = QSpinBox()
            spin_box.setRange(0, 10)
            spin_box.valueChanged.connect(self.total_cost)
            product_layout.addWidget(spin_box)
            self.spin_boxes[product] = spin_box

            dial = QDial()
            dial.setRange(0, 10)
            dial.setNotchesVisible(True)
            dial.valueChanged.connect(self.total_cost)
            product_layout.addWidget(dial)
            self.dials[product] = dial

            cost_label = QLabel("0 руб.")
            product_layout.addWidget(cost_label)
            self.cost_labels[product] = cost_label

            layout.addLayout(product_layout)

        self.setLayout(layout)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    app.exec()
