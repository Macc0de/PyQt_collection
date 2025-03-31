from PySide6.QtCore import QStringListModel
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QListView


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        listView = QListView()
        self.data = ['Item 1', 'Item 2', 'Item 3', 'Item 4']
        listView.setModel(QStringListModel(self.data))
        listView.clicked.connect(self.clicked)
        self.setCentralWidget(listView)

    def clicked(self, modelIndex):
        print('You have selected:' + self.data[modelIndex.row()])


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
