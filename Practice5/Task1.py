from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListView, QLineEdit
from PySide6.QtCore import QAbstractListModel, Qt


class ListModel(QAbstractListModel):
    def __init__(self, items=None):
        super().__init__()
        self.items = items or []

    def rowCount(self, parent=None):
        return len(self.items)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return self.items[index.row()]
        return None

    def add_item(self, item):
        self.beginInsertRows(self.index(len(self.items), 0), len(self.items), len(self.items))
        self.items.append(item)
        self.endInsertRows()

    def remove_item(self, row):
        if 0 <= row < len(self.items):
            self.beginRemoveRows(self.index(row, 0), row, row)
            del self.items[row]
            self.endRemoveRows()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заметки")

        self.model = ListModel()

        self.view = QListView()
        self.view.setModel(self.model)
        self.view.clicked.connect(self.remove_note)

        self.input = QLineEdit()
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_note)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input)
        input_layout.addWidget(self.add_button)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addLayout(input_layout)

        self.setLayout(layout)

    def add_note(self):
        text = self.input.text().strip()
        if text:
            self.model.add_item(text)
            self.input.clear()

    def remove_note(self, index):
        self.model.remove_item(index.row())


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
