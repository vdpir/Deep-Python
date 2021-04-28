import functools
import json
import csv

import os

def get_car_list(csv_filename):
    car_list = []

    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            print(row)
            try:
                if (len(row) < 4) or \
                        (os.path.splitext(row[3])[1] not in [".jpg", ".jpeg", ".png", ".gif"]) or \
                        row[0] == '' or row[1] == '' or row[3] == '' or row[5] == '':
                    continue

                if row[0] == 'car' and row[2] != '':
                        car_list.append(Car(row[1], row[3], row[5], row[2]))
                elif row[0] == 'truck':
                    car_list.append(Truck(row[1], row[3], row[5], row[4]))
                elif row[0] == 'spec_machine' and row[6] != '':
                    car_list.append(SpecMachine(row[1], row[3], row[5], row[6]))
            except Exception:
                continue

    return car_list

class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.carrying = float(carrying)
        self.photo_file_name = photo_file_name

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]

class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        self.car_type = 'car'
        self.passenger_seats_count = int(passenger_seats_count)
        super().__init__(brand, photo_file_name, carrying)


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        self.car_type = 'truck'
        super().__init__(brand, photo_file_name, carrying)

        if body_whl == '':
            self.body_height = self.body_width = self.body_length = 0.
            return

        try:
            bl, bw, bh = body_whl.split('x')
            self.body_length = float(bl.strip())
            self.body_width = float(bw.strip())
            self.body_height = float(bh.strip())
        except:
            self.body_height = self.body_width = self.body_length = 0.

    def get_body_volume(self):
        return self.body_height * self.body_width * self.body_length

class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra
        self.car_type = 'spec_machine'

