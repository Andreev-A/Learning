"""
На предыдущей неделе вы разработали клиентское сетевое приложение — клиента для сервера метрик, который умеет
отправлять и получать данные о различных численных показателях. Пришло время финального задания — в нем необходимо
реализовать серверную часть.
Как обычно, вам необходимо разработать программу в одном файле-модуле, который вы загрузите на проверку обычным
способом. Сервер должен соответствовать протоколу, который был описан в задании к предыдущей неделе. Он должен уметь
принимать от клиентов команды put и get, разбирать их, и формировать ответ согласно протоколу. По запросу put
требуется сохранять метрики в структурах данных в памяти процесса. По запросу get сервер обязан отдавать данные в
правильной последовательности. При работе с клиентом сервер должен поддерживать сессии, соединение с клиентом между
запросами не должно "разрываться".
На верхнем уровне вашего модуля должна быть объявлена функция run_server(host, port) — она принимает адрес и порт, на
которых должен быть запущен сервер.
Для проверки правильности решения мы воспользуемся своей реализацией клиента и будем отправлять на ваш сервер put и
get запросы, ожидая в ответ правильные данные от сервера (согласно объявленному протоколу). Все запросы будут
выполняться с таймаутом — сервер должен отвечать за приемлемое время.
Сервер должен быть готов к неправильным командам со стороны клиента и отдавать клиенту ошибку в формате, оговоренном
в протоколе. В этих случаях работа сервера не должна завершаться аварийно.
На последней неделе мы с вами разбирали пример tcp-сервера на asyncio:

import asyncio
class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())
loop = asyncio.get_event_loop()
coro = loop.create_server(
    ClientServerProtocol,
    '127.0.0.1', 8181
)
server = loop.run_until_complete(coro)
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()

Данный код создает tcp-соединение для адреса 127.0.0.1:8181 и слушает все входящие запросы. При подключении клиента
будет создан новый экземпляр класса ClientServerProtocol, а при поступлении новых данных вызовется метод этого
объекта - data_received. Внутри asyncio.Protocol спрятана вся магия обработки запросов через корутины, остается
реализовать протокол взаимодействия между клиентом и сервером.
Вы можете использовать этот код, как основу при написании вашей реализации сервера. Это не обязательное требование.
Для реализации задачи вы можете использовать любые вызовы из стандартной библиотеки Python 3 (обратим ваше внимание,
что в грейдере установлена версия Python 3.6).  Сервер должен уметь обрабатывать запросы от нескольких клиентов
одновременно.
В процессе разработки сервера для тестирования работоспособности вы можете использовать клиент, написанный на
предыдущей неделе.
Давайте еще раз посмотрим на текстовый протокол в действии при использовании утилиты telnet:

$: telnet 127.0.0.1 8888
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
> get test_key
< ok
<
> got test_key
< error
< wrong command
<
> put test_key 12.0 1503319740
< ok
<
> put test_key 13.0 1503319739
< ok
<
> get test_key
< ok
< test_key 13.0 1503319739
< test_key 12.0 1503319740
<
> put another_key 10 1503319739
< ok
<
> get *
< ok
< test_key 13.0 1503319739
< test_key 12.0 1503319740
< another_key 10.0 1503319739

Также вы можете воспользоваться вспомогательным скриптом, который использует "'эталонную" реализацию клиента,
открывающуюся после сдачи задания на пятой неделе, для локального тестирования написанного вами сервера.
"""

import asyncio


class ClientError(Exception):
    pass


class EchoServerClientProtocol(asyncio.Protocol):
    metrics_dict = {}

    def __init__(self):
        super().__init__()
        self.transport = None
        self._buffer = b''

    def process_data(self, data):
        result = 'ok\n'
        messages = data.split("\n")
        for command in messages:
            if not command:
                continue
            try:
                method, metric = command.strip().split(" ", 1)
                if method == "put":
                    name, value, timestamp = metric.split()
                    if name not in self.metrics_dict:
                        self.metrics_dict[name] = {}
                    self.metrics_dict[name][int(timestamp)] = float(value)
                    return result + '\n'
                elif method == "get":
                    responses, result_dict, name = [], {}, metric
                    if len(name.strip().split(" ")) != 1:
                        raise ValueError("wrong command")
                    if name != "*":
                        result_dict = {name: self.metrics_dict.get(name, {})}
                    if name == "*":
                        result_dict = self.metrics_dict
                    for name in result_dict.keys():
                        for timestamp in sorted(result_dict[name]):
                            responses.append(
                                f"{name} {result_dict[name][timestamp]}"
                                f" {timestamp}"
                            )
                    if responses:
                        result += '\n'.join(responses) + '\n'
                    return result + '\n'
                else:
                    raise ValueError("unknown method")
            except ValueError:
                raise ClientError("wrong command")
        raise ClientError("wrong command")

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data: bytes):
        self._buffer += data
        decoded_data = self._buffer.decode()
        if not decoded_data.endswith('\n'):
            return
        self._buffer = b''
        try:
            resp = self.process_data(decoded_data)
        except ClientError as err:
            self.transport.write(f"error\n{err}\n\n".encode())
            return
        self.transport.write(resp.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        EchoServerClientProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server('127.0.0.1', 8888)

######################################################################################################################
# Решение от преподавателей сервер для приема метрик
######################################################################################################################
# Ниже наша реализация сервера для приема метрик. Код приложения разбит на классы Storage, StorageDriver и
# MetricsStorageServerProtocol. Storage инкапсулирует в себе методы для работы с хранилищем и сами метрики, в нашем
# случае мы просто сохраняем их в словарь, лежащий в памяти, однако класс легко расширить и добавить персистентность.
# StorageDriver — класс представляющий интерфейс для работы с хранилищем. Передача объекта хранилища при инициализации,
# позволяет абстрагироваться от конкретной реализации самого хранилища (мы можем реализовать хранение на файловой
# системе или на удаленном сервере, при этом в код класса StorageDriver не придется вносить изменения). В методе
# __call__ реализована логика разбора входных данных. MetricsStorageServerProtocol — класс, который реализует
# asyncio-сервер.
# Разбив логику приложения на несколько классов, мы можем легко модифицировать программу и добавлять новую
# функциональность. Также намного легче воспринимать и отлаживать код, который выполняет конкретную задачу, а не делает
# всё сразу. Надеемся, вы тоже постарались разбить свою реализацию на функциональные блоки с помощью классов и функций.
# import asyncio
# from collections import defaultdict
# from copy import deepcopy
#
#
# class StorageDriverError(ValueError):
#     pass
#
#
# class Storage:
#     """Класс для хранения метрик в памяти процесса"""
#
#     def __init__(self):
#         self._data = defaultdict(dict)
#
#     def put(self, key, value, timestamp):
#         self._data[key][timestamp] = value
#
#     def get(self, key):
#
#         if key == '*':
#             return deepcopy(self._data)
#
#         if key in self._data:
#             return {key: deepcopy(self._data.get(key))}
#
#         return {}
#
#
# class StorageDriver:
#     """Класс, предосталяющий интерфейс для работы с хранилищем данных"""
#
#     def __init__(self, storage):
#         self.storage = storage
#
#     def __call__(self, data):
#
#         method, *params = data.split()
#
#         if method == "put":
#             key, value, timestamp = params
#             value, timestamp = float(value), int(timestamp)
#             self.storage.put(key, value, timestamp)
#             return {}
#         elif method == "get":
#             key = params.pop()
#             if params:
#                 raise StorageDriverError
#             return self.storage.get(key)
#         else:
#             raise StorageDriverError
#
#
# class MetricsStorageServerProtocol(asyncio.Protocol):
#     """Класс для реализации сервера при помощи asyncio"""
#
#     # Обратите внимание на то, что storage является атрибутом класса, что предоставляет
#     # доступ к хранилищу данных для всех экземпляров класса MetricsStorageServerProtocol
#     # через обращение к атрибуту self.storage.
#     storage = Storage()
#     # настройки сообщений сервера
#     sep = '\n'
#     error_message = "wrong command"
#     code_err = 'error'
#     code_ok = 'ok'
#
#     def __init__(self):
#         super().__init__()
#         self.driver = StorageDriver(self.storage)
#         self._buffer = b''
#
#     def connection_made(self, transport):
#         self.transport = transport
#
#     def data_received(self, data):
#         """Метод data_received вызывается при получении данных в сокете"""
#
#         self._buffer += data
#
#         try:
#             request = self._buffer.decode()
#             # ждем данных, если команда не завершена символом \n
#             if not request.endswith(self.sep):
#                 return
#
#             self._buffer, message = b'', ''
#             raw_data = self.driver(request.rstrip(self.sep))
#
#             for key, values in raw_data.items():
#                 message += self.sep.join(f'{key} {value} {timestamp}' \
#                                          for timestamp, value in sorted(values.items()))
#                 message += self.sep
#
#             code = self.code_ok
#         except (ValueError, UnicodeDecodeError, IndexError):
#             message = self.error_message + self.sep
#             code = self.code_err
#
#         response = f'{code}{self.sep}{message}{self.sep}'
#         # отправляем ответ
#         self.transport.write(response.encode())
#
#
# def run_server(host, port):
#     loop = asyncio.get_event_loop()
#     coro = loop.create_server(MetricsStorageServerProtocol, host, port)
#     server = loop.run_until_complete(coro)
#
#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         pass
#
#     server.close()
#     loop.run_until_complete(server.wait_closed())
#     loop.close()
#
#
# if __name__ == "__main__":
#     run_server("127.0.0.1", 8888)
