from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtGui import QPainter, QColor
import csv


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ураганы")

        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        csv_data = self.read_csv()

        self.pie_2007(csv_data)
        self.pie_chart_by_year(csv_data)

    def pie_2007(self, csv_data):
        hurricanes = []
        valid_months = []

        for month, hurricanes_data in csv_data.items():
            value = hurricanes_data[2]  # 2007 год
            if value > 0:
                hurricanes.append(value)
                valid_months.append(month)

        if hurricanes:
            max_hurricanes = max(hurricanes)
            max_month = valid_months[hurricanes.index(max_hurricanes)]

            series = QPieSeries()
            total_hurricanes = sum(hurricanes)  # Общее количество ураганов за 2007 год

            for month, count in zip(valid_months, hurricanes):  # zip - пара
                slice_ = series.append(month, count)
                slice_.setLabelVisible(True)
                percentage = (count / total_hurricanes) * 100
                slice_.setLabel(f"{month}: {percentage:.1f}%")
                if month == max_month:
                    slice_.setBrush(QColor("red"))
                    slice_.setExploded(True)

            chart = QChart()
            chart.addSeries(series)
            chart.setTitle("Количество ураганов по месяцам за 2007 год")

            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.Antialiasing)

            chart_widget = QWidget()
            layout = QVBoxLayout(chart_widget)
            layout.addWidget(chart_view)
            self.tabs.addTab(chart_widget, "Ураганы 2007 года")
        else:
            print("Нет данных об ураганах за 2007 год")

    def pie_chart_by_year(self, csv_data):
        years = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
        hurricanes_by_year = {year: 0 for year in years}

        for id_year, year in enumerate(years):
            for hurricane in csv_data.values():
                hurricanes_by_year[year] += hurricane[id_year]

        hurricanes = list(hurricanes_by_year.values())
        valid_years = list(hurricanes_by_year.keys())

        # Минимальное количество ураганов
        min_hurricanes = min(hurricanes)
        # min_years = [year for year, count in zip(valid_years, hurricanes) if count == min_hurricanes]
        min_years = []
        for year, count in zip(valid_years, hurricanes):
            if count == min_hurricanes:
                min_years.append(year)

        series = QPieSeries()
        total_hurricanes = sum(hurricanes)  # Общее количество ураганов

        for year, count in zip(valid_years, hurricanes):
            slice_ = series.append(str(year), count)
            slice_.setLabelVisible(True)
            percentage = (count / total_hurricanes) * 100
            slice_.setLabel(f"{year}: {percentage:.1f}%")

            if year in min_years:  # Если год в списке минимальных
                slice_.setBrush(QColor("red"))
                slice_.setExploded(True)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Количество ураганов по годам")

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        chart_widget = QWidget()
        layout = QVBoxLayout(chart_widget)
        layout.addWidget(chart_view)
        self.tabs.addTab(chart_widget, "Ураганы по годам")

    def read_csv(self):
        csv_data = {}
        with open("hurricanes.csv", 'r', encoding="utf-8") as file:
            data = csv.reader(file, delimiter=',')
            next(data)
            for row in data:
                if row:
                    month = row[0]
                    hurricanes_per_month = list(map(int, row[2:]))
                    csv_data[month] = hurricanes_per_month
        return csv_data


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
