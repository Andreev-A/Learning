"""
Задание по программированию: Клиент для отправки метрик
В крупных проектах, с большим количеством пользователей, необходимо тщательно наблюдать за всеми процессами,
происходящими в нем. Информация о процессах может быть представлена различными численными показателями, например:
количество запросов к вашему приложению, время ответа вашего сервиса на каждый запрос, количество пользователей в
сутки и другие. Эти различные численные показатели мы будем называть метриками.
Для сбора, хранения и отображения подобных метрик существуют готовые решения, например Graphite, InfluxDB. Мы в рамках
курса разработаем свою систему для сбора и хранения метрик, основанную на клиент-серверной архитектуре.
На этой неделе мы начнем с разработки клиента для отправки и получения метрик. На следующей неделе, в качестве
финального задания, вам будет предложено реализовать сервер для хранения метрик.
Протокол взаимодействия
Прежде, чем приступить к описанию задания, рассмотрим протокол взаимодействия, по которому будет происходить обмен
данными между клиентом и сервером.
Клиент и сервер взаимодействуют между собой по простому текстовому протоколу через TCP сокеты. Текстовый протокол
имеет главное преимущество – наглядность, можно просматривать диалог взаимодействия клиентской и серверной стороны без
использования дополнительных инструментов.
Общий формат запросов и ответов.
Протокол поддерживает два вида запросов к серверу со стороны клиента:
- отправка данных для сохранения их на сервере
- получения сохраненных данных
Общий формат запроса клиента:
1  <команда> <данные запроса><\n>
где:
- <команда> - команда сервера (команда может принимать одно из двух значений: put — сохранить данные на сервере,
get — вернуть сохраненные данные с сервера),
- <данные запроса> - данные запроса (их формат мы подробно разберем ниже в примере),
- <\n> - символ переноса строки.
Обратим ваше внимание на пробел между командой и данными запроса и его отсутствием между данными и символом перевода
на новую строку.
Общий формат ответов сервера:
1   <статус ответа><\n><данные ответа><\n\n>
где:
- <статус ответа> - статус выполнения команды, допустимы два варианта: «ok» - команда успешно выполнена на сервере и
«error» - выполнение команды завершилось ошибкой
- <данные ответа> - не обязательное поле (формат ответа и случаи его отсутствия будут рассмотрены в примере ниже)
- <\n\n> - два символа переноса строки.
Обратите внимание, что статус ответа и данные ответа разделены символом перевода строки <\n>.
Пример взаимодействия сервера и клиента.
Для наглядности рассмотрим протокол взаимодействия между клиентом и сервером на конкретном примере. В примере мы
будем, собирать данные о работе операционной системы: cpu (загрузка процессора), usage (потребление памяти),
disk_usage (потребление места на жестком диске), network_usage (статистика сетевых интерфейсов). Такие данные могут
понадобится для контроля загрузки серверов и прогноза по расширению парка железа компании - проще говоря для
мониторинга.
Какие данные мы будем сохранять?
Для каждой метрики (<name>) мы будем хранить данные о ее значениях (<value>) и времени, когда производилось измерение
(<timestamp>) . Поскольку, в реальной жизни серверов может быть несколько, необходимо различать данные полученные от
разных серверов (в нашем примере имеются в наличии два сервера palm и eardrum). Договоримся об именовании метрик,
название метрики <name> в примере мы будем определять их по правилу:
1   <название сервера>.<название данных>
Примеры названий метрик:  "palm.cpu", "eardrum.memory".
Таким образом на сервере по каждому ключу будет сохранятся список данных конкретных измерений (пара: значение,
время измерения).
Обратим ваше внимание, на то что названия метрик могут быть произвольными и отличаться от тех, что используются в
данном примере (название метрики не обязательно должно быть составным и иметь точку в названии).
Запросы клиента.
Рассмотрим пример отправки на сервер данных для сохранения. Пусть у нас имеются данные измерений - загрузка процессора
«cpu» на сервере "palm" во время 1150864247 была равна 23.7 процента. Строка запроса в этом случае будет иметь вид:
1   put palm.cpu 23.7 1150864247\n
В запросе на сохранение мы можем передать данные только об одном измерении.
Чтобы получить с сервера данные, сохраненные по ключу «palm.cpu», необходимо в данных запроса просто передать имя
ключа:
1   get palm.cpu\n
Для случая, когда необходимо получить все хранимые на сервере данные, в качестве ключа используется символ звездочки
«*». Пример строки запроса:
1  # get *\n
Ответы сервера.
Допустим, что на сервере хранятся данные:
 name          | value | timestamp
-----------------------------------
"palm.cpu"    |  2.0  | 1150864247
"palm.cpu"    |  0.5  | 1150864248
"eardrum.cpu" |  3.0  | 1150864250
Тогда в ответ на запрос о получении данных по ключу "palm.cpu" сервер отправит строку:
1  ok\npalm.cpu 2.0 1150864247\npalm.cpu 0.5 1150864248\n\n
Данные ответа содержат данные о каждой сохраненной записи с ключом "palm.cpu" (метрика, значение, временная метка
разделенные пробелом), которые разделены символом перевода строки «\n».
Строка ответа сервера на запрос о получении всех хранящихся на сервере данных (в качестве ключа передано «*») в нашем
случае будет таким:
1  # ok\npalm.cpu 2.0 1150864247\npalm.cpu 0.5 1150864248\neardrum.cpu 3.0 1150864250\n\n
В случаях:
- когда в запросе на получение данных передан не существующий ключ
- успешного выполнения команды сохранения данных put
сервер отправляет клиенту строку со статусом «оk» и пустым полем с данными ответа:
1   ok\n\n
Если в параметре запроса переданы не валидные данные (например: нарушен формат запроса, ошибочная команда или значения
value и timestamp не могут быть приведены к необходимому типу данных) сервер отправляет строку со статусом ответа
«error» и данными ответа «wrong command»:
1   error\nwrong command\n\n
Реализация клиента.
Необходимо реализовать класс Client, в котором будет инкапсулировано соединение с сервером, клиентский сокет и методы
для получения (get) и отправки (put) метрик на сервер. Отправка и получение данных в методах get и put должна быть
реализована в соответствии с протоколом, описанным выше. В конструктор класса Client должна передаваться адресная
пара хост и порт, а также необязательный аргумент timeout (имеющий значение по умолчанию - None). Соединение с
сервером устанавливается при создании экземпляра класса Client  и не должно разрываться между запросами.
Пример создания объекта клиента и отправки запросов на сервер:
# >>> from client import Client
# >>> client = Client("127.0.0.1", 8888, timeout=15)
# >>> client.put("palm.cpu", 0.5, timestamp=1150864247)
# >>> client.put("palm.cpu", 2.0, timestamp=1150864248)
# >>> client.put("palm.cpu", 0.5, timestamp=1150864248)
# >>> client.put("eardrum.cpu", 3, timestamp=1150864250)
# >>> client.put("eardrum.cpu", 4, timestamp=1150864251)
# >>> client.put("eardrum.memory", 4200000)
# >>> print(client.get("*"))
Метод put.
Метод put принимает в качестве параметров: название метрики, численное значение и необязательный именованный параметр
timestamp. Если пользователь вызвал метод put без аргумента timestamp, то клиент автоматически должен подставить
значение временной отметки, полученное с помощью вызова int(time.time()).
Метод put не возвращает ничего в случае успешной отправки и выбрасывает пользовательское исключение ClientError в
случае не успешной.
Метод get.
Метод get принимает в качестве параметра имя метрики, значения которой мы хотим получить. В качестве имени метрики
можно использовать символ «*», о котором мы упоминали в описании протокола.
Метод get возвращает словарь с метриками (смотрите пример ниже) в случае успешного получения ответа от сервера и
выбрасывает исключение ClientError в случае не успешного.
Клиент получает данные от сервера в текстовом виде, метод get должен обработать строку ответа и вернуть словарь с
полученными ключами с сервера. Значением ключей в словаре является список кортежей:
1   [(timestamp1, metric_value1), (timestamp2, metric_value2), …]
Значение timestamp и metric_value должны быть преобразованы соответственно к типам int и float. Список должен быть
отсортирован по значению timestamp (по возрастанию).
Пример возвращаемого значения при успешном вызове client.get("palm.cpu"):
{
  'palm.cpu': [
    (1150864247, 0.5),
    (1150864248, 0.5)
  ]
}
Обратите внимание, что сервер хранит данные с максимальным разрешением в одну секунду. Это означает, что если в одну
и ту же секунду отправить две одинаковые метрики, то будет сохранено только одно значение, которое было обработано
последним. Все остальные значения будут перезаписаны. По этой причине запрос по ключу "palm.cpu" вернул данные двух
измерений.
Пример возвращаемого значения при успешном вызове client.get("*"):
{
  'palm.cpu': [
    (1150864247, 0.5),
    (1150864248, 0.5)
  ],
  'eardrum.cpu': [
    (1150864250, 3.0),
    (1150864251, 4.0)
  ],
  'eardrum.memory': [
    (1503320872, 4200000.0)
  ]
}
Если в ответ на get-запрос сервер вернул положительный ответ "ok\n\n", но без данных (то есть данных по запрашиваемому
ключу нет), то метод get клиента должен вернуть пустой словарь.
Итак, в качестве решения вам необходимо предоставить модуль с реализованным в нем классом Client, пользовательским
исключением ClientError. В классе Client должны быть доступны методы get и put с описанной выше сигнатурой. При вызове
методов get и put клиент должен посылать сообщения в TCP-соединение с сервером (в соответствии с описанным текстовым
протоколом), получать ответ от сервера и возвращать словарь с данными, в формате описанном выше.
Примечание.
Не смотря на то, что на этой неделе вы изучали асинхронность, клиент должен быть синхронным.

data = 'ok\npalm.cpu 2.0 1150864249\npalm.cpu 0.5 1150864248\neardrum.cpu 3.0 1150864250\n\n'
ret[res_key].sort(name=lambda tup: tup[0])
"""

import socket
import time


class ClientError(Exception):
    pass


class Client:

    def __init__(self, ip, port, timeout=None):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.buffer_size = 1024

    def __connect(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.ip, self.port))
            sock.settimeout(self.timeout)
            sock.send(message.encode('utf8'))
            return sock.recv(self.buffer_size).decode('utf8')

    def put(self, name, value, timestamp=None):
        if not timestamp:
            timestamp = int(time.time())
        else:
            timestamp = timestamp
        message = f"put {name} {value} {timestamp}\n"
        if self.__connect(message) == 'error\nwrong command\n\n':
            raise ClientError()

    def get(self, name):
        message = f'get {name}\n'
        data = self.__connect(message)
        if data[0:3] != 'ok\n':
            raise ClientError()
        if data == 'ok\n\n':
            return {}
        try:
            metric_dict = {}
            metrics = data.lstrip('ok\n').rstrip('\n\n')
            for metric in metrics.split('\n'):
                name, value, timestamp = metric.split()
                if name in metric_dict:
                    metric_dict[name].append((int(timestamp), float(value)))
                metric_dict.setdefault(name, [(int(timestamp), float(value))])
            for value in metric_dict.values():
                value.sort()
        except ValueError:
            raise ClientError()

        return metric_dict

#######################################################################################################################
# решение от преподавателей клиент для отправки метрик
#######################################################################################################################
# import bisect
# import socket
# import time
#
#
# class ClientError(Exception):
#     """класс исключений клиента"""
#     pass
#
#
# class Client:
#     def __init__(self, host, port, timeout=None):
#         self.host = host
#         self.port = port
#         self.timeout = timeout
#
#         try:
#             self.connection = socket.create_connection((host, port), timeout)
#         except socket.error as err:
#             raise ClientError("Cannot create connection", err)
#
#     def _read(self):
#
#         data = b""
#
#         while not data.endswith(b"\n\n"):
#             try:
#                 data += self.connection.recv(1024)
#             except socket.error as err:
#                 raise ClientError("Error reading data from socket", err)
#
#         return data.decode('utf-8')
#
#     def _send(self, data):
#
#         try:
#             self.connection.sendall(data)
#         except socket.error as err:
#             raise ClientError("Error sending data to server", err)
#
#     def put(self, key, value, timestamp=None):
#
#         timestamp = timestamp or int(time.time())
#         self._send(f"put {key} {value} {timestamp}\n".encode())
#         raw_data = self._read()
#
#         if raw_data == 'ok\n\n':
#             return
#         raise ClientError('Server returns an error')
#
#     def get(self, key):
#
#         self._send(f"get {key}\n".encode())
#         raw_data = self._read()
#         data = {}
#         status, payload = raw_data.split("\n", 1)
#         payload = payload.strip()
#
#         if status != 'ok':
#             raise ClientError('Server returns an error')
#
#         if payload == '':
#             return data
#
#         try:
#
#             for row in payload.splitlines():
#                 key, value, timestamp = row.split()
#                 if key not in data:
#                     data[key] = []
#                 bisect.insort(data[key], ((int(timestamp), float(value))))
#
#         except Exception as err:
#             raise ClientError('Server returns invalid data', err)
#
#         return data
#
#     def close(self):
#
#         try:
#             self.connection.close()
#         except socket.error as err:
#             raise ClientError("Error. Do not close the connection", err)

#######################################################################################################################
"""
    Это unittest для тестирования вашего класса Client из задания на неделе 5.

    Для запуска теста на локальном компьютере разместите код unittest-та
    и код решения в одном каталоге. Запустите тест при помощи команды:

        python -m unittest test_week5.py

    Обратите внимание на то, что ваш модуль должен называться client_for_sending_metrics.py.
    Это не обязательное требование, если вы назвали мобуль по-другому, то
    просто измените его импорт в строке 26 на:
        from you_module_name import Client, ClientError

    Модуль должен содержать классы Client и ClientError.

    Этот unittest поможет вам выполнить задание и пройти проверку на курсере.
    Успехов!
"""
#
# import unittest
# from unittest.mock import patch
# from collections import deque
#
# # импорт модуля с решением
# from client import Client, ClientError
#
#
# class ServerSocketException(Exception):
#     pass
#
#
# class ServerSocket:
#     """Mock socket module"""
#
#     def __init__(self):
#         self.response_buf = deque()
#         self.rsp_map = {
#             b'put test 0.5 1\n': b'ok\n\n',
#             b'put test 2.0 2\n': b'ok\n\n',
#             b'put test 0.4 2\n': b'ok\n\n',
#             b'put load 301 3\n': b'ok\n\n',
#             b'get key_not_exists\n': b'ok\n\n',
#             b'get test\n': b'ok\n'
#                            b'test 0.5 1\n'
#                            b'test 0.4 2\n\n',
#             b'get get_client_error\n': b'error\nwrong command\n\n',
#             b'get *\n': b'ok\n'
#                         b'test 0.5 1\n'
#                         b'test 0.4 2\n'
#                         b'load 301 3\n\n',
#         }
#
#     def sendall(self, data):
#         return self.send(data)
#
#     def send(self, data):
#         if data in self.rsp_map:
#             self.response_buf.append(self.rsp_map[data])
#         else:
#             raise ServerSocketException(input_file"запрос не соответствует протоколу: {data}")
#
#     def recv(self, bytes_count):
#         try:
#             rsp = self.response_buf.popleft()
#         except IndexError:
#             raise ServerSocketException("нет данных в сокете для чтения ответа")
#
#         return rsp
#
#     @classmethod
#     def create_connection(cls, *args, **kwargs):
#         return cls()
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         pass
#
#     def __getattr__(self, feature):
#         """ignore socket.connect, soket.bind, etc..."""
#         pass
#
#
# class TestClient(unittest.TestCase):
#     @classmethod
#     @patch("socket.create_connection", ServerSocket.create_connection)
#     @patch("socket.socket", ServerSocket.create_connection)
#     def setUpClass(cls):
#         cls.client = Client("127.0.0.1", 10000, timeout=2)
#
#     @patch("socket.create_connection", ServerSocket.create_connection)
#     @patch("socket.socket", ServerSocket.create_connection)
#     def test_client_put(self):
#         metrics_for_put = [
#             ("test", 0.5, 1),
#             ("test", 2.0, 2),
#             ("test", 0.4, 2),
#             ("load", 301, 3),
#         ]
#         for metric, value, timestamp in metrics_for_put:
#             try:
#                 self.client.put(metric, value, timestamp)
#             except ServerSocketException as exp:
#                 message = exp.args[0]
#                 self.fail(input_file"Ошибка вызова client.put("
#                           input_file"'{metric}', {value}, timestamp={timestamp})\n{message}")
#
#     @patch("socket.create_connection", ServerSocket.create_connection)
#     @patch("socket.socket", ServerSocket.create_connection)
#     def test_client_get_key(self):
#         try:
#             rsp = self.client.get("test")
#         except ServerSocketException as exp:
#             message = exp.args[0]
#             self.fail(input_file"Ошибка вызова client.get('test')\n{message}")
#
#         metrics_fixture = {
#             "test": [(1, .5), (2, .4)],
#         }
#         self.assertEqual(rsp, metrics_fixture)
#
#     @patch("socket.create_connection", ServerSocket.create_connection)
#     @patch("socket.socket", ServerSocket.create_connection)
#     def test_client_get_all(self):
#         try:
#             rsp = self.client.get("*")
#         except ServerSocketException as exp:
#             message = exp.args[0]
#             self.fail(input_file"Ошибка вызова client.get('*')\n{message}")
#
#         metrics_fixture = {
#             "test": [(1, .5), (2, .4)],
#             "load": [(3, 301.0)]
#         }
#         self.assertEqual(rsp, metrics_fixture)
#
#     @patch("socket.create_connection", ServerSocket.create_connection)
#     @patch("socket.socket", ServerSocket.create_connection)
#     def test_client_get_not_exists(self):
#         try:
#             rsp = self.client.get("key_not_exists")
#         except ServerSocketException as exp:
#             message = exp.args[0]
#             self.fail(input_file"Ошибка вызова client.get('key_not_exists')\n{message}")
#
#         self.assertEqual({}, rsp, "check rsp eq {}")
#
#     @patch("socket.create_connection", ServerSocket.create_connection)
#     @patch("socket.socket", ServerSocket.create_connection)
#     def test_client_get_client_error(self):
#         try:
#             self.assertRaises(ClientError,
#                               self.client.get, "get_client_error")
#         except ServerSocketException as exp:
#             message = exp.args[0]
#             self.fail(input_file"Некорректно обработано сообщение сервера об ошибке: {message}")
