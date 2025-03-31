from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication, QListWidget, QAbstractItemView, QListView, QPushButton
from train import Train


class ListModel(QAbstractListModel):
    def __init__(self, train_list):
        super(ListModel, self).__init__()
        self.__train_list = train_list

    def rowCount(self, parent=None):
        return len(self.__train_list)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return str(self.__train_list[index.row()])
        return None
    
    def removeRows(self, row, count, parent=QModelIndex()):
        if row + count >= len(self.__train_list) or count < 1:
            return False
        self.beginRemoveRows(parent, row, row + count - 1)
        del self.__train_list[row:row+count]
        self.endRemoveRows()
        return True


class Window(QWidget):
    def __create_model(self):
        train_list = [Train('Москва-Ярославль', "12/03/23 11:00", "12/03/23 14:00"),
                      Train('Ярославль-Москва', "12/03/23 15:00", "12/03/23 18:00"),
                      Train('Москва-Казань', "12/03/23 23:00", "13/03/23 12:00"),
                      Train('Казань-Москва', "13/03/23 14:00", "14/03/23 01:00")]
        self.__trains = ListModel(train_list)

    def __init__(self):
        super().__init__()
        self.__create_model()
        mainlayout = QVBoxLayout()
        view = QListView()
        view.setMinimumWidth(600)
        view.setModel(self.__trains)
        view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        mainlayout.addWidget(view)
        button = QPushButton("Удалить первый")
        mainlayout.addWidget(button)
        button.clicked.connect(self.remove_item)
        self.setLayout(mainlayout)

    def remove_item(self):
        self.__trains.removeRow(0)


app = QApplication([])
window = Window()
window.show()
app.exec()
