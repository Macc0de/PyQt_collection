from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QMessageBox, \
    QColorDialog
from PySide6.QtCore import Slot


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.add_menu()
        layout = QVBoxLayout()
        self.label = QLabel()
        layout.addWidget(self.label)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def add_menu(self):
        menuBar = self.menuBar()
        menuBar.resize(100, 20)
        menuDialogs = menuBar.addMenu("Диалоги")
        actionColor = menuDialogs.addAction("Цвет")
        actionInfo = menuDialogs.addAction("Информация")
        actionColor.triggered.connect(self.clickActionColor)
        actionInfo.triggered.connect(self.clickActionInfo)

    @Slot()
    def clickActionColor(self):
        color = QColorDialog.getColor()
        self.label.setText(color.name())

    @Slot()
    def clickActionInfo(self):
        msgBox = QMessageBox()
        msgBox.setText("Произошло событие.")
        msgBox.setInformativeText("Какой вариант вы выбираете?")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Save)
        ret = msgBox.exec()
        if ret == QMessageBox.Save:
            self.label.setText("Нажата кнопка сохранения")

app = QApplication([])
window = Window()
window.show()
app.exec()
