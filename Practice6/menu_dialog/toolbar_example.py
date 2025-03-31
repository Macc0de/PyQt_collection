from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QLabel, QToolBar, QStatusBar, QApplication


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        label = QLabel("Hello!")
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)
        button_action = QAction(QIcon("clocks.png"), "Часы", self)
        button_action.setStatusTip("Кнопка с часами")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)
        self.setStatusBar(QStatusBar(self))


    def onMyToolBarButtonClick(self, s):
        print("click", s)

app = QApplication([])
window = Window()
window.show()
app.exec()
