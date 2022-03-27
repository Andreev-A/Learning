"""Реализуйте класс Matrix. Он должен содержать:
Конструктор от списка списков. Гарантируется, что списки состоят из чисел, не пусты и все имеют одинаковый размер.
Конструктор должен копировать содержимое списка списков, т. е. при изменении списков, от которых была сконструирована
матрица, содержимое матрицы изменяться не должно.
Метод __str__, переводящий матрицу в строку. При этом элементы внутри одной строки должны быть разделены знаками
табуляции, а строки  —  переносами строк. После каждой строки не должно быть символа табуляции и в конце не должно
быть переноса строки.
Метод size без аргументов, возвращающий кортеж вида (число строк, число столбцов). Пример теста с участием этого
метода есть в следующей задаче этой недели."""
# from sys import stdin
#
#
# class Matrix:
#     def __init__(self, cls):
#         self._cls = [lst[:] for lst in cls]
#
#     def __str__(self):
#         s = ''
#         for i in self._cls:
#             if s:
#                 s += '\n'
#             s += '\t'.join(map(str, i))
#         return s
#
#     def size(self):
#         return len(self._cls), len(self._cls[0])
#
#
# exec(stdin.read())

"""Добавьте в предыдущий класс следующие методы:
 __add__, принимающий вторую матрицу того же размера и возвращающий сумму матриц.
 __mul__, принимающий число типа int или float и возвращающий матрицу, умноженную на скаляр.
 __rmul__, делающий то же самое, что и __mul__. Этот метод будет вызван в том случае, аргумент находится справа. Для
реализации этого метода в коде класса достаточно написать __rmul__ = __mul__.
Иллюстрация:
 В следующем случае вызовется __mul__: Matrix([[0, 1], [1, 0]) * 10.
 В следующем случае вызовется __rmul__ (так как у int не определен __mul__ для матрицы справа):
 10 * Matrix([[0, 1], [1, 0]).
Разумеется, данные методы не должны менять содержимое матрицы.
Формат ввода - Как в предыдущей задаче.
Формат вывода - Как в предыдущей задаче."""
# from sys import stdin
#
#
# class Matrix:
#     def __init__(self, cls):
#         self.cls = [lst[:] for lst in cls]
#
#     def __str__(self):
#         s = ''
#         for i in self.cls:
#             if s:
#                 s += '\n'
#             s += '\t'.join(map(str, i))
#         return s
#
#     def __add__(self, other):
#         return Matrix([[num + other.cls[j][i] for i, num in enumerate(number)]
#                        for j, number in enumerate(self.cls)])
#
#     def __mul__(self, other):
#         return Matrix([[num * other for num in number]
#                        for number in self.cls])
#
#     __rmul__ = __mul__
#
#     def size(self):
#         return len(self.cls), len(self.cls[0])
#
#
# exec(stdin.read())

# # Другой вариант класса
# from sys import stdin
# from copy import deepcopy
#
#
# class Matrix:
#     def __init__(self, matrix):
#         self.matrix = deepcopy(matrix)
#
#     def __str__(self):  # без аргументов
#         return '\n'.join(['\t'.join(map(str, list)) for list in self.matrix])
#
#     def __add__(self, other):
#         return Matrix()
#
#     def size(self):  # без аргументов!
#         return (len(self.matrix), len(self.matrix[0]))
#
#     def __add__(self, other):
#         return Matrix(list(map(
#             lambda x, y: list(map(lambda z, w: z + w, x, y)),
#             self.matrix, other.matrix)))
#
#     def __mul__(self, other):
#         return Matrix([[i * other for i in list] for list in self.matrix])
#
#     __rmul__ = __mul__
#
#
# # exec(stdin.read())

# m1 = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
# m2 = Matrix([[0, 1, 0], [20, 0, -1], [-1, -2, 0]])
# print(m1 + m2)
# m = Matrix([[1, 1, 0], [0, 2, 10], [10, 15, 30]])
# alpha = 15
# print(m * alpha)
# print(alpha * m)

"""Добавьте в программу из предыдущей задачи класс MatrixError, содержащий внутри self поля matrix1 и matrix2 — ссылки
на матрицы.
В класс Matrix внесите следующие изменения:
Добавьте в метод __add__ проверку на ошибки в размере входных данных, чтобы при попытке сложить матрицы разных
размеров было выброшено исключение MatrixError таким образом, чтобы matrix1 поле MatrixError стало первым аргументом
__add__ (просто self), а matrix2  —  вторым (второй операнд для сложения).
Реализуйте метод transpose, транспонирующий матрицу и возвращающую результат (данный метод модифицирует экземпляр
класса Matrix)
Реализуйте статический метод transposed, принимающий Matrix и возвращающий транспонированную матрицу. Пример
статического метода.
Формат ввода - Как в предыдущей задаче.
Формат вывода - Как в предыдущей задаче."""
# from sys import stdin
#
#
# class MatrixError(BaseException):
#     def __init__(self, cls, other):
#         self.matrix1 = cls
#         self.matrix2 = other
#
#
# class Matrix:
#     def __init__(self, cls):
#         self.cls = [lst[:] for lst in cls]
#
#     def __str__(self):
#         s = ''
#         for i in self.cls:
#             if s:
#                 s += '\n'
#             s += '\t'.join(map(str, i))
#         return s
#
#     def __add__(self, other):
#         if len(self.cls) == len(other.cls):
#             return Matrix(
#                 [[num + other.cls[j][i] for i, num in enumerate(number)]
#                  for j, number in enumerate(self.cls)])
#
#         else:
#             raise MatrixError(self, other)
#
#     def __mul__(self, other):
#         return Matrix([[num * other for num in number]
#                        for number in self.cls])
#
#     __rmul__ = __mul__
#
#     def size(self):
#         return len(self.cls), len(self.cls[0])
#
#     def transpose(self):
#         if isinstance(self, Matrix):
#             self.cls = [*zip(*self.cls)]  #  list(map(list, zip(*self.matrix)))
#             return Matrix(self.cls)
#
#     @staticmethod
#     def transposed(cls):
#         return Matrix([*zip(*cls.cls)])
#
#
# exec(stdin.read())

"""Внесите следующие изменение в предыдущую программу:
Измените метод __mul__ таким образом, чтобы матрицы можно было умножать как на скаляры, так и на другие матрицы. В
случае, если две матрицы перемножить невозможно, то тогда выбросьте ошибку MatrixError. Первая матрице в ошибке  —
это self, вторая  —  это второй операнд умножения.
Формат ввода - Как в предыдущей задаче.
Формат вывода - Как в предыдущей задаче."""
# from sys import stdin
#
#
# class MatrixError(BaseException):
#     def __init__(self, cls, other):
#         self.matrix1 = cls
#         self.matrix2 = other
#
#
# class Matrix:
#     def __init__(self, cls):
#         self.cls = [lst[:] for lst in cls]
#
#     def __str__(self):
#         s = ''
#         for i in self.cls:
#             if s:
#                 s += '\n'
#             s += '\t'.join(map(str, i))
#         return s
#
#     def __add__(self, other):
#         if len(self.cls) == len(other.cls):
#             return Matrix(
#                 [[num + other.cls[j][i] for i, num in enumerate(number)]
#                  for j, number in enumerate(self.cls)])
#
#         else:
#             raise MatrixError(self, other)
#
#     def __mul__(self, other):
#         if isinstance(other, int) or isinstance(other, float):
#             return Matrix([[num * other for num in number]
#                            for number in self.cls])
#         elif isinstance(other, Matrix):
#             if self.size()[1] != other.size()[0]:
#                 raise MatrixError(self, other)
#             return Matrix(
#                 list(map(
#                     lambda x: list(
#                         map(
#                             lambda y: sum(map(
#                                 lambda z: z[0] * z[1],
#                                 zip(x, y))
#                             ),
#                             zip(*other.cls))),
#                     zip(*Matrix.transposed(self).cls))
#                 )
#             )
#
#     __rmul__ = __mul__
#
#     def size(self):
#         return len(self.cls), len(self.cls[0])
#
#     def transpose(self):
#         if isinstance(self, Matrix):
#             self.cls = [*zip(*self.cls)]
#             return Matrix(self.cls)
#
#     @staticmethod
#     def transposed(cls):
#         return Matrix([*zip(*cls.cls)])
#
#
# exec(stdin.read())

# Тест 1
# Входные данные:
# # Task 4 check 1
# mid = Matrix([[1, 0, 0],[0, 1, 0],[0, 0, 1]])
# m1 = Matrix([[3, 2], [-10, 0], [14, 5]])
# m2 = Matrix([[5, 2, 10], [-0.5, -0.25, 18], [-22, -2.5, -0.125]])
# print(mid * m1)
# print(mid * m2)
# print(m2 * m1)
# try:
#     m = m1 * m2
#     print("WA It should be error")
# except MatrixError as e:
#     print(e.matrix1)
#     print(e.matrix2)
#
# Вывод программы:
# 3	2
# -10	0
# 14	5
# 5.0	2.0	10.0
# -0.5	-0.25	18.0
# -22.0	-2.5	-0.125
# 135	60
# 253.0	89.0
# -42.75	-44.625
# 3	2
# -10	0
# 14	5
# 5	2	10
# -0.5	-0.25	18
# -22	-2.5	-0.125
#
#
#
# Тест 2
# Входные данные:
# # Task 4 check 2
# mid = Matrix([[1, 0, 0],[0, 1, 0],[0, 0, 1]])
# m1 = Matrix([[3, 2], [-10, 0], [14, 5]])
# m2 = Matrix([[5, 2, 10], [-0.5, -0.25, 18], [-22, -2.5, -0.125]])
# print(0.5 * m2)
# print(m2 * (0.5 * mid * m1))
#
# Вывод программы:
# 2.5	1.0	5.0
# -0.25	-0.125	9.0
# -11.0	-1.25	-0.0625
# 67.5	30.0
# 126.5	44.5
# -21.375	-22.3125
#
#
#
# Тест 3
# Входные данные:
# # Task 4 check 3
# mid = Matrix([[1, 0, 0],[0, 1, 0],[0, 0, 1]])
# m1 = Matrix([[3, 2], [-10, 0], [14, 5]])
# m2 = Matrix([[5, 2, 10], [-0.5, -0.25, 18], [-22, -2.5, -0.125]])
# print(5 * m2)
# print(m2 * (120 * mid * m1))
#
# Вывод программы:
# 25	10	50
# -2.5	-1.25	90
# -110	-12.5	-0.625
# 16200	7200
# 30360.0	10680.0
# -5130.0	-5355.0

# Тест 5
# Task 4 check 5
# m1 = Matrix([[3, 2], [-10, 0], [14, 5]])
# m2 = Matrix([[5, 2, 10], [-0.5, -0.25, 18], [-22, -2.5, -0.125]])
# print(m2 * m1)
# print(Matrix.transposed(m2 * m1))
# print(m1.transpose() * m2.transpose())
# Ответ:
# 135	60
# 253.0	89.0
# -42.75	-44.625
# 135	253.0	-42.75
# 60	89.0	-44.625
# 135	253.0	-42.75
# 60	89.0	-44.625

# # Другой вариант класса
# from sys import stdin
#
# class MatrixError(BaseException):
#     def __init__(self, Mtx, other):
#         self.matrix1 = Mtx
#         self.matrix2 = other
#
#
# class Matrix:
#     def __init__(self, l4l):
#         self.Mtx = [_.copy() for _ in l4l]
#
#     def __str__(self):
#         return '\n'.join(['\t'.join(map(str, self.Mtx[i]))
#                           for i in range(len(self.Mtx))])
#
#     def size(self):
#         return len(self.Mtx), len(self.Mtx[0])
#
#     def __add__(self, other):
#         if self.size() != other.size():
#             raise MatrixError(self, other)
#         return Matrix(list(map(
#             lambda a, b: list(map(
#                 lambda x, y: x + y, a, b)), self.Mtx, other.Mtx)))
#
#     def __mul__(self, other):
#         if isinstance(other, int) or isinstance(other, float):
#             return Matrix([list(map(
#                 lambda x: x * other, self.Mtx[i]))
#                 for i in range(len(self.Mtx))])
#         elif isinstance(other, Matrix):
#             if self.size()[1] != other.size()[0]:
#                 raise MatrixError(self, other)
#             return Matrix(
#                 list(map(
#                         lambda x: list(
#                             map(
#                                 lambda y: sum(map(
#                                     lambda z: z[0] * z[1],
#                                     zip(x, y))
#                                 ),
#                             zip(*other.Mtx))),
#                     zip(*Matrix.transposed(self).Mtx))
#                 )
#             )
#
#     __rmul__ = __mul__
#
#     def transpose(self):
#         self.Mtx = list(map(lambda *args: list(args), *self.Mtx))
#         return Matrix(self.Mtx)
#
#     @staticmethod
#     def transposed(M):
#         return Matrix(list(map(lambda *args: list(args), *M.Mtx)))
#
#
# exec(stdin.read())
#
# # Другой вариант метода
# def __mul__(self, n):
#     if isinstance(n, list):
#         if len(self.l[0]) != len(n):
#             return MatrixError
#         else:
#             tmp, res = [], [] * len(self.l)
#             for i in range(len(self.l)):
#                 for j in range(len(n[0])):
#                     s = 0
#                     for k in range(len(self.l[0])):
#                         s += self.l[i][k] * n[k][j]
#                     tmp.append(s)
#                 res.append(tmp)
#                 tmp = []
#             return Matrix(res)
#     else:
#         return ([n * j for j in i] for i in self.l)

"""Пусть экземпляр класса Matrix задаёт систему линейных алгебраических уравнений.
Тогда добавьте в класс метод solve, принимающий вектор-строку свободных членов и возвращающий строку-список, состоящую
из float  —  решение системы, если оно единственно. Если решений нет или оно не единственно  — выдайте какую-нибудь
ошибку.
Формат ввода - Как в предыдущей задаче.
Формат вывода - Как в предыдущей задаче."""
# def solve(self, vector):
#     if self.size()[1] != self.size()[0]:
#         raise Exception("The Matrix is not square!")
#     elif self.size()[1] != len(vector):
#         raise Exception("The Matrix and vector have different length!")
#     helperD = []
#     for i in range(len(vector)):
#         M = Matrix(self.cls)
#         for j in range(len(vector)):
#             M.cls[j][i] = vector[j]
#         helperD.append(Matrix.determinator(M))
#     return list(map(lambda x: x / Matrix.determinator(self), helperD))
#
#
# @staticmethod
# def determinator(M):
#     if M.size()[0] == 2:
#         return M.cls[0][0] * M.cls[1][1] - M.cls[0][1] * M.cls[1][0]
#     elif M.size()[0] == 3:
#         return \
#             M.cls[0][0] * M.cls[1][1] * M.cls[2][2] \
#             + M.cls[2][0] * M.cls[0][1] * M.cls[1][2] \
#             + M.cls[1][0] * M.cls[2][1] * M.cls[0][2] \
#             - M.cls[2][0] * M.cls[1][1] * M.cls[0][2] \
#             - M.cls[0][0] * M.cls[2][1] * M.cls[1][2] \
#             - M.cls[1][0] * M.cls[0][1] * M.cls[2][2]
#     else:
#         raise Exception("Matrix's range more than 3")

# Тест 1
# Входные данные:
# # Task 5 check 1
# m = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
# print(m.solve([1,1,1]))
# Вывод программы:
# [1.0, 1.0, 1.0]
#
# Тест 2
# Входные данные:
# # Task 5 check 2
# m = Matrix([[1, 1, 1], [0, 2, 0], [0, 0, 4]])
# print(m.solve([1,1,1]))
# Вывод программы:
# [0.25, 0.5, 0.25]
#
# Тест 3
# Входные данные:
# # Task 5 check 3
# m = Matrix([[1, 1, 1], [0, 1, 2], [0.5, 1, 1.5]])
# try:
#     s = m.solve([1,1,1])
#     print('WA No solution')
# except Exception as e:
#     print('OK')
# Вывод программы:
# OK

"""К программе в предыдущей задаче добавьте класс SquareMatrix  —  наследник Matrix с операцией возведения в степень
__pow__, принимающей натуральную степень (включая ноль), в которую нужно возвести матрицу. Используйте быстрое
возведение в степень.
Формат ввода - Как в предыдущей задаче.
Формат вывода - Как в предыдущей задаче.
Возводить в степень можно гораздо быстрее, чем за n умножений! Для этого нужно воспользоваться следующими
рекуррентными соотношениями: aⁿ = (a²)ⁿ/² при четном n, aⁿ=a⋅aⁿ⁻¹ при нечетном n. Реализуйте алгоритм быстрого
возведения в степень. Если вы все сделаете правильно,то сложность вашего алгоритма будет O(logn)."""
# def power(a, n):
#     if n == 0:
#         return 1
#     if n % 2 == 0:
#         return power(a, n/2)**2
#     else:
#         return a*power(a, n-1)
#
# a = int(input())
# n = int(input())
# print(power(a, n))


# class SquareMatrix(Matrix):
#     def __mul__(self, other):
#         return SquareMatrix(super().__mul__(other).cls)
#
#     def __pow__(self, n):
#         if n in [0, 1]:
#             return self
#         elif n == 2:
#             return self * self
#         if n % 2 != 0:
#             return self * (self ** (n - 1))
#         else:
#             return (self * self) ** (n // 2)
#
# m = SquareMatrix([[1, 1, 0, 0, 0, 0],
#                   [0, 1, 1, 0, 0, 0],
#                   [0, 0, 1, 1, 0, 0],
#                   [0, 0, 0, 1, 1, 0],
#                   [0, 0, 0, 0, 1, 1],
#                   [0, 0, 0, 0, 0, 1]]
#                 )
# print(m)
# print('----------')
# print(m ** 1)
# print('----------')
# print(m ** 2)
# print('----------')
# print(m ** 3)
# print('----------')
# print(m ** 4)
# print('----------')
# print(m ** 5)

####################################################################################################################
# Классы полностью
####################################################################################################################
from sys import stdin


class MatrixError(BaseException):
    def __init__(self, cls, other):
        self.matrix1 = cls
        self.matrix2 = other


class Matrix:
    def __init__(self, cls):
        self.cls = [lst[:] for lst in cls]

    def __str__(self):
        s = ''
        for i in self.cls:
            if s:
                s += '\n'
            s += '\t'.join(map(str, i))
        return s

    def __add__(self, other):
        if len(self.cls) == len(other.cls):
            return Matrix(
                [[num + other.cls[j][i] for i, num in enumerate(number)]
                 for j, number in enumerate(self.cls)])

        else:
            raise MatrixError(self, other)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Matrix([[num * other for num in number]
                           for number in self.cls])
        elif isinstance(other, Matrix):
            if self.size()[1] != other.size()[0]:
                raise MatrixError(self, other)
            return Matrix(
                list(map(
                    lambda x: list(
                        map(
                            lambda y: sum(map(
                                lambda z: z[0] * z[1],
                                zip(x, y))
                            ),
                            zip(*other.cls))),
                    zip(*Matrix.transposed(self).cls))
                )
            )

    __rmul__ = __mul__

    def size(self):
        return len(self.cls), len(self.cls[0])

    def transpose(self):
        if isinstance(self, Matrix):
            self.cls = [*zip(*self.cls)]
            return Matrix(self.cls)

    @staticmethod
    def transposed(cls):
        return Matrix([*zip(*cls.cls)])

    def solve(self, vector):
        if self.size()[1] != self.size()[0]:
            raise Exception("The Matrix is not square!")
        elif self.size()[1] != len(vector):
            raise Exception("The Matrix and vector have different length!")
        helperD = []
        for i in range(len(vector)):
            M = Matrix(self.cls)
            for j in range(len(vector)):
                M.cls[j][i] = vector[j]
            helperD.append(Matrix.determinator(M))
        return list(map(lambda x: x / Matrix.determinator(self), helperD))

    @staticmethod
    def determinator(M):
        if M.size()[0] == 2:
            return M.cls[0][0] * M.cls[1][1] - M.cls[0][1] * M.cls[1][0]
        elif M.size()[0] == 3:
            return \
                M.cls[0][0] * M.cls[1][1] * M.cls[2][2] \
                + M.cls[2][0] * M.cls[0][1] * M.cls[1][2] \
                + M.cls[1][0] * M.cls[2][1] * M.cls[0][2] \
                - M.cls[2][0] * M.cls[1][1] * M.cls[0][2] \
                - M.cls[0][0] * M.cls[2][1] * M.cls[1][2] \
                - M.cls[1][0] * M.cls[0][1] * M.cls[2][2]
        else:
            raise Exception("Matrix's range more than 3")


class SquareMatrix(Matrix):
    def __mul__(self, other):
        return SquareMatrix(super().__mul__(other).cls)

    def __pow__(self, n):
        if n in [0, 1]:
            return self
        elif n == 2:
            return self * self
        if n % 2 != 0:
            return self * (self ** (n - 1))
        else:
            return (self * self) ** (n // 2)


exec(stdin.read())
