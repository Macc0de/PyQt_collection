import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from book import Book


class Widget(QWidget):
    def __init__(self, book):
        super().__init__()
        self.book = book
        self.setup()

    def setup(self):
        layout = QVBoxLayout()

        text = QLabel(self.book.get_info())
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(text)

        cover = QLabel()
        pixmap = QPixmap(self.book.path)
        cover.setPixmap(pixmap)
        cover.setScaledContents(True)
        cover.setFixedSize(200, 300)
        cover.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(cover, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setWindowTitle("Books")
        self.setGeometry(400, 100, 500, 500)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        widget = QWidget()
        layout = QVBoxLayout()

        books = [
            Book("The Great Gatsby", "F. Scott Fitzgerald", 180, "covers/gatsby.jpg"),
            Book("The Hobbit", "J.R.R. Tolkien", 310, "covers/hobbit.jpg"),
            Book("The Dark Tower", "Stephen King", 4250, "covers/tower.jpg")
        ]

        for book in books:
            layout.addWidget(Widget(book))

        widget.setLayout(layout)
        scroll_area.setWidget(widget)

        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
