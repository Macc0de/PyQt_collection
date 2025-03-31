from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QSplineSeries
from PySide6.QtGui import QPainter
import numpy as np


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Графики")

        arr_x = np.linspace(0, 2 * np.pi, 30)  # 30 точек
        sin_y = np.sin(arr_x)
        cos_y = np.cos(arr_x)

        chart = QChart()
        chart.addSeries(self.create_series(arr_x, sin_y, "Sin(x)", "red"))  # серия данных
        chart.addSeries(self.create_series(arr_x, cos_y, "Cos(x)", "blue"))
        chart.createDefaultAxes()

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        layout.addWidget(chart_view)
        widget.setLayout(layout)

    def create_series(self, x, y, name, color):
        series = QSplineSeries()

        series.setName(name)
        series.setColor(color)
        for i in range(len(x)):
            series.append(x[i], y[i])  # точка

        return series


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.resize(440, 300)
    window.show()
    app.exec()
