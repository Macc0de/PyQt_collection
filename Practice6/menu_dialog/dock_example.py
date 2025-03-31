from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QDockWidget, QListWidget, QTextEdit


class DockDemo(QMainWindow):
    def __init__(self,parent=None):
        super(DockDemo, self).__init__(parent)
        self.setWindowTitle('Боковой виджет')
        layout=QHBoxLayout()
        bar=self.menuBar()
        file=bar.addMenu('Файл')
        file.addAction('Создать')
        file.addAction('Сохранить')

        self.items=QDockWidget('Панель',self)

        self.listWidget=QListWidget()
        self.listWidget.addItem('Шаблон 1')
        self.listWidget.addItem('Шаблон 2')
        self.listWidget.addItem('Шаблон 3')
        self.listWidget.addItem('Шаблон 4')

        self.items.setWidget(self.listWidget)
        self.items.setFloating(False)
        self.setCentralWidget(QTextEdit())
        self.addDockWidget(Qt.RightDockWidgetArea,self.items)

        self.setLayout(layout)

if __name__ == '__main__':
    app=QApplication([])
    demo=DockDemo()
    demo.show()
    app.exec()