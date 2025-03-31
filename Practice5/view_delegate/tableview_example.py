from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide6.QtWidgets import QApplication, QTableView, QWidget, QVBoxLayout, QPushButton


class MyModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__data = [[1, 1, 1], [2, 2, 2]]

    def rowCount(self, parent=None):
        return len(self.__data)

    def columnCount(self, parent=None):
        return len(self.__data[0])

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return f"Value {self.__data[index.row()][index.column()]}"
        elif role == Qt.EditRole:
            return self.__data[index.row()][index.column()]
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            self.__data[index.row()][index.column()] = value
            return True
        return False

    def flags(self, index):
        """Returns an appropriate value for the item's flags. Valid items are
           enabled, selectable, and editable."""
        if not index.isValid():
            return Qt.ItemIsEnabled
        return super().flags(index) | Qt.ItemIsEditable

    def insertRows(self, row, count, parent=QModelIndex()):
        if row < 0 or count < 1:
            return False
        self.beginInsertRows(parent, row, row + count - 1)
        self.endInsertRows()
        return True

    def append_data(self):
        self.__data.append([5, 5, 5])
        self.insertRow(len(self.__data)-1)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        model = MyModel()
        mainlayout = QVBoxLayout()
        view = QTableView()
        view.setMinimumWidth(600)
        view.setModel(model)
        mainlayout.addWidget(view)
        button = QPushButton("Добавить строку")
        mainlayout.addWidget(button)
        button.clicked.connect(model.append_data)
        self.setLayout(mainlayout)

app = QApplication([])
window = Window()
window.show()
app.exec()
