# Все ошибки в языке Python делятся на 2 типа:
# 1. синтаксические - когда мы даем инструкцию интерпретатору, а интерпретатор не может ее разобрать, потому что в
# ней мы допустили синтаксическую ошибку
# 2. исключения - ошибки, возникающие в процессе исполнения самого кода
# Когда мы запускаем файл на исполнение, он проверяется целиком. И если в нем есть синтаксические ошибки, то он не
# начнет свое исполнение.
# В случае, если синтаксических ошибок нет, он будет выполняться строка за строкой.
# Сообщения об ошибках важно правильно уметь читать.
# У любой ошибки есть 3 обязательные вещи:
# ●	ошибки являются объектами и поэтому у любой ошибки есть тип (TypeError, NameError и т.д., по которым уже можно
# догадаться, какую ошибку мы совершили)
# ●	дополнительное сообщение, в котором более подробно расписано, что пошло не так
# ●	состояние стека вызовов на момент совершения ошибки

# Обработка исключений
# В теле конструкции try: указываем код, который мы хотели запустить проверить.
# Далее указываем ключевое слово except и тип того исключения, которое мы хотели бы обработать. Внутри except указываем
# инструкции, что делать, если исключение действительно возникло внутри тела try.
# Если внутри try блока происходит исключение, которое мы не ловим внутри блока except, то это исключение ведет себя
# также, как если бы этого try блока не было.
# Когда мы пишем несколько except блоков, важно помнить, что любое исключение будет обработано лишь одним из них
# - первым, под которое оно подойдет. Остальные except блоки просто не будут исполняться.
# Важно помнить, что мы можем ловить исключения в любой момент исполнения на стеке.
# В примере ниже мы ловим исключение деления на ноль не в момент выполнения деления, а в процессе исполнения функции f:
# def f(x, y):
#     try:
#         return x / y
#     except TypeError:
#         print('TypeError')
# try:
#     print(f(5, 0))
# except ZeroDivisionError:
#     print('ZeroDivisionError')
# Одним except блоком можно поймать сразу несколько типов исключений. Для этого в except блок нужно передавать кортеж с
# типами этих исключений.
# В языке Python мы можем поймать и сам объект ошибки:
# def f(x, y):
#     try:
#         return x / y
#     except (TypeError, ZeroDivisionError) as e:
#         print(type(e))
#         print(e)
#         print(e.args)
# print(f(5, 0))  # return вернет None
# print(f(5, []))  # return вернет None
# Если мы не знаем какой конкретный тип ошибки может произойти, потому что не ожидаем в исполнении блока ошибок, то
# можно указать пустой except без указания типа ошибки. Он поймает любую ошибку, которая произошла внутри кода:
# def f(x, y):
#     try:
#         return x / y
#     except:
#         print('Error')
# Все ошибки в языке Python представляют собой иерархию.
# При этом ошибки не используют множественное наследование. Можно точно гарантировать, что ZeroDivisionError наследуется
# от класса ArithmeticError, который, в свою очередь, наследуется только от Exception и т.д.:
# print(ZeroDivisionError.mro())
# try:
#     15 / 0
#     # e
# except ArithmeticError:  # isinstance(e, ArithmeticError) == True
#     print('ArithmeticError')
# Ключевое слово else используется тогда, когда внутри блока try не возникло никакого исключения.
# Блок finally запускается в любом случае (чтобы закрыть сессию, файл, базу данных, отменить транзакцию, вывести
# окончательное сообщение о совершенных процедурах и т.д, и т.п. перед тем, как приложение крашнется):
# ●	когда исключения не было
# ●	когда мы обработали исключение
# ●	и даже когда есть такое исключение, которое мы обработать не смогли
# Что интересно, блок finally выполняется даже в случае исполнения return внутри try. При этом его код никак не влияет
# на возвращаемое значение, если оно - неизменяемый тип, и влияет, если тип изменяем.
# Синтаксис try-except таков, что только:
# try
# except
# except
# ...........
# else
# finally
# Иерархия исключений:
# https://docs.python.org/3/library/exceptions.html#exception-hierarchy
# def divide(x, y):
#     try:
#         result = x / y
#     except ZeroDivisionError:
#         print('ZeroDivisionError')
#     else:
#         print('result', result)
#     finally:
#         print('finally')
# divide(2, 1)
# divide(2, 0)
# divide(2, [])
# А если требуется поймать все исключение и поработать с инстансом ошибки, то как быть? Просто except: не дает работать
# с инстансом. Правильно в этом случае писать следующий код:
# try:
#     # code
# except Exception as e:
#     print(e)
# Использование except без указания конкретного класса исключения считается плохой практикой, поскольку может
# значительно усложнить отладку. Кроме того, пустая ветка `except` перехватывает специальные исключения, наследующиеся
# от класса `BaseException`, например `SystemExit` или `KeyboardInterrupt` (происходит при нажатии Ctrl+C).
# Поэтому для того чтобы обработать "любое" исключение пишут `except Exception` а не просто `except`

# Терминология
# Ошибки (исключения):
# ●	ловят (catch)
# ●	бросают (throw)
# Вызов исключений
# Для того, чтобы бросить исключение в языке Python, используют конструкцию raise, в которую затем нужно передать объект
# нашего исключения.
# def greet(name):
#     if name[0].isupper():
#         return 'Hello ' + name
#     else:
#         raise ValueError(name + ' error')
# # print(greet('Anton'))
# # print(greet('anton'))
# while True:
#     try:
#         name = input('Enter your name: ')
#         greeting = greet(name)
#         print(greeting)
#     except ValueError:
#         print('Try again')
#     else:
#         break
# Все исключения, которые мы бросаем с помощью raise и все исключения, которые мы ловим, с помощью except должны быть
# экземплярами класса BaseException.
# Если нет такого класса, который бы подходил именно под нужный вам тип ошибки, можно написать собственный класс
# (пользовательские исключения, как правило, должны наследоваться от Exception):
# class BadName(Exception):
#     pass
#
# def greet(name):
#     if name[0].isupper():
#         return 'Hello ' + name
#     else:
#         raise BadName(name + ' error')
# print(greet('Anton'))
# print(greet('anton'))
# Все новые классы исключений должны наследоваться от Exception,
# согласно https://docs.python.org/3/library/exceptions.html

# Антон написал код, который выглядит следующим образом.
# try:
#    foo()
# except <имя 1>:
#    print("<имя 1>")
# except <имя 2>:
#    print("<имя 2>")
# ...
# Костя посмотрел на этот код и указал Антону на то, что некоторые исключения можно не ловить, так как ранее в коде
# будет пойман их предок. Но Антон не помнит какие исключения наследуются от каких. Помогите ему выйти из неловкого
# положения и напишите программу, которая будет определять обработку каких исключений можно удалить из кода.
# Важное примечание:
# В отличие от предыдущей задачи, типы исключений не созданы.
# Создавать классы исключений также не требуется
# Мы просим вас промоделировать этот процесс, и понять какие из исключений можно и не ловить, потому что мы уже ранее
# где-то поймали их предка.
# Формат входных данных
# В первой строке входных данных содержится целое число n - число классов исключений.
# В следующих n строках содержится описание наследования классов. В i-й строке указано от каких классов наследуется
# i-й класс. Обратите внимание, что класс может ни от кого не наследоваться. Гарантируется, что класс не наследуется
# сам от себя (прямо или косвенно), что класс не наследуется явно от одного класса более одного раза.
# В следующей строке содержится число m - количество обрабатываемых исключений.
# Следующие m строк содержат имена исключений в том порядке, в каком они были написаны у Антона в коде.
# Гарантируется, что никакое исключение не обрабатывается дважды.
# Формат выходных данных
# Выведите в отдельной строке имя каждого исключения, обработку которого можно удалить из кода, не изменив при этом
# поведение программы. Имена следует выводить в том же порядке, в котором они идут во входных данных.

# def search(child, parent):
#     if child == parent:
#         return True
#     for prev_parent in base[child]:
#         if search(prev_parent, parent):
#             return True
#     return False
#
#
# base, queue, out = {}, [], []
# for _ in range(int(input())):
#     child, *parents = input().replace(":", " ").split()
#     base[child] = parents
# for _ in range(int(input())):
#     queue.append(input())
# for _ in range(len(queue)):
#     a = queue.pop()
#     for i in reversed(queue):
#         if search(a, i):
#             out.append(a)
#             break
# print(*reversed(out), sep='\n')

# parents = {}
# for _ in range(int(input())):
#     a = input().split()
#     parents[a[0]] = [] if len(a) == 1 else a[2:]
#
# def is_parent(child, parent):
#     if child == parent: return True
#     for p in parents[child]:
#         if is_parent(p, parent): return True
#     return False
#
# exceptions = []
# for _ in range(int(input())):
#     a = input().strip()
#     for i in exceptions:
#         if is_parent(a, i):
#             print(a)
#             break
#     else:
#         exceptions.append(a)

# n = int(input())
# classes = {}
# for i in range(n):
#     line = input()
#     parts = line.split(" : ")
#     cls = parts[0]
#     if len(parts) == 1:
#         classes[cls] = []
#     else:
#         classes[cls] = parts[1].split(" ")
#
#
# def check(src, dest):
#     if src == dest:
#         return True
#     return any([check(child, dest) for child in classes[src]])
#
#
# used = []
#
# for i in range(int(input())):
#     cls = input()
#     if any([check(cls, used_one) for used_one in used]):
#         print(cls)
#     used.append(cls)

# Реализуйте класс PositiveList, отнаследовав его от класса list, для хранения положительных целых чисел.
# Также реализуйте новое исключение NonPositiveError.
# В классе PositiveList переопределите метод append(self, x) таким образом, чтобы при попытке добавить неположительное
# целое число бросалось исключение NonPositiveError и число не добавлялось, а при попытке добавить положительное целое
# число, число добавлялось бы как в стандартный list.
#
# class NonPositiveError(Exception):
#     pass
#
# class PositiveList(list):
#     def append(self, x):
#         if x > 0:
#             list.append(self, x)
#         else:
#             raise NonPositiveError
#
#
# class NonPositiveError(ArithmeticError):
#     pass
#
# class PositiveList(list):
#     def append(self, x):
#         if x <= 0:
#             raise NonPositiveError
#         super().append(x)
# Так помним несколько вещей:
# 1. Все исключения наследуется от класса Exception
# 2. self.append() обращается сам себе(то есть рекурсия бесконечная), super().append() обращается к предкам
# 3. Исключение вне команды except, вызывается через команду raise
