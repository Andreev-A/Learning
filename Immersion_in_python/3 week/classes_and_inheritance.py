"""Классы и наследование
Как правило задачи про классы не носят вычислительный характер. Обычно нужно написать классы, которые отвечают
определенным интерфейсам. Насколько удобны эти интерфейсы и как сильно связаны классы между собой, определит легкость
их использования в будущих программах.
Предположим есть данные о разных автомобилях и спецтехнике. Данные представлены в виде таблицы с характеристиками. Вся
техника разделена на три вида: спецтехника, легковые и грузовые автомобили. Обратите внимание на то, что некоторые
характеристики присущи только определенному виду техники. Например, у легковых автомобилей есть характеристика «кол-во
пассажирских мест», а у грузовых автомобилей — габариты кузова: «длина», «ширина» и «высота».
Вам необходимо создать свою иерархию классов для данных, которые описаны в таблице. Классы должны называться CarBase
(базовый класс для всех типов машин), Car (легковые автомобили), Truck (грузовые автомобили) и SpecMachine
(спецтехника). Все объекты имеют обязательные атрибуты:
- car_type, значение типа объекта и может принимать одно из значений: «car», «truck», «spec_machine».
- photo_file_name, имя файла с изображением машины, допустимы названия файлов изображений с расширением из списка:
«.jpg», «.jpeg», «.png», «.gif»
- brand, марка производителя машины
- carrying, грузоподъемность
В базовом классе CarBase нужно реализовать метод get_photo_file_ext для получения расширения файла изображения.
Расширение файла можно получить при помощи os.path.splitext.
Для грузового автомобиля необходимо в конструкторе класса определить атрибуты: body_length, body_width, body_height,
отвечающие соответственно за габариты кузова — длину, ширину и высоту. Габариты передаются в параметре body_lwh
строка, в которой размеры разделены латинской буквой «x»). Обратите внимание на то, что характеристики кузова должны
быть вещественными числами и характеристики кузова могут быть не валидными (например, пустая строка). В таком случае
всем атрибутам, отвечающим за габариты кузова, присваивается значение равное нулю.
Также для класса грузового автомобиля необходимо реализовать метод get_body_volume, возвращающий объем кузова.
В классе Car должен быть определен атрибут passenger_seats_count (количество пассажирских мест), а в классе
SpecMachine — extra (дополнительное описание машины).
Обратите внимание, что у каждого объекта из иерархии должен быть свой набор атрибутов и методов. Например, у класса
легковой автомобиль не должно быть метода get_body_volume в отличие от класса грузового автомобиля. Имена атрибутов и
методов должны совпадать с теми, что описаны выше.
Далее вам необходимо реализовать функцию get_car_list, на вход которой подается имя файла в формате csv. Файл содержит
данные, аналогичные строкам из таблицы. Вам необходимо прочитать этот файл построчно при помощи модуля стандартной
библиотеки csv. Затем проанализировать строки на валидность и создать список объектов с автомобилями и специальной
техникой. Функция должна возвращать список объектов.
Первая строка в исходном файле — это заголовок csv, который содержит имена колонок. Нужно пропустить первую строку из
исходного файла. Обратите внимание на то, что в некоторых строках исходного файла , данные могут быть заполнены
некорректно, например, отсутствовать обязательные поля или иметь не валидное значение. В таком случае нужно
проигнорировать подобные строки и не создавать объекты. Строки с пустым или не валидным значением для body_lwh
игнорироваться не должны.  Вы можете использовать стандартный механизм обработки исключений в процессе чтения,
валидации и создания объектов из строк csv-файла.
Несколько примеров работы:
# >>> from solution import *
# >>> car = Car('Bugatti Veyron', 'bugatti.png', '0.312', '2')
# >>> print(car.car_type, car.brand, car.photo_file_name, car.carrying,
# ... car.passenger_seats_count, sep='\n')
car
Bugatti Veyron
bugatti.png
0.312
2
# >>> truck = Truck('Nissan', 'nissan.jpeg', '1.5', '3.92x2.09x1.87')
# >>> print(truck.car_type, truck.brand, truck.photo_file_name, truck.body_length,
# ... truck.body_width, truck.body_height, sep='\n')
truck
Nissan
nissan.jpeg
3.92
2.09
1.87
# >>> spec_machine = SpecMachine('Komatsu-D355', 'd355.jpg', '93', 'pipelayer specs')
# >>> print(spec_machine.car_type, spec_machine.brand, spec_machine.carrying,
# ... spec_machine.photo_file_name, spec_machine.extra, sep='\n')
spec_machine
Komatsu-D355
93.0
d355.jpg
pipelayer specs
# >>> spec_machine.get_photo_file_ext()
'.jpg'
# >>> cars = get_car_list('cars_week3.csv')
# >>> len(cars)
4
# >>> for car in cars:
# ...     print(type(car))
# ...
<class 'solution.Car'>
<class 'solution.Truck'>
<class 'solution.Truck'>
<class 'solution.Car'>
# >>> cars[0].passenger_seats_count
4
# >>> cars[1].get_body_volume()
60.0
# >>>
"""
import os
import csv


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying,
                 passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'car'
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'truck'
        try:
            self.body_length = float(body_whl.split('x')[0].strip())
            self.body_width = float(body_whl.split('x')[1].strip())
            self.body_height = float(body_whl.split('x')[2].strip())
            if len(body_whl.split('x')) > 3:
                raise ValueError
        except ValueError:
            self.body_length = self.body_width = self.body_height = float(0)

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'spec_machine'
        self.extra = extra


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            try:
                if row[1] and (os.path.splitext(row[3])[1] in
                               ['.jpg', '.jpeg', '.png', '.gif']) and row[5]:
                    if row[0] == 'car' and row[2].isdigit():
                        car_list.append(Car(row[1], row[3], row[5], row[2]))
                    if row[0] == 'truck':
                        car_list.append(Truck(row[1], row[3], row[5], row[4]))
                    if row[0] == 'spec_machine' and row[6]:
                        car_list.append(SpecMachine(row[1], row[3], row[5], row[6]))
            except IndexError:
                pass
    return car_list

######################################################################################################################
# Решение от преподавателей задания про классы и наследование
######################################################################################################################
# import csv
# import os.path
#
#
# class CarBase():
#     """базовый класс для транспортных средств"""
#
#     # атрибут для хранения обязательных параметров класса, описывающего транспортное средство
#     required = []
#
#     def __init__(self, brand, photo_file_name, carrying):
#         self.brand = self.validate_input(brand)
#         self.photo_file_name = self.validate_photo_filename(photo_file_name)
#         self.carrying = float(self.validate_input(carrying))
#
#     def validate_input(self, value):
#         """метод валидации данных, возвращает значение, если оно валидно,
#         иначе выбрасывает исключение ValueError"""
#         if value == '':
#             raise ValueError
#         return value
#
#     def validate_photo_filename(self, filename):
#         for ext in ('.jpg', '.jpeg', '.png', '.gif'):
#             if filename.endswith(ext) and len(filename) > len(ext):
#                 return filename
#         raise ValueError
#
#     def get_photo_file_ext(self):
#         _, ext = os.path.splitext(self.photo_file_name)
#         return ext
#
#     @classmethod
#     def create_from_dict(cls, data):
#         """создает экземпляр класса из словаря с параметрами"""
#         parameters = [data[parameter] for parameter in cls.required]
#         return cls(*parameters)
#
#
# class Car(CarBase):
#     """класс описывающий автомобили для перевозок людей"""
#     car_type = "car"
#     required = ['brand', 'photo_file_name', 'carrying', 'passenger_seats_count']
#
#     def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
#         super().__init__(brand, photo_file_name, carrying)
#         self.passenger_seats_count = int(self.validate_input(passenger_seats_count))
#
#
# class Truck(CarBase):
#     """класс описывающий автомобили для перевозок грузов"""
#     car_type = "truck"
#     required = ['brand', 'photo_file_name', 'carrying', 'body_whl']
#
#     def __init__(self, brand, photo_file_name, carrying, body_whl):
#         super().__init__(brand, photo_file_name, carrying)
#         self.body_length, self.body_width, self.body_height = self.parse_whl(body_whl)
#
#     def get_body_volume(self):
#         """возвращает объем кузова"""
#         return self.body_length * self.body_width * self.body_height
#
#     def parse_whl(self, body_whl):
#         """возвращает реальные размеры кузова length, width, height"""
#         try:
#             length, width, height = (float(c) for c in body_whl.split("x", 2))
#         except Exception:
#             length, width, height = 0.0, 0.0, 0.0
#         return length, width, height
#
#
# class SpecMachine(CarBase):
#     """класс описывающий спецтехнику"""
#
#     car_type = "spec_machine"
#     required = ['brand', 'photo_file_name', 'carrying', 'extra']
#
#     def __init__(self, brand, photo_file_name, carrying, extra):
#         super().__init__(brand, photo_file_name, carrying)
#         self.extra = self.validate_input(extra)
#
#
# def get_car_list(csv_filename):
#     """возвращает список объектов, сохраненных в файле csv_filename"""
#
#     car_types = {'car': Car, 'spec_machine': SpecMachine, 'truck': Truck}
#     csv.register_dialect('cars', delimiter=';')
#     car_list = []
#
#     with open(csv_filename, 'r') as file:
#         reader = csv.DictReader(file, dialect='cars')
#         for row in reader:
#             try:
#                 car_class = car_types[row['car_type']]
#                 car_list.append(car_class.create_from_dict(row))
#             except Exception:
#                 pass
#
#     return car_list
#
#
# if __name__ == '__main__':
#     pass
