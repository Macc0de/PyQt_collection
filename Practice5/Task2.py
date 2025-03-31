from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                               QPushButton, QTableView, QLineEdit, QFormLayout)
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex


class Product:
    def __init__(self, name, count, weight_one):
        self.name = name
        self.count = count
        self.weight_one = weight_one

    def total_weight(self):
        return self.weight_one * self.count


class ProductModel(QAbstractTableModel):
    def __init__(self, items=None):
        super().__init__()
        self.items = items or []

    def rowCount(self, parent=None):
        return len(self.items)

    def columnCount(self, parent=None):
        return 3

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            item = self.items[index.row()]
            if index.column() == 0:
                return item.name
            elif index.column() == 1:
                return item.count
            elif index.column() == 2:
                return item.weight_one
        return None

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            headers = ["Название", "Количество", "Масса 1 ед. (кг):"]
            return headers[section]
        return None

    def addItem(self, item):
        self.beginInsertRows(QModelIndex(), len(self.items), len(self.items))
        self.items.append(item)
        self.endInsertRows()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Продукты")

        self.model = ProductModel([
            Product("Молоко", 2, 1.0),
            Product("Картошка", 20, 0.20),
            Product("Курица", 4, 0.15)
        ])

        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        self.name_input = QLineEdit()
        self.count_input = QLineEdit()
        self.weight_input = QLineEdit()

        self.add_button = QPushButton("Добавить продукт")
        self.add_button.clicked.connect(self.add_product)

        self.label = QLabel()
        self.update_total_weight()

        form_layout = QFormLayout()
        form_layout.addRow("Название:", self.name_input)
        form_layout.addRow("Количество:", self.count_input)
        form_layout.addRow("Масса 1 ед. (кг):", self.weight_input)

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        layout.addLayout(form_layout)
        layout.addWidget(self.add_button)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def add_product(self):
        name = self.name_input.text().strip()
        count = self.count_input.text().strip()
        unit_weight = self.weight_input.text().strip()

        if not name or not count or not unit_weight:
            return
        try:
            count = int(count)
            unit_weight = float(unit_weight)
        except ValueError:
            self.name_input.clear()
            self.count_input.clear()
            self.weight_input.clear()
            return

        new_product = Product(name, count, unit_weight)
        self.model.addItem(new_product)
        self.update_total_weight()

        self.name_input.clear()
        self.count_input.clear()
        self.weight_input.clear()

    def update_total_weight(self):
        total_weight = 0
        for item in self.model.items:
            total_weight += item.total_weight()
        self.label.setText(f"Общий вес продуктов: {total_weight:.2f} кг")


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
