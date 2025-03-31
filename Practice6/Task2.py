from PySide6.QtWidgets import (QApplication, QMainWindow, QListView, QVBoxLayout, QWidget, QPushButton,
                               QDialog, QLineEdit, QMenu, QLabel)
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex
from PySide6.QtGui import QAction
from datetime import datetime


class NoteDialog(QDialog):
    def __init__(self, text="", date=None):
        super().__init__()
        self.setWindowTitle("Диалог")

        self.layout = QVBoxLayout(self)

        self.note_edit = QLineEdit(self)
        self.note_edit.setText(text)
        self.layout.addWidget(self.note_edit)

        self.date_label = QLabel(self)
        self.date_label.setText(f"{date if date else datetime.now().strftime('%H:%M %Y-%m-%d')}")
        self.layout.addWidget(self.date_label)

        self.button = QPushButton("OK", self)
        self.button.clicked.connect(self.accept)
        self.layout.addWidget(self.button)

    def get_note(self):
        return self.note_edit.text()


class NoteModel(QAbstractListModel):
    def __init__(self, items=None):
        super().__init__()
        self.items = items or []

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self.items)

    def data(self, index, role):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            note = self.items[index.row()]
            return f"{note['text']} ({note['date']})"
        return None

    def add_note(self, text):
        self.beginInsertRows(QModelIndex(), len(self.items), len(self.items))
        self.items.append({"text": text, "date": datetime.now().strftime('%H:%M %Y-%m-%d')})  # словарь
        self.endInsertRows()

    def setData(self, index, value, role=Qt.EditRole):  # для Edit
        if index.isValid() and 0 <= index.row() < len(self.items):
            self.items[index.row()]["text"] = value
            self.dataChanged.emit(index, index, [Qt.DisplayRole])
            return True
        return False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заметки")

        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)

        self.add_button = QPushButton("Добавить", self)
        self.add_button.clicked.connect(self.open_dialog)
        self.layout.addWidget(self.add_button)

        self.view = QListView(self)
        self.layout.addWidget(self.view)

        self.model = NoteModel()
        self.view.setModel(self.model)

        self.view.setContextMenuPolicy(Qt.CustomContextMenu)  # Свое (1)контекстное меню для заметки
        self.view.customContextMenuRequested.connect(self.show_menu)

        self.menu = self.menuBar().addMenu("Меню")  # (2)меню
        self.add_action = QAction("Добавить заметку", self)
        self.add_action.triggered.connect(self.open_dialog)
        self.menu.addAction(self.add_action)

        self.edit_action = QAction("Изменить заметку", self)
        self.edit_action.triggered.connect(self.open_editDialog)
        self.menu.addAction(self.edit_action)

    def show_menu(self, position):
        index = self.view.indexAt(position)
        if index.isValid():
            menu = QMenu(self)

            edit_action = QAction("Изменить", self)
            edit_action.triggered.connect(self.open_editDialog)
            menu.addAction(edit_action)
            menu.exec(self.view.viewport().mapToGlobal(position))

    def open_dialog(self):
        dialog = NoteDialog()
        if dialog.exec():
            text = dialog.get_note()
            if text:  # если текст ввели
                self.model.add_note(text)

    def open_editDialog(self):
        index = self.view.currentIndex()
        if not index.isValid():
            return
        old_note = self.model.items[index.row()]  # старая записка

        dialog = NoteDialog(old_note["text"], old_note["date"])
        if dialog.exec():
            new_text = dialog.get_note()
            if new_text:
                self.model.setData(index, new_text)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
