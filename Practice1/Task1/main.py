import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setWindowTitle("Window")
        self.setGeometry(400, 100, 500, 500)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)

        # Метка
        label1 = QLabel("!!!Label!!!Label!!!Label!!!Label!!!Label!!!Label!!!Label!!!Label!!!Label!!!Label!!!"
                       "!!!Label!!!Label!!!Label!!!Label!!!Label!!!Label!!!Label!!!Label!!!Label!!!Label!!!"
                       "!!!Label!!!Label!!!Label!!!Label!!!Label!!!Label!!!Label!!!Label!!!Label!!!Label!!!")
        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label1.setWordWrap(True)
        font1 = QFont("Arial", 14, italic=True)
        label1.setFont(font1)

        label2 = QLabel("(second!!!second)")
        label2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        font2 = QFont("Arial", 28)
        label2.setFont(font2)

        label3 = QLabel(self)
        image = QPixmap("cat.png")
        label3.setPixmap(image.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))

        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

        label2.move(0, 200)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
