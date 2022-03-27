"""В этом задании вам нужно создать интерфейс для работы с файлами. Интерфейс должен предоставлять следующие возможности
по работе с файлами:
- чтение из файла, метод read возвращает строку с текущим содержанием файла
- запись в файл, метод write принимает в качестве аргумента строку с новым содержанием файла
- сложение объектов типа file, результатом сложения является объект класса file, при этом создается новый файл и
файловый объект, в котором содержимое второго файла добавляется к содержимому первого файла. Новый файл должен
создаваться в директории, полученной с помощью функции tempfile.gettempdir. Для получения нового пути можно
использовать os.path.join.
- возвращать в качестве строкового представления объекта класса file полный путь до файла
- поддерживать протокол итерации, причем итерация проходит по строкам файла
При создании экземпляра класса file в конструктор передается полный путь до файла на файловой системе. Если файла с
таким путем не существует, он должен быть создан при инициализации.
Пример работы: (Тест в другом модуле)
from solution import file
import os.path
path_to_file = 'asd'
print(os.path.exists(path_to_file))  # False
file_obj = file(path_to_file)
os.path.exists(path_to_file)  # True
print(file_obj)  # 'asd.txt'
print(file_obj.read())  # ''
file_obj.write('some text')
print(file_obj.read())  # 'some text'
file_obj.write('other text')
print(file_obj.read())  # 'other text'
file_obj_1 = file(path_to_file + '_1')
file_obj_2 = file(path_to_file + '_2')
file_obj_1.write('line 1\n')
file_obj_2.write('line 2\n')
new_file_obj = file_obj_1 + file_obj_2
print(isinstance(new_file_obj, file))  # True
print(new_file_obj)
# C:\Users\Alexandr\AppData\Local\Temp\299f1c21207044cdae0c754dc4a76c59
for line in new_file_obj:
    print(ascii(line))
# 'line 1\n'
# 'line 2\n'
new_path_to_file = str(new_file_obj)
print(os.path.exists(new_path_to_file))  # True
file_obj_3 = file(new_path_to_file)
print(file_obj_3)
# C:\Users\Alexandr\AppData\Local\Temp\299f1c21207044cdae0c754dc4a76c59
for line in new_file_obj:
    print(ascii(line))
# 'line 1\n'
# 'line 2\n'
"""

from os import path
from tempfile import gettempdir
import uuid


class File:
    """Класс file работает с файлами"""

    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.i = 0
        if not path.exists(path_to_file):
            with open(path_to_file, "w") as f:
                f.write('')

    def __str__(self):
        return path.join(self.path_to_file)

    def __add__(self, obj):
        new_path = path.join(gettempdir(), str(uuid.uuid4().hex))
        new_file = type(self)(new_path)
        new_file.write(self.read() + obj.read())
        return new_file

    def read(self):
        with open(self.path_to_file, "r") as f:
            return f.read()

    def write(self, new_str):
        with open(self.path_to_file, "w") as f:
            f.write(new_str)

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path_to_file, "r") as f:
            self.i += 1
            try:
                return f.readlines()[self.i - 1]
            except IndexError:
                self.i = 0
                raise StopIteration

#######################################################################################################################
# Решение от преподавателей
#######################################################################################################################
# В этом задании нужно было аккуратно реализовать несколько классических магических методов и пару обычных. При
# инициализации мы сохраняем путь, а также можем проверить существование файла, хотя это и не требовалось при
# тестировании. Методы write и read просто работают с файлом в системе. Хотя наличие метода для чтения не требовалось,
# его реализация помогает нам в работе других функций, да и вообще — какой write без read.
# Метод __str__ вряд ли вызвал у вас проблемы, остальные методы более интересны. При сложении файлов на нас ложится
# задача выбора имени нового файла. В условии про именование ничего не сказано, и в реальных задачах почти всегда над
# такими деталями приходится думать самостоятельно. В примере мы генерим имя с помощью модуля uuid, который позволяет
# создавать идентификаторы UUID. Файл мы сохраняем в той же директории, что и существующий, что помогает избежать
# проблем с правами (можно использовать gettempdir как в условии).
# При итерации главным вопросом является сохранение номера прочитанной строки. Самым простым вариантом было бы просто
# вернуть итератор строк, например, с помощью метода readlines. Однако, в таком случае мы читаем сразу весь файл,
# который может быть очень большим и который весь нам может быть и не нужен. В нашем решении мы сохраняем текущую
# позицию в файле с помощью метода tell и используем readline для получения единственной следующей строки. По окончании
# чтения файла метод выбрасывает StopIteration, как каждый уважающий себя итератор. Можно было также использовать то,
# что файловый объект в Python сам по себе является итератором.

# import os
# import uuid
#
#
# class File:
#     def __init__(self, path):
#         self.path = path
#         self.current_position = 0
#
#         if not os.path.exists(self.path):
#             open(self.path, 'w').close()
#
#     def write(self, content):
#         with open(self.path, 'w') as f:
#             return f.write(content)
#
#     def read(self):
#         with open(self.path, 'r') as f:
#             return f.read()
#
#     def __add__(self, obj):
#         new_path = os.path.join(
#             os.path.dirname(self.path),
#             str(uuid.uuid4().hex)
#         )
#         new_file = type(self)(new_path)
#         new_file.write(self.read() + obj.read())
#
#         return new_file
#
#     def __str__(self):
#         return self.path
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         with open(self.path, 'r') as f:
#             f.seek(self.current_position)
#
#             line = f.readline()
#             if not line:
#                 self.current_position = 0
#                 raise StopIteration('EOF')
#
#             self.current_position = f.tell()
#             return line
