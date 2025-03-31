from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (QMainWindow, QApplication)
from PySide6.QtCharts import (QBarCategoryAxis, QBarSet, QChart, QChartView,
                              QPercentBarSeries)
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        series = QPercentBarSeries()
        df = pd.read_csv("biostats.csv")
        for i in range(7):
            set = QBarSet(df.iloc[i]['Name'])
            set.append(df.iloc[i, 3:].values.flatten().tolist())
            series.append(set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Simple percentbarchart example")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = df.columns[3:]
        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.addAxis(axis, Qt.AlignBottom)
        series.attachAxis(axis)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chart_view)


if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.resize(420, 300)
    w.show()
    app.exec()