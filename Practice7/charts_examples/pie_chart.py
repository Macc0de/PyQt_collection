from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCharts import QChart, QChartView, QPieSeries


class TestChart(QMainWindow):

    def __init__(self):
        super().__init__()

        self.series = QPieSeries()

        self.series.append('Jane', 1)
        self.series.append('Joe', 2)
        self.series.append('Andy', 3)
        self.series.append('Barbara', 4)
        self.series.append('Axel', 5)

        self.slice = self.series.slices()[1]
        self.slice.setExploded()
        self.slice.setLabelVisible()
        self.slice.setPen(QPen(Qt.darkGreen, 2))
        self.slice.setBrush(Qt.green)

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle('Simple piechart example')
        self.chart.legend().hide()

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(self._chart_view)


if __name__ == "__main__":
    app = QApplication([])

    window = TestChart()
    window.show()
    window.resize(440, 300)

    app.exec()