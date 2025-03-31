from PySide6.QtWidgets import (QWizard, QMessageBox, QWizardPage, QLabel, QVBoxLayout, QCheckBox, QApplication,
                               QLineEdit, QFormLayout, QListWidget, QMainWindow, QPushButton, QTextEdit, QWidget)


class Wizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: black")
        self.addPage(LoginPage())
        self.addPage(FullNamePage())
        self.addPage(TopicsPage())
        self.setWindowTitle("Wizard Registration")

    def accept(self):
        QMessageBox.information(None, "Wizard", "Wizard is accepted")
        super().accept()


class LoginPage(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Регистрация")
        self.setStyleSheet("background-color: purple")

        self.login_label = QLabel("Логин:")
        self.password_label = QLabel("Пароль:")
        self.login_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        layout = QFormLayout()
        layout.addRow(self.login_label, self.login_edit)
        layout.addRow(self.password_label, self.password_edit)
        self.setLayout(layout)

        self.registerField("login*", self.login_edit)
        self.registerField("password*", self.password_edit)


class FullNamePage(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Ввод ФИО")
        self.setStyleSheet("background-color: purple")

        self.fio_label = QLabel("ФИО:")
        self.fio_edit = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.fio_label)
        layout.addWidget(self.fio_edit)
        self.setLayout(layout)

        self.registerField("fio*", self.fio_edit)


class TopicsPage(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Выберите интересующие темы")
        self.setStyleSheet("background-color: purple")
        layout = QFormLayout()

        self.topics = QListWidget()
        self.topics.addItems(["Новости", "Погода", "Отдых", "Природа", "Образование"])
        self.topics.setSelectionMode(QListWidget.MultiSelection)
        layout.addRow("Темы:", self.topics)

        self.privacy = QCheckBox("Согласен на обработку персональных данных")
        layout.addRow(self.privacy)

        self.setLayout(layout)

        self.registerField("topics*", self.topics)
        self.registerField("privacy*", self.privacy)

    def selected_topics(self):
        return [item.text() for item in self.topics.selectedItems()]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Главное окно")

        self.start_wizard_button = QPushButton("Пройти регистрацию", self)
        self.start_wizard_button.clicked.connect(self.start_wizard)

        self.info = QTextEdit(self)
        self.info.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.start_wizard_button)
        layout.addWidget(self.info)

        widget = QWidget()
        widget.setLayout(layout)  # устанавливаем слой
        self.setCentralWidget(widget)

    def start_wizard(self):
        wizard = Wizard()
        if wizard.exec() == QWizard.Accepted:
            login = wizard.field("login")
            password = wizard.field("password")
            fio = wizard.field("fio")
            topics_page = wizard.page(2)
            selected_topics = topics_page.selected_topics()  # выбранные темы

            info = f"Логин: {login}\nПароль: {password}\nФИО: {fio}\nТемы: {', '.join(selected_topics)}"
            self.info.setText(info)


if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
