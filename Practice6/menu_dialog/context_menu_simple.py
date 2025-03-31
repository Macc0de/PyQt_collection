from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("Действие 1", self))
        context.addAction(QAction("Действие 2", self))
        context.addAction(QAction("Действие 3", self))
        context.exec(e.globalPos())


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
