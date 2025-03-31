from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QVBoxLayout, QLabel, QWidget
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
        menuFile = menuBar.addMenu("Файл")
        menuCreate = menuFile.addMenu("Создать")
        actionProject = menuCreate.addAction("Проект")
        actionFile = menuCreate.addAction("Файл")
        actionOpen = menuFile.addAction("Открыть")
        menuBar.triggered.connect(self.clickMenuBar)
        menuFile.triggered.connect(self.clickMenu)
        menuCreate.triggered.connect(self.clickMenu)
        actionProject.triggered.connect(self.clickActionProject)
        actionFile.triggered.connect(self.clickActionFile)
        actionOpen.triggered.connect(self.clickActionOpen)

    @Slot()
    def clickMenuBar(self):
        print("Нажат QMenuBar. Это тоже можно отследить")

    @Slot()
    def clickMenu(self):
        print("Нажат QMenu. Это тоже можно отследить")

    @Slot()
    def clickActionProject(self):
        self.label.setText("Создание проекта")

    @Slot()
    def clickActionFile(self):
        self.label.setText("Создание файла")

    @Slot()
    def clickActionOpen(self):
        self.label.setText("Открытие проекта")

app = QApplication([])
window = Window()
window.show()
app.exec()
