from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PySide6.QtCharts import QChart, QChartView, QScatterSeries, QBarSeries, QBarSet
from PySide6.QtGui import QPainter, Qt
import csv


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Деревья")

        csv_data = self.read_csv()
        # {1: {'Girth': 8.3, 'Height': 70.0, 'Volume': 10.3},...}

        tab_widget = QTabWidget()
        scatter_tab = QWidget()
        scatter_layout = QVBoxLayout()

        # Точечная диаграмма
        scatter_chart = self.scatter_chart(csv_data)
        scatter_chart_view = QChartView(scatter_chart)  # Вид
        scatter_chart_view.setRenderHint(QPainter.Antialiasing)

        scatter_layout.addWidget(scatter_chart_view)
        scatter_tab.setLayout(scatter_layout)

        bar_tab = QWidget()
        bar_layout = QVBoxLayout()

        # Столбчатая
        bar_chart = self.bar_chart(csv_data)
        bar_chart_view = QChartView(bar_chart)  # Вид
        bar_chart_view.setRenderHint(QPainter.Antialiasing)

        bar_layout.addWidget(bar_chart_view)
        bar_tab.setLayout(bar_layout)

        tab_widget.addTab(scatter_tab, "Точечная диаграмма")
        tab_widget.addTab(bar_tab, "Столбчатая диаграмма")
        self.setCentralWidget(tab_widget)

    def scatter_chart(self, csv_data):
        chart = QChart()
        scatter_series = QScatterSeries()
        scatter_series.setName("Точечная диаграмма")
        scatter_series.setMarkerSize(10)

        for tree_id, tree_data in csv_data.items():
            girth = tree_data['Girth']
            height = tree_data['Height']
            scatter_series.append(girth, height)  # точка

        chart.addSeries(scatter_series)
        chart.createDefaultAxes()
        chart.axes(Qt.Horizontal)[0].setTitleText("Girth")
        chart.axes(Qt.Vertical)[0].setTitleText("Height")

        return chart

    def bar_chart(self, csv_data):
        chart = QChart()
        bar_series = QBarSeries()

        bar_set = QBarSet("Столбчатая диаграмма")
        for tree_id, tree_data in csv_data.items():
            volume = tree_data['Volume']
            bar_set.append(volume)

        bar_series.append(bar_set)
        chart.addSeries(bar_series)

        chart.createDefaultAxes()
        chart.axes(Qt.Horizontal)[0].setTitleText("Tree ID")
        chart.axes(Qt.Vertical)[0].setTitleText("Volume")

        return chart

    def read_csv(self):
        csv_data = {}
        with open("trees.csv", 'r', encoding="utf-8") as file:
            data = csv.reader(file, delimiter=',')
            if not data:
                print("Файл пустой!")
                exit()

            next(data)
            for row in data:
                if row:
                    tree_id = int(row[0])
                    csv_data[tree_id] = {
                        'Girth': float(row[1]),
                        'Height': float(row[2]),
                        'Volume': float(row[3])
                    }
        return csv_data


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
