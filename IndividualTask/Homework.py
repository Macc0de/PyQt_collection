from PySide6.QtGui import QAction, QRegularExpressionValidator
from PySide6.QtWidgets import (QApplication, QWidget, QListWidget, QCheckBox, QLineEdit,
                               QFormLayout, QPushButton, QHBoxLayout, QDialog, QVBoxLayout, QMainWindow,
                               QMessageBox, QListView, QMenu, QComboBox, QInputDialog, QLabel, QFrame, QDateEdit)
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex, QRegularExpression, QDate
from datetime import datetime
import csv


class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.uid = 0
        self.filename = "users_data.csv"
        self.setWindowTitle("Вход в личный кабинет")
        self.resize(300, 100)  # ширина, высота

        layout = QFormLayout()

        self.login = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        layout.addRow("Логин:", self.login)
        layout.addRow("Пароль:", self.password)

        self.password_checkbox = QCheckBox("Показать пароль")
        self.password_checkbox.toggled.connect(lambda checked: password_visibility(self.password, checked))
        layout.addRow(self.password_checkbox)

        self.submit_button = QPushButton("Войти")
        self.submit_button.clicked.connect(self.authorization)  # Проверить есть ли в БД
        layout.addRow(self.submit_button)

        self.setLayout(layout)

    def authorization(self):
        if not validation(self.login, self.password, self):
            return

        success, self.uid = verification(self.login, self.password, self.filename, self)  # uid сохранено
        if success:
            QMessageBox.information(self, "Ответ", "Вы вошли в аккаунт")
            self.accept()  # Перейти в Главное Окно
        else:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            self.reject()  # Вернуться в Начальное Окно

    def get_uid(self):
        return self.uid


class Registration(QDialog):
    def __init__(self):
        super().__init__()
        self.uid = 1
        self.filename = "users_data.csv"
        self.update_uid()

        self.setWindowTitle("Регистрация")
        self.resize(300, 100)

        layout = QFormLayout()

        self.login = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        layout.addRow("Логин:", self.login)
        layout.addRow("Пароль:", self.password)

        self.password_checkbox = QCheckBox("Показать пароль")
        self.password_checkbox.toggled.connect(lambda checked: password_visibility(self.password, checked))
        layout.addRow(self.password_checkbox)

        self.submit_button = QPushButton("Зарегистрироваться")
        self.submit_button.clicked.connect(self.registration)  # Добавить данные в БД
        layout.addRow(self.submit_button)

        self.setLayout(layout)

    def get_uid(self):
        return self.uid

    def update_uid(self):  # Кол-во юзеров
        with open(self.filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for _ in reader:
                self.uid += 1

    def registration(self):
        if not validation(self.login, self.password, self):
            return

        if verification(self.login, self.password, self.filename, self)[0]:  # [0] - только True
            QMessageBox.warning(self, "Ошибка", "Такой пользователь уже зарегистрирован")
            self.reject()
            return

        uid = "uid_" + str(self.uid)
        user_data = [uid, self.login.text(), self.password.text()]
        self.save_user(user_data)
        QMessageBox.information(self, "Ответ", "Вы зарегистрировались")
        self.accept()

    def save_user(self, data):
        try:
            with open(self.filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(data)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка записи файла", f"Не удалось зарегистрировать пользователя: {str(e)}")


def verification(login: QLineEdit, password: QLineEdit, filename, parent_window):
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row and row[1] == login.text() and row[2] == password.text():
                    return (True, row[0][4:])
    except Exception as e:
        QMessageBox.critical(parent_window, "Ошибка чтения файла", f"Не удалось проверить данные пользователя: {str(e)}")
    return (False, None)


def password_visibility(password: QLineEdit, checked: bool):
    if checked:
        password.setEchoMode(QLineEdit.Normal)
    else:
        password.setEchoMode(QLineEdit.Password)


def validation(login: QLineEdit, password: QLineEdit, parent_window):
    if not login.text() or not password.text():
        show_error("Поля ввода должны быть заполнеными", parent_window)
        return False
    if len(login.text()) < 4:
        show_error("Логин должен быть не менее 4 символов", parent_window)
        return False
    if len(password.text()) < 6:
        show_error("Пароль должен быть не менее 6 символов", parent_window)
        return False
    return True


def show_error(text, parent_window):
    QMessageBox.critical(parent_window, "Ошибка", text)


class Account(QDialog):
    def __init__(self):
        super().__init__()
        self.uid = 0
        self.setWindowTitle("Вход в аккаунт")
        self.resize(300, 150)

        layout = QVBoxLayout()

        self.button_login = QPushButton("Войти")
        self.button_login.clicked.connect(self.show_login)
        layout.addWidget(self.button_login)

        self.button_registration = QPushButton("Регистрация")
        self.button_registration.clicked.connect(self.show_registration)
        layout.addWidget(self.button_registration)

        self.setLayout(layout)

    def show_login(self):
        dialog = Login()
        if dialog.exec() == QDialog.Accepted:
            self.uid = dialog.get_uid()  # Login хранит uid
            self.accept()  # Закрыть Account

    def show_registration(self):
        dialog = Registration()
        if dialog.exec() == QDialog.Accepted:
            self.uid = dialog.get_uid()  # Registration хранит uid
            self.accept()

    def get_uid(self):
        return self.uid


class DataModel(QAbstractListModel):
    def __init__(self, categories, filename):
        super().__init__()
        self.filename = filename
        self.current_category = "ALL"
        self.display_data = []  # для вывода

        self.categories = {item: [] for item in categories}
        # {"salary": [], "bonus": [], "investment income": [], "gift": []}

        self.all_elements = []  # ВСЕ доходы в порядке добавления
        # [{'category': 'salary', 'income': '300', 'date': '29.03.25 21:31'}, ...]

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self.display_data)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        if role == Qt.DisplayRole:
            return self.display_data[row]
        elif role == Qt.EditRole:
            if isinstance(self.display_data[row], dict):
                return self.display_data[row]['value']
            else:  # Для ALL
                return self.display_data[row].split(': ')[1].split(' (')[0]
        return None

    def add_transaction(self, category, value, date):
        """Добавить в нужную категорию"""
        # item = {'income': income, 'date': date}
        item = {'category': category, 'value': value, 'date': date}
        self.categories[category].append(item)
        self.all_elements.append(item)

    def sum(self):
        """Сумма транзакций в категории"""
        category = self.current_category
        sum = 0
        if category == "ALL":
            for item in self.all_elements:
                sum += int(item['value'])
        else:
            for item in self.categories[category]:
                sum += int(item['value'])
        return sum

    def sum_period(self, start, end):
        """Сумма транзакций за период"""
        end = end.replace(hour=23, minute=59, second=59)

        category = self.current_category
        sum = 0
        if category == "ALL":
            for item in self.all_elements:
                value_date = datetime.strptime(item['date'], "%d.%m.%Y %H:%M")
                if start <= value_date <= end:
                    sum += int(item['value'])
        else:  # Категории
            for item in self.categories[category]:
                value_date = datetime.strptime(item['date'], "%d.%m.%Y %H:%M")
                if start <= value_date <= end:
                    sum += int(item['value'])

        return sum

    def update_display(self, category):
        """Показывает доходы ALL или категорий"""
        self.current_category = category  # для setData
        self.beginResetModel()

        if category == "ALL":
            # Создание ALL динамически
            self.display_data = [f"{item['category']}: {item['value']} ({item['date']})" for item in self.all_elements]
            # ['salary: 300 (29.03.25 21:31)', ...] - список строк
        else:
            self.display_data = [f"{item['value']} ({item['date']})" for item in self.categories[category]]
            # ['300 (29.03.25 21:31)', ...] - список строк

        self.endResetModel()

    def remove_value(self, category, index, uid):
        """Удаляет доход из указанной категории по индексу"""
        if category == "ALL":
            item = self.all_elements[index]
            global_index = index
        else:
            item = self.categories[category][index]
            # Поиск нужного элемента - индекс
            global_index = next((i for i, x in enumerate(self.all_elements)  # x - словарь
                                 if x['value'] == item['value'] and x['date'] == item['date']), None)

        if category == "ALL":  # Удаление из all_elements и  категории
            self.all_elements.pop(global_index)
            self.categories[item['category']].remove(item)
        else:  # Удаление из категории и all_incomes
            self.categories[category].pop(index)
            if global_index is not None:
                self.all_elements.pop(global_index)

        # Удаление в файле
        if global_index is not None:
            with open(self.filename, 'r', newline='', encoding='utf-8') as file:
                csv_data = list(csv.reader(file))

            uid_rows = [i for i, row in enumerate(csv_data) if row[0] == uid]
            del csv_data[uid_rows[global_index]]

            with open(self.filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(csv_data)

        self.update_display(category)

    def setData(self, index, value, role=Qt.EditRole):  # нельзя передать category
        if not index.isValid():
            return False

        row = index.row()
        category = self.current_category
        new_value = str(value)

        if category == "ALL":
            # Поменять в ALL
            item = self.all_elements[row]
            old_value = item['value']
            item['value'] = new_value

            for x in self.categories[item['category']]:  # Поменять в категории
                if x['value'] == old_value and x['date'] == item['date']:
                    x['value'] = new_value
                    break

            self.display_data[row] = f"{item['category']}: {new_value} ({item['date']})"
        else:
            # Поменять в категории
            item = self.categories[category][row]
            old_value = item['value']
            item['value'] = new_value

            for x in self.all_elements:  # Поменять в ALL
                if (x['category'] == category and
                        x['date'] == item['date'] and
                        x['value'] == old_value):
                    x['value'] = new_value
                    break

            self.display_data[row] = f"{new_value} ({item['date']})"

        self.dataChanged.emit(index, index)
        return True


class Period(QDialog):
    def __init__(self):
        super().__init__()
        layout = QFormLayout()

        self.start = QDateEdit(calendarPopup=True)
        self.start.setDisplayFormat("dd.MM.yyyy")
        self.start.setDate(QDate.currentDate().addMonths(-1))  # месяц назад

        self.end = QDateEdit(calendarPopup=True)
        self.end.setDisplayFormat("dd.MM.yyyy")
        self.end.setDate(QDate.currentDate())

        self.button = QPushButton("OK", self)
        self.button.clicked.connect(self.accept)

        layout.addRow("Начало:", self.start)
        layout.addRow("Конец:", self.end)
        layout.addRow(self.button)

        self.setLayout(layout)

    def get_dates(self):
        return (self.start.date().toString("dd.MM.yyyy"),
                self.end.date().toString("dd.MM.yyyy"))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uid = "uid_1"
        self.setWindowTitle("Учёт доходов/расходов")
        self.resize(800, 500)

        if not self.setup():
            exit()

        widget = QWidget()
        self.setCentralWidget(widget)
        main_layout = QHBoxLayout(widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(20)  # отступ между панелями

        self.incomes_panel = TransactionPanel(
            filename="users_incomes.csv",
            categories_items=["salary", "bonus", "investment income", "gift"],
            uid=self.uid,
            title="Доходы"
        )
        incomes = QFrame()
        incomes.setFrameShape(QFrame.StyledPanel)
        incomes.setLayout(QVBoxLayout())
        incomes.layout().addWidget(self.incomes_panel)
        incomes.layout().setContentsMargins(5, 5, 5, 5)

        self.expenses_panel = TransactionPanel(
            filename="users_expenses.csv",
            categories_items=["products", "household goods", "utilities payment",
                              "communication and internet", "transport", "entertainment"],
            uid=self.uid,
            title="Расходы"
        )
        expenses = QFrame()
        expenses.setFrameShape(QFrame.StyledPanel)
        expenses.setLayout(QVBoxLayout())
        expenses.layout().addWidget(self.expenses_panel)
        expenses.layout().setContentsMargins(5, 5, 5, 5)

        main_layout.addWidget(incomes)
        main_layout.addWidget(expenses)

        self.show()

    def setup(self):
        dialog = Account()
        if dialog.exec() == QDialog.Accepted:
            uid = dialog.get_uid()  # текущий аккаунт
            self.uid = f"uid_{uid}"
            return True
        else:
            QApplication.quit()
            return False


class TransactionPanel(QWidget):
    def __init__(self, filename, categories_items, uid, title):
        super().__init__()
        self.filename = filename
        self.uid = uid

        layout = QFormLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        title_label = QLabel(title)  # Заголовок
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 17px; color: orange")

        self.topics = QListWidget()
        self.topics.addItems(categories_items)
        self.topics.setSelectionMode(QListWidget.SingleSelection)
        self.topics.setFixedSize(200, 118)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Введите сумму")
        self.user_input.setFixedWidth(150)
        regex = QRegularExpression("^[1-9][0-9]{0,5}$")
        validator = QRegularExpressionValidator(regex)
        self.user_input.setValidator(validator)

        self.add_button = QPushButton("Добавить", self)
        self.add_button.clicked.connect(lambda: self.save_input(self.user_input))  # Сохранить в файл
        self.add_button.clicked.connect(self.show_selected_category)  # Обработчик: вид + сумма

        self.categories = QComboBox()
        self.categories.addItems(["ALL"] + categories_items)
        self.categories.currentIndexChanged.connect(self.show_selected_category)

        self.total_sum = QLabel("Общая сумма: 0")
        self.total_sum.setFrameStyle(QFrame.Panel)
        self.total_sum.setStyleSheet("border: 2px solid orange; border-radius: 6px;")

        self.period_button = QPushButton("Указать период для подсчёта суммы", self)
        self.period_button.setFixedSize(230, 30)
        self.period_button.clicked.connect(self.input_period)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.user_input)
        top_layout.addWidget(self.add_button)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.total_sum)
        bottom_layout.addWidget(self.period_button)

        # Layout
        layout.addRow(title_label)
        layout.addRow("Категории", self.topics)
        layout.addRow(top_layout)
        layout.addRow(self.categories)

        self.view = QListView()
        self.model = DataModel(categories_items, self.filename)
        self.view.setModel(self.model)
        layout.addRow(self.view)
        layout.addRow(bottom_layout)

        self.setLayout(layout)

        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.context_menu)

        self.load_transactions()  # 1 раз выводит в начале - файл -> модель

    def show_selected_category(self):
        """Обновлене экрана(Вида)"""
        category = self.categories.currentText()  # выбранная категория для вывода
        self.model.update_display(category)
        self.update_total_sum()  # Сумма

    def load_transactions(self):
        """Найти uid в файле и добавить доход в модель"""
        try:
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader)
                last_index = len(headers) - 1  # Индекс последнего столбца (date)

                for row in reader:
                    if row and row[0] == self.uid:  # поиск индекса != 0
                        for col_index in range(1, last_index):
                            value = row[col_index]
                            if value != "0":
                                category = headers[col_index]
                                self.model.add_transaction(category, value, row[last_index])
        except Exception as e:
            QMessageBox.critical(self, "Ошибка чтения файла", f"Не удалось добавить в модель: {str(e)}")

        self.show_selected_category()  # Показывать ALL

    def save_input(self, data):
        """Сохранить в файл и в модель"""
        topic_index = self.topics.currentRow()
        text = data.text()

        if not text or topic_index == -1:
            QMessageBox.warning(self, "Ошибка", "Введите сумму и выберите категорию")
            return

        category = self.topics.item(topic_index).text()  # Выбранная категория
        date = datetime.now().strftime('%d.%m.%Y %H:%M')
        self.model.add_transaction(category, text, date)

        try:
            with open(self.filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader)
                num_columns = len(headers)  # Количество столбцов в заголовке

                new_row = [self.uid] + [0] * (num_columns - 2) + [date]
                new_row[topic_index + 1] = text

            with open(self.filename, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(new_row)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить доход пользователя: {str(e)}")

        self.user_input.clear()  # Очистить ввод

    def input_period(self):
        category = self.categories.currentText()
        dialog = Period()
        dialog.setWindowTitle(f"Категория {category}")

        if dialog.exec() == QDialog.Accepted:
            start_str, end_str = dialog.get_dates()
            start = datetime.strptime(start_str, "%d.%m.%Y")
            end = datetime.strptime(end_str, "%d.%m.%Y")

            if start > end:
                QMessageBox.warning(self, "Ошибка", "Начальная дата позже конечной")
                return

            total = self.model.sum_period(start, end)
            QMessageBox.information(self, "Результат", f"Сумма: {total}")

    def update_total_sum(self):
        total = self.model.sum()
        self.total_sum.setText(f"Общая сумма: {total}")

    def context_menu(self, position):
        """Правая кнопка мыши"""
        index = self.view.currentIndex()
        if not index.isValid():
            return

        menu = QMenu(self)
        remove_action = QAction("Удалить", self)
        edit_action = QAction("Изменить", self)

        category = self.categories.currentText()
        remove_action.triggered.connect(lambda: self.model.remove_value(category, index.row(), self.uid))
        edit_action.triggered.connect(lambda: self.edit_value(category, index.row(), self.uid))

        menu.addAction(remove_action)
        menu.addAction(edit_action)
        menu.exec(self.view.viewport().mapToGlobal(position))

        self.update_total_sum()  # Сумма - после изменения, удаления

    def edit_value(self, category, index, uid):
        model_index = self.model.index(index)
        old_text = self.model.data(model_index, Qt.DisplayRole)

        # без даты
        if category == "ALL":
            old_value = old_text.split(': ')[1].split(' (')[0]
        else:
            old_value = old_text.split(' (')[0]

        new_value, ok = QInputDialog.getText(
            self, "Изменение", "Введите новую сумму", QLineEdit.Normal, old_value
        )

        if ok and new_value:
            regex = QRegularExpression("^[1-9][0-9]{0,5}$")
            if not regex.match(new_value).hasMatch():
                QMessageBox.warning(self, "Ошибка", "Введите значение больше нуля")
                return

            self.model.setData(model_index, new_value)
            self.edit_income_in_file(category, old_text, old_value, new_value, uid)

    def edit_income_in_file(self, category, old_text, old_value, new_value, uid):
        with open(self.filename, 'r', newline='', encoding='utf-8') as file:
            csv_data = list(csv.reader(file))
            headers = csv_data[0]
            last_index = len(headers) - 1

        # определить столбец - категория
        if category == "ALL":
            selected_category = old_text.split(":")[0]
        else:  # для категорий - другой текст
            selected_category = category

        index = 0
        for i in csv_data[0]:  # только заголовки
            if i == selected_category:
                break
            index += 1

        date = old_text.split("(")[1].rstrip(")")
        for row in csv_data:  # поиск нужной строки
            if row[0] == uid and row[last_index] == date and row[index] == old_value:  # нужный uid, дата и значение
                row[index] = new_value  # новое значение
                break

        with open(self.filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(csv_data)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec()
