# Потому что словарь - неупорядоченная коллекция данных, как и множество. Но начиная с версии python 3.6 - порядок
# добавления ключей в словарь сохраняется, а с 3.7 даже гарантируется -
# https://docs.python.org/3/library/stdtypes.html#dict-views а вообще, если нужен упорядоченный словарь - то есть
# collections.OrderedDict - https://docs.python.org/3/library/collections.html#collections.OrderedDict

#  словарь создание   ##################################################################################################

# dict_sample = {}  # пустой словарь
# dict_sample = {1: 'mango', 2: 'pawpaw'}  # ключи являются целыми числами
# dict_sample = {'fruit': 'mango', 1: [4, 6, 8]}  # с ключами разных типов (только неизменяемые объекты)
# dict_sample = dict({1:'mango', 2:'pawpaw'})  # явно вызвав метод dict()
# с помощью последовательности: dict_sample = dict([(1,'mango'), (2,'pawpaw')])
#   dict_sample = {  # могут быть вложенными
#   1: {'student1': 'Nicholas', 'student2': 'John', 'student3': 'Mercy'},
#   2: {'course1': 'Computer Science', 'course2': 'Mathematics', 'course3': 'Accounting'}
#   }
# x = dict.copy()  # создание копии словаря (изменения в скопированном словаре не затрагивают оригинальный словарь)
#   dict_sample.fromkeys(keys, value)  # с указанными ключами и значениями
#   keys = ('1, 2, 3')
#   value = 25  # (если одинаковое значение), если value нет - то None
# {v: k for k, v in a.items()}  # поменять местами ключи и значения в словаре
# letters_in_binary = dict({map(str, input().split(':')) for i in range(x)})  # с клавиатуры парами
# = dict({map(str, input().split(': ')[::-1]) for _ in range(number_of_letters)})  # поменять значения

#  словарь доступ  #####################################################################################################

# x = dict_sample["model"]  # нужно передать ключ в квадратных скобках [] (выдаст ошибку при отсутствии такого ключа)
# x = dict_sample.get("model")  # функция get() (нет ошибки при отсутствии ключа)
# x = dict_sample.get('model', 'return')  # нет ключа - вернет значение 'return'
# x = dict_sample.setdefault('model', 'return')  # нет ключа - запишет ключ 'model' и значение 'return' в словарь

#  словарь вывод  ######################################################################################################

#   for key, value in notes.items():  # ключ : значение
#       print(key, ':', value)
#   for key in notes.keys():  # ключ
#       print(key)
#   for value in notes.values():  # значение
#       print(value)
#   def get_key(d, value):  # вывод ключа по значению
#       for k, v in d.items():
#           if v == value:
#               return k
# print(str(len(dots))+'\n'+' '.join(map(str, dots)))  # печать в двух строках
# print(" ".join(map(str, a)))  # вывод массива целых чисел с пробелами
# print('Выйграл игрок номер {}'.format(user_number))

# словарь удаление  ####################################################################################################

# del dict_sample['year']  # удаление элемента
# dict_sample.pop('year')  # с конкретным ключом
# dict_sample.popitem()  # удаляет последний элемент в словаре
# dict_sample.clear()  # удаляет все элементы словаря
# del dict_sample  # удаление всего словаря