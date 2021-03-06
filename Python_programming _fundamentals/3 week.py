"""Даны длины сторон треугольника. Вычислите площадь треугольника.
Формат ввода - Вводятся три положительных действительных числа.
Формат вывода - Выведите ответ на задачу."""
# a, b, c = float(input()), float(input()), float(input())
# p = (a + b + c) / 2
# s = (p * (p - a) * (p - b) * (p - c)) ** 0.5
# print('{0:.6f}'.format(s))

"""По данному числу n вычислите сумму (1 / 1²)+(1 / 2²)+(1 / 3²)+...+(1 / n²).
Формат ввода - Вводится целое положительное число.
Формат вывода - Выведите ответ на задачу."""
# n = int(input())
# i, summa = 1, 0
# while i <= n:
#     summa += 1 / i ** 2
#     i += 1
# print('{0:.6f}'.format(summa))

"""Дано положительное действительное число X. Выведите его дробную часть.
Формат ввода - Вводится положительное действительное число.
Формат вывода - Выведите ответ на задачу."""
# x = float(input())
# print('{0:.6f}'.format(x - int(x)))

"""Цена товара обозначена в рублях с точностью до копеек, то есть действительным числом с двумя цифрами после десятичной
точки. Запишите в две целочисленные переменные стоимость товара в виде целого числа рублей и целого числа копеек и
выведите их на экран. При решении этой задачи нельзя пользоваться условными инструкциями и циклами.
Формат ввода - Вводится неотрицательное действительное число.
Формат вывода - Выведите ответ на задачу."""
# x = float(input())
# print(int(x), '{0:.0f}'.format((x - int(x)) * 100))

"""По российский правилам числа округляются до ближайшего целого числа,а если дробная часть числа равна 0.5, то число
округляется вверх. Дано неотрицательное число x, округлите его по этим правилам. Обратите внимание, что функция round
не годится для этой задачи!
Формат ввода - Вводится неотрицательное число.
Формат вывода - Выведите ответ на задачу."""
# x = float(input())
# if round(x - int(x), 10) >= 0.5:
#     print(int(x) + 1)
# else:
#     print(int(x))

"""Процентная ставка по вкладу составляет P процентов годовых, которые прибавляются к сумме вклада. Вклад составляет X
рублей Y копеек. Определите размер вклада через год. Рельзя пользоваться условными инструкциями и циклами.
Формат ввода - Программа получает на вход целые числа P, X, Y.
Формат вывода - Программа должна вывести два числа: величину вклада через год в рублях и копейках. Дробная часть
копеек отбрасывается. Поэтому надо сделать - my_input * 100 % 100
17
94
41
Ответ: 110 45."""
# p, x, y = int(input()), int(input()), int(input())
# my_input = ((x * 100 + y) + (x * 100 + y) * p / 100) / 100
# print(int(my_input), int(my_input * 100 % 100))

"""Процентная ставка по вкладу составляет P процентов годовых, которые прибавляются к сумме вклада через год. Вклад
составляет X рублей Y копеек. Определите размер вклада через K лет.
Формат ввода - Программа получает на вход целые числа  P, X, Y, K.
Формат вывода - Программа должна вывести два числа: величину вклада через K лет в рублях и копейках. Дробное число
копеек по истечение года отбрасывается. Перерасчет суммы вклада (с отбрасыванием дробных частей копеек) происходит
ежегодно."""
# p, x, y, k = int(input()), int(input()), int(input()), int(input())
# my_input = (x * 100 + y)
# i = 0
# while k > i:
#     my_input = (my_input + my_input * p / 100) // 1
#     i += 1
# print(int(my_input / 100), int(my_input % 100))

"""Дан многочлен P(x) = a[n] xⁿ+a[n-1] xⁿ⁻¹+...+a[1] x+a[0] и число x. Вычислите значение этого многочлена,
воспользовавшись схемой Горнера: P(x) = ( ... ( ( ( a[n] x + a[n-1] ) x + a[n-2] ) x + a[n-3] ) ... ) x + a[0]
Формат ввода - Сначала программе подается на вход целое неотрицательное число n ≤ 20, затем действительное число x,
затем следует n+1 вещественных чисел — коэффициенты многочлена от старшего к младшему.
Формат вывода - Программа должна вывести значение многочлена.
Примечания - При решении этой задачи нельзя использовать массивы и операцию возведения в степень. Программа должна
иметь сложность O(n), то есть при увеличении количества входных данных в k раз время выполнения программы должно
вырастать примерно в k раз."""
# n, x, a = int(input()), float(input()), float(input())
# i, summa = 0, a
# while n > i:
#     summa *= x
#     a = float(input())
#     summa += a
#     i += 1
# print(round(summa, 6))

"""Дана последовательность натуральных чисел x₁, x₂ ..., xn. Стандартным отклонением называется величина
σ=sqrt(((x₁-s)²+(x₂-s)²+…+(xn-s)²) / (n-1)), где s = ((x₁+x₂+…+xn) / n) — среднее арифметическое последовательности,
а sqrt - квадратный корень. Определите стандартное отклонение для данной последовательности натуральных чисел,
завершающейся числом 0.
Формат ввода - Вводится последовательность целых чисел, оканчивающаяся числом 0 (само число 0 в последовательность не
входит, а служит как признак ее окончания).
Формат вывода - Выведите ответ на задачу."""
# from math import sqrt
# number, n, summa, summa_squares = 1, -1, 0, 0
# while number != 0:
#     number = int(input())
#     summa += number
#     summa_squares += number ** 2
#     n += 1
# print(sqrt((summa_squares - summa ** 2 / n) / (n - 1)))

"""Даны действительные коэффициенты a, b, c, при этом a!=0. Решите квадратное уравнение ax²+bx+c=0 и выведите его корни.
Формат ввода - Вводятся три действительных числа.
Формат вывода - Если уравнение имеет два корня, выведите два корня в порядке возрастания, если один корень — выведите
одно число, если нет корней — не выводите ничего."""
# from math import sqrt
# a, b, c = float(input()), float(input()), float(input())
# d = b ** 2 - 4 * a * c
# if d > 0:
#     x_1 = (-b + sqrt(d)) / (2 * a)
#     x_2 = (-b - sqrt(d)) / (2 * a)
#     if x_1 > x_2:
#         x_1, x_2 = x_2, x_1
#     print(round(x_1, 6), round(x_2, 6))
# elif d == 0:
#     x = -b / (2 * a)
#     print(round(x, 6))

"""Даны произвольные действительные коэффициенты a, b, c. Решите уравнение ax²+bx+c=0.
Формат ввода - Вводятся три действительных числа.
Формат вывода - Если данное уравнение не имеет корней, выведите число 0. Если уравнение имеет один корень, выведите
число 1, а затем этот корень. Если уравнение имеет два корня, выведите число 2, а затем два корня в порядке
возрастания. Если уравнение имеет бесконечно много корней, выведите число 3."""
# from math import sqrt
# a, b, c = float(input()), float(input()), float(input())
# if a == 0:
#     if b == 0 and c == 0:
#         print(3)
#     elif b != 0:
#         print(1, -c / b)
#     elif b == 0 and c != 0:
#         print(0)
# else:
#     d = b ** 2 - 4 * a * c
#     if d > 0:
#         x_1 = (-b + sqrt(d)) / (2 * a)
#         x_2 = (-b - sqrt(d)) / (2 * a)
#         if x_1 > x_2:
#             x_1, x_2 = x_2, x_1
#         print(2, round(x_1, 6), round(x_2, 6))
#     elif d == 0:
#         x = -b / (2 * a)
#         print(1, round(x, 6))
#     elif d < 0:
#         print(0)

"""Даны вещественные числа a, b, c, d, e, input_file. Известно, что система линейных уравнений:
ax + by = e
cx + dy = input_file
имеет ровно одно решение. Выведите два числа x и y, являющиеся решением этой системы.
Формат ввода - Вводятся шесть чисел a, b, c, d, e, input_file - коэффициенты уравнений системы.
Формат вывода - Выведите ответ на задачу. Вариант округления - *1 00000000 // 100000000"""
# a, b, c, d = float(input()), float(input()), float(input()), float(input())
# e, input_file = float(input()), float(input())
# x, y = 0, 0
# if a != 0:
#     y = (input_file - c * e / a) / (d - c * b / a)  # a != 0
# if b != 0:
#     x = (input_file - d * e / b) / (c - d * a / b)  # b != 0
# if c != 0:
#     y = (e - a * input_file / c) / (b - a * d / c)  # c != 0
# if d != 0:
#     x = (e - b * input_file / d) / (a - b * c / d)  # d != 0
# print(round(x, 6), round(y, 6))
#
# a, b, c = float(input()), float(input()), float(input())
# d, e, input_file = float(input()), float(input()), float(input())
# x = (e * d - b * input_file) / (a * d - b * c)
# y = (a * input_file - c * e) / (a * d - b * c)
# print(x, y)  # *100000000//100000000

"""Даны числа a, b, c, d, e, input_file. Решите систему линейных уравнений
ax + by = e
cx + dy = input_file
Формат ввода - Вводятся 6 чисел a, b, c, d, e, input_file — коэффициенты уравнений.
Формат вывода - Вывод программы зависит от вида решения этой системы.
Если система не имеет решений, то программа должна вывести единственное число 0.
Если система имеет бесконечно много решений, каждое из которых имеет вид y=px+q, то программа должна вывести число 1,
а затем значения p и q.
Если система имеет единственное решение (x₀,y₀), то программа должна вывести число 2, а затем значения x₀ и y₀.
Если система имеет бесконечно много решений вида x=x₀, y—любое, то программа должна вывести число 3, затем значение x₀.
Если система имеет бесконечно много решений вида y=y₀, x—любое, то программа должна вывести число 4, затем значение y₀.
Если любая пара чисел (x,y) является решением, то программа должна вывести число 5."""
# a, b, c, d = float(input()), float(input()), float(input()), float(input())
# e, input_file = float(input()), float(input())
# if a * d == b * c and a * input_file != c * e:
#     print(0)
# elif a == b == 0 and e != 0:
#     print(0)
# elif c == d == 0 and input_file != 0:
#     print(0)
# elif a == c == 0 and b * input_file != d * e:
#     print(0)
# elif b == d == 0 and a * input_file != c * e:
#     print(0)
# elif a == b == c == d == e == input_file == 0:
#     print(5)
# elif a * d == b * c and a * input_file == c * e:
#     if b == d == 0:
#         if a != 0 and c != 0:
#             print(3, e / a)
#         elif a == 0 and e == 0:
#             print(3, input_file / c)
#         elif c == 0 and input_file == 0:
#             print(3, e / a)
#     elif a == c == 0:
#         if b:
#             print(4, e / b)
#         elif d:
#             print(4, input_file / d)
#     elif b:
#         print(1, -a / b, e / b)
#     elif d:
#         print(1, -c / d, input_file / d)
# else:
#     x = (e * d - b * input_file) / (a * d - b * c)
#     y = (a * input_file - c * e) / (a * d - b * c)
#     print(2, x, y)

"""Дана строка. Если в этой строке буква input_file встречается только один раз, выведите её индекс. Если она
встречается два и более раз, выведите индекс её первого и последнего появления. Если буква input_file в данной строке
не встречается, ничего не выводите. При решении этой задачи нельзя использовать метод count и циклы."""
# string = input()
# first = string.find('input_file')
# last = string.rfind('input_file')
# if first != -1:
#     if first == last:
#         print(first)
#     else:
#         print(first, last)

"""Дана строка, в которой буква h встречается минимум два раза.Удалите из этой строки первое и последнее вхождение буквы
h, а также все символы, находящиеся между ними."""
# string = input()
# first = string.find('h')
# last = string.rfind('h')
# first = string[:first]
# last = string[last + 1:]
# print(first + last)

"""Дана строка, в которой буква h встречается как минимум два раза. Выведите измененную строку: повторите
последовательность символов, заключенную между первым и последним появлением буквы h два раза (сами буквы h не
в повторяемый фрагмент, т. е. их повторять не надо)."""
# string = input()
# first = string.find('h')
# last = string.rfind('h')
# first = string[first + 1:]
# last = string[:last]
# print(last + first)

"""Дана строка. Найдите в этой строке второе вхождение буквы input_file и выведите индекс этого вхождения. Если буква
input_file в данной строке встречается только один раз, выведите число -1, а если не встречается ни разу, выведите 
число -2. При решении этой задачи нельзя использовать метод count."""
# string = input()
# first = string.find('input_file')
# if first == -1:
#     print(-2)
# else:
#     first = string.find('input_file', first + 1)
#     if first == -1:
#         print(-1)
#     else:
#         print(first)

"""Дана строка, состоящая ровно из двух слов, разделенных пробелом. Переставьте эти слова местами. Результат запишите в
строку и выведите получившуюся строку. При решении этой задачи нельзя пользоваться циклами и инструкцией if."""
# string = input()
# space = string.find(' ')
# first = string[space + 1:]
# second = string[:space]
# print(first, second)

"""Дана строка. Удалите из этой строки все символы @."""
# string = input()
# s = string.replace('@', '')
# print(s)

"""Дана строка. Замените в этой строке все появления буквы h на букву H, кроме первого и последнего вхождения."""
# string = input()
# pos_min = string.find('h')
# pos_max = string.rfind('h')
# fragment = string[pos_min + 1:pos_max]
# fragment = fragment.replace('h', 'H')
# print(string[:pos_min + 1] + fragment + string[pos_max:])

"""Дана строка. Получите новую строку, вставив между каждыми двумя символами исходной строки символ *. Выведите
полученную строку."""
# string, count, = input(), 1,
# my_input = string[0]
# while len(string) > count:
#     my_input = my_input + '*' + string[count]
#     count += 1
# print(my_input)

"""Дана строка. Удалите из нее все символы, чьи индексы делятся на 3.Символы строки нумеруются, начиная с нуля."""
# string, count, = input(), 0,
# my_input = ''
# while len(string) > count:
#     if count % 3 != 0:
#         my_input = my_input + string[count]
#     count += 1
# print(my_input)
