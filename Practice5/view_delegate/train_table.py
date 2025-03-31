from PySide6.QtCore import Qt, QAbstractTableModel
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication, QAbstractItemView, QTableView
from train import Train


class TableModel(QAbstractTableModel):
    def __init__(self, train_list):
        super(TableModel, self).__init__()
        self.__train_list = train_list
        self.__headers = ['Поезд', 'Время отправления', 'Время прибытия', 'Время в пути']

    def rowCount(self, parent=None):
        return len(self.__train_list)

    def columnCount(self, parent=None):
        return 4

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            train = self.__train_list[index.row()]
            if index.column() == 0:
                return train.name()
            elif index.column() == 1:
                return train.start_time()
            elif index.column() == 2:
                return train.arrival_time()
            else:
                return str(train.travel_time())
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.__headers[section]
        return section


class Window(QWidget):
    def __create_model(self):
        train_list = [Train('Москва-Ярославль', "12/03/23 11:00", "12/03/23 14:00"),
                      Train('Ярославль-Москва', "12/03/23 15:00", "12/03/23 18:00"),
                      Train('Москва-Казань', "12/03/23 23:00", "13/03/23 12:00"),
                      Train('Казань-Москва', "13/03/23 14:00", "14/03/23 01:00")]
        self.__trains = TableModel(train_list)

    def __init__(self):
        super().__init__()
        self.__create_model()
        mainlayout = QVBoxLayout()
        view = QTableView()
        view.setMinimumWidth(600)
        view.setModel(self.__trains)
        view.setColumnWidth(0, 120)
        view.setColumnWidth(1, 150)
        view.setColumnWidth(2, 150)
        view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        mainlayout.addWidget(view)
        self.setLayout(mainlayout)

app = QApplication([])
window = Window()
window.show()
app.exec()
