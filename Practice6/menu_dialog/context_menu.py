from PySide6.QtCore import QAbstractTableModel, Qt, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QTableView


class MyModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def rowCount(self, parent=None):
        return 2

    def columnCount(self, parent=None):
        return 3

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row() + 1
            column = index.column() + 1
            return f"Row {row}, Column {column}"
        return None


@Slot()
def print_info():
    row = table_view.currentIndex().row() + 1
    column = table_view.currentIndex().column() + 1
    print(f"Row {row}, Column {column}")

if __name__ == '__main__':
    app = QApplication([])
    table_view = QTableView()
    my_model = MyModel()
    table_view.setModel(my_model)
    table_view.setContextMenuPolicy(Qt.ActionsContextMenu)
    infoAction = QAction("Info", None)
    table_view.addAction(infoAction)
    infoAction.triggered.connect(print_info)
    table_view.show()
    app.exec()
