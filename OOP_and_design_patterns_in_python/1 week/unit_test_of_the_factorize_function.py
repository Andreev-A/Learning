"""Задача по созданию модульного теста функции factorize
Дана функция factorize(x) со следующим контрактом:

# def factorize(x):
#     '''
#     Factorize positive integer and return its factors.
#     :type x: int,>=0
#     :rtype: tuple[N],N>0
#    '''
#     pass

Необходимо написать комплект тестов используя модуль unittest стандартной библиотеки Python. Имя тестового
класса - TestFactorize.
Описание тестов:
1. test_wrong_types_raise_exception - проверяет, что передаваемый в функцию аргумент типа float или str вызывает
исключение TypeError. Тестовый набор входных данных:  'string',  1.5
2. test_negative - проверяет, что передача в функцию factorize отрицательного числа вызывает исключение ValueError.
Тестовый набор входных данных:   -1,  -10,  -100
3. test_zero_and_one_cases - проверяет, что при передаче в функцию целых чисел 0 и 1, возвращаются соответственно
кортежи (0,) и (1,). Набор тестовых данных: 0 → (0, ),  1 → (1, )
4. test_simple_numbers - что для простых чисел возвращается кортеж, содержащий одно данное число. Набор тестовых
данных: 3 → (3, ),  13 → (13, ),   29 → (29, )
5. test_two_simple_multipliers — проверяет случаи, когда передаются числа для которых функция factorize возвращает
кортеж с числом элементов равным 2. Набор тестовых данных: 6 → (2, 3),   26 → (2, 13),   121 --> (11, 11)
6. test_many_multipliers - проверяет случаи, когда передаются числа для которых функция factorize возвращает кортеж с
числом элементов больше 2. Набор тестовых данных: 1001 → (7, 11, 13) ,   9699690 → (2, 3, 5, 7, 11, 13, 17, 19)

ВАЖНО!  Все входные данные должны быть такими, как указано в условии. Название переменной в каждом тестовом случае
должно быть именно "x". При этом несколько различных проверок в рамках одного теста должны быть обработаны как
подслучаи с указанием x: subTest(x=...). В задании необходимо реализовать ТОЛЬКО класс TestFactorize, кроме этого
реализовывать ничего не нужно. Импортировать unittest и вызывать unittest.main() в отправляемом решении также не нужно.
"""

def factorize(x):
    """
    Factorize positive integer and return its factors.
    :type x: int,>=0
    :rtype: tuple[N],N>0
    """
    pass


import unittest


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        cases = ('string', 1.5)
        for x in cases:
            with self.subTest(case=x):
                self.assertRaises(TypeError, factorize, x)

    def test_negative(self):
        cases = (-1, -10, -100)
        for x in cases:
            with self.subTest(case=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        cases = (0, 1)
        for x in cases:
            with self.subTest(case=x):
                self.assertTupleEqual(factorize(x), (x,))

    def test_simple_numbers(self):
        cases = (3, 13, 29)
        for x in cases:
            with self.subTest(case=x):
                self.assertTupleEqual(factorize(x), (x,))

    def test_two_simple_multipliers(self):
        cases = (6, 26, 121)
        for i, x in enumerate(cases):
            expected = ((2, 3), (2, 13), (11, 11))
            with self.subTest(case=x):
                self.assertTupleEqual(factorize(x), expected[i])

    def test_many_multipliers(self):
        cases = (1001, 9699690)
        for i, x in enumerate(cases):
            expected = ((7, 11, 13), (2, 3, 5, 7, 11, 13, 17, 19))
            with self.subTest(case=x):
                self.assertTupleEqual(factorize(x), expected[i])


if __name__ == '__main__':
    unittest.main()

#######################################################################################################################
# Авторское решение задания
#######################################################################################################################

# class TestFactorize(unittest.TestCase):
#     def test_wrong_types_raise_exception(self):
#         """ аргументы типа float или str вызывают исключение TypeError """
#         for x in 1.5, 'string':
#             with self.subTest(x=x):
#                 with self.assertRaises(TypeError):
#                     factorize(x)
#
#     def test_negative(self):
#         """ отрицательные числа вызывают исключение ValueError """
#         for x in -1, -10, -100:
#             with self.subTest(x=x):
#                 with self.assertRaises(ValueError):
#                     factorize(x)
#
#     def test_zero_and_one_cases(self):
#         """ целые чисела 0 и 1, возвращают кортежи (0,) и (1,) соответственно. """
#         for x in 0, 1:
#             with self.subTest(x=x):
#                 self.assertEqual(factorize(x), (x,))
#
#     def test_simple_numbers(self):
#         """ для простых чисел возвращается кортеж, содержащий одно данное число """
#         for x in 3, 13, 29:
#             with self.subTest(x=x):
#                 self.assertEqual(factorize(x), (x,))
#
#     def test_two_simple_multipliers(self):
#         """ числа для которых функция factorize возвращает кортеж размером 2 """
#         test_cases = (
#             (6, (2, 3)),
#             (26, (2, 13)),
#             (121, (11, 11)),
#         )
#         for x, expected in test_cases:
#             with self.subTest(x=x):
#                 self.assertEqual(factorize(x), expected)
#
#     def test_many_multipliers(self):
#         """ числа для которых функция factorize возвращает кортеж размером >2 """
#         test_cases = (
#             (1001, (7, 11, 13)),
#             (9699690, (2, 3, 5, 7, 11, 13, 17, 19)),
#         )
#         for x, expected in test_cases:
#             with self.subTest(x=x):
#                 self.assertEqual(factorize(x), expected)
