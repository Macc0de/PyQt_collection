from datetime import datetime


class Train:
    def __init__(self, name, start_time, arrival_time):
        if not isinstance(name, str) or name == "":
            raise AttributeError("name должен быть непустой строкой")
        self.__name = name
        self.__start_time = datetime.strptime(start_time, "%d/%m/%y %H:%M")
        self.__arrival_time = datetime.strptime(arrival_time, "%d/%m/%y %H:%M")
        if self.__start_time >= self.__arrival_time:
            raise AttributeError("Время отправления не может быть раньше времени прибытия")

    def travel_time(self):
        return self.__arrival_time - self.__start_time

    def travel_time_in_hours(self):
        return self.travel_time().total_seconds() / 3600

    def name(self):
        return self.__name

    def start_time(self):
        return str(self.__start_time)

    def arrival_time(self):
        return str(self.__arrival_time)

    def __str__(self):
        return f'Поезд {self.__name} отправляется в {self.__start_time} и прибывает в {self.__arrival_time}'
