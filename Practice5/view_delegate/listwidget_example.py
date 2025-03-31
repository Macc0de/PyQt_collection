from PySide6.QtWidgets import QApplication, QAbstractItemView, QListWidget

app = QApplication([])
numbers = ["One", "Two", "Three", "Four", "Five"]
listWidget = QListWidget()
listWidget.setSelectionMode(QAbstractItemView.SingleSelection)
listWidget.addItems(numbers)
listWidget.show()
app.exec()
