import os
import csv
import re


# from test import get_photo_file_ext


class CarBase:
    base_car_type = 0
    base_brand = 1
    base_passenger_seats_count = 2
    base_photo_file_name = 3
    base_body_whl = 4
    base_carrying = 5
    base_extra = 6

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        _, file_ext = os.path.splitext(self.photo_file_name)
        return file_ext


class Car(CarBase):
    car_type = "car"

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)

    @classmethod
    def make_obj_from_cvs(cls, row):
        return cls(
            row[cls.base_brand],
            row[cls.base_photo_file_name],
            row[cls.base_carrying],
            row[cls.base_passenger_seats_count],
        )


class Truck(CarBase):
    car_type = "truck"

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        try:
            length, width, height = (float(i) for i in body_whl.split('x', 2))
        except ValueError:
            length, width, height = .0, .0, .0

        self.body_length = length
        self.body_width = width
        self.body_height = height

    def get_body_volume(self):
        return self.body_height * self.body_length * self.body_width

    @classmethod
    def make_obj_from_cvs(cls, row):
        return cls(
            row[cls.base_brand],
            row[cls.base_photo_file_name],
            row[cls.base_carrying],
            row[cls.base_body_whl],
        )


class SpecMachine(CarBase):
    car_type = "spec_machine"

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra

    @classmethod
    def make_obj_from_cvs(cls, row):
        return cls(
            row[cls.base_brand],
            row[cls.base_photo_file_name],
            row[cls.base_carrying],
            row[cls.base_extra],
        )


def get_file_ext(a):
    _, file_ext = os.path.splitext(a)
    return file_ext


def get_car_list(csv_filename):
    with open(csv_filename) as csv_fd:
        # создаем объект csv.reader для чтения csv-файла
        reader = csv.reader(csv_fd, delimiter=';')

        # пропускаем заголовок csv
        next(reader)

        # это наш список, который будем возвращать
        car_list = []

        # объявим словарь, ключи которого - тип автомобиля (car_type),
        # а значения - класс, объект которого будем создавать
        create_strategy = {car_class.car_type: car_class
                           for car_class in (Car, Truck, SpecMachine)}

        # обрабатываем csv-файл построчно
        for row in reader:
            try:
                # определяем тип автомобиля
                car_type = row[0]
            except IndexError:
                # если не хватает колонок в csv - игнорируем строку
                continue

            try:
                # получаем класс, объект которого нужно создать
                # и добавить в итоговый список car_list
                car_class = create_strategy[car_type]
            except KeyError:
                # если car_type не извесен, просто игнорируем csv-строку
                continue

            ext = get_file_ext(row[3])
            # var = re.search(r'[^\W\d]', row[0])
            if (ext == ".png" or ext == ".gif" or ext == ".jpg" or ext == ".jpeg") and row[1]:
                if car_type == "car":
                    if not row[2]:
                        continue
                elif car_type == "spec_machine":
                    if not row[6]:
                        continue
                try:
                    # создаем и добавляем объект в car_list
                    car_list.append(car_class.make_obj_from_cvs(row))
                except (ValueError, IndexError):
                    # if len(car_list) > 0:
                    #   car_list.pop()
                    pass

    return car_list
