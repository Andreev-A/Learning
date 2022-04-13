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
