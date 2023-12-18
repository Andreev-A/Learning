"""
Это вспомогательный скрипт для тестирования сервера из задания на неделе 6.

Для запуска скрипта на локальном компьютере разместите рядом файл client_for_sending_metrics.py,
где содержится код клиента, который открывается по прохождении задания
недели 5.

Сначала запускаете ваш сервер на адресе 127.0.0.1 и порту 8888, а затем
запускаете этот скрипт.
"""
import sys
from client_for_sending_metrics import Client, ClientError


def run(host, port):
    client1 = Client(host, port, timeout=5)
    client2 = Client(host, port, timeout=5)
    command = "wrong command test\n"

    try:
        data = client1.get(command)
    except ClientError:
        pass
    except BaseException as err:
        print(f"Ошибка соединения с сервером: {err.__class__}: {err}")
        sys.exit(1)
    else:
        print("Неверная команда, отправленная серверу, должна возвращать ошибку протокола")
        sys.exit(1)

    command = 'some_key'
    try:
        data_1 = client1.get(command)
        data_2 = client1.get(command)
    except ClientError:
        print('Сервер вернул ответ на валидный запрос, который клиент определил, '
              'как не корректный.. ')
    except BaseException as err:
        print(f"Сервер должен поддерживать соединение с клиентом между запросами, "
              f"повторный запрос к серверу завершился ошибкой: {err.__class__}: {err}")
        sys.exit(1)

    assert data_1 == data_2 == {}, \
        "На запрос клиента на получения данных по несуществующему ключу, сервер " \
        "вдолжен озвращать ответ с пустым полем данных."

    try:
        data_1 = client1.get(command)
        data_2 = client2.get(command)
    except ClientError:
        print('Сервер вернул ответ на валидный запрос, который клиент определил'
              ', как не корректный.. ')
    except BaseException as err:
        print(f"Сервер должен поддерживать соединение с несколькими клиентами: "
              f"{err.__class__}: {err}")
        sys.exit(1)

    assert data_1 == data_2 == {}, \
        "На запрос клиента на получения данных по не существующему ключу, сервер " \
        "должен возвращать ответ с пустым полем данных."

    try:
        client1.put("k1", 0.25, timestamp=1)
        client2.put("k1", 2.156, timestamp=2)
        client1.put("k1", 0.35, timestamp=3)
        client2.put("k2", 30, timestamp=4)
        client1.put("k2", 40, timestamp=5)
        client1.put("k2", 41, timestamp=5)
    except Exception as err:
        print(f"Ошибка вызова client.put(...) {err.__class__}: {err}")
        sys.exit(1)

    expected_metrics = {
        "k1": [(1, 0.25), (2, 2.156), (3, 0.35)],
        "k2": [(4, 30.0), (5, 41.0)],
    }

    try:
        metrics = client1.get("*")
        if metrics != expected_metrics:
            print(f"client.get('*') вернул неверный результат. Ожидается: "
                  f"{expected_metrics}. Получено: {metrics}")
            sys.exit(1)
    except Exception as err:
        print(f"Ошибка вызова client.get('*') {err.__class__}: {err}")
        sys.exit(1)

    expected_metrics = {"k2": [(4, 30.0), (5, 41.0)]}

    try:
        metrics = client2.get("k2")
        if metrics != expected_metrics:
            print(f"client.get('k2') вернул неверный результат. Ожидается: "
                  f"{expected_metrics}. Получено: {metrics}")
            sys.exit(1)
    except Exception as err:
        print(f"Ошибка вызова client.get('k2') {err.__class__}: {err}")
        sys.exit(1)

    try:
        result = client1.get("k3")
        if result != {}:
            print(
                f"Ошибка вызова метода get с ключом, который еще не был добавлен. "
                f"Ожидается: пустой словарь. Получено: {result}")
            sys.exit(1)
    except Exception as err:
        print(f"Ошибка вызова метода get с ключом, который еще не был добавлен: "
              f"{err.__class__} {err}")
        sys.exit(1)

    print("Похоже, что все верно! Попробуйте отправить решение на проверку.")


if __name__ == "__main__":
    run("127.0.0.1", 8888)

############################################################################################################################################################
# Сервер для приема метрик
############################################################################################################################################################
'''
Ниже наша реализация сервера для приема метрик. Код приложения разбит на классы Storage, StorageDriver и MetricsStorageServerProtocol. Storage инкапсулирует в себе
методы для работы с хранилищем и сами метрики, в нашем случае мы просто сохраняем их в словарь, лежащий в памяти, однако класс легко расширить и добавить персистентность.
StorageDriver — класс представляющий интерфейс для работы с хранилищем. Передача объекта хранилища при инициализации, позволяет абстрагироваться от конкретной реализации 
самого хранилища (мы можем реализовать хранение на файловой системе или на удаленном сервере, при этом в код класса StorageDriver не придется вносить изменения). В 
методе __call__ реализована логика разбора входных данных. MetricsStorageServerProtocol — класс, который реализует asyncio-сервер.

Разбив логику приложения на несколько классов, мы можем легко модифицировать программу и добавлять новую функциональность. Также намного легче воспринимать и отлаживать код, 
который выполняет конкретную задачу, а не делает всё сразу. Надеемся, вы тоже постарались разбить свою реализацию на функциональные блоки с помощью классов и функций.
'''
import asyncio
from collections import defaultdict
from copy import deepcopy


class StorageDriverError(ValueError):
    pass


class Storage:
    """Класс для хранения метрик в памяти процесса"""

    def __init__(self):
        self._data = defaultdict(dict)

    def put(self, key, value, timestamp):
        self._data[key][timestamp] = value

    def get(self, key):

        if key == '*':
            return deepcopy(self._data)

        if key in self._data:
            return {key: deepcopy(self._data.get(key))}

        return {}


class StorageDriver:
    """Класс, предосталяющий интерфейс для работы с хранилищем данных"""

    def __init__(self, storage):
        self.storage = storage

    def __call__(self, data):

        method, *params = data.split()

        if method == "put":
            key, value, timestamp = params
            value, timestamp = float(value), int(timestamp)
            self.storage.put(key, value, timestamp)
            return {}
        elif method == "get":
            key = params.pop()
            if params:
                raise StorageDriverError
            return self.storage.get(key)
        else:
            raise StorageDriverError


class MetricsStorageServerProtocol(asyncio.Protocol):
    """Класс для реализации сервера при помощи asyncio"""

    # Обратите внимание на то, что storage является атрибутом класса, что предоставляет
    # доступ к хранилищу данных для всех экземпляров класса MetricsStorageServerProtocol
    # через обращение к атрибуту self.storage.
    storage = Storage()
    # настройки сообщений сервера
    sep = '\n'
    error_message = "wrong command"
    code_err = 'error'
    code_ok = 'ok'

    def __init__(self):
        super().__init__()
        self.driver = StorageDriver(self.storage)
        self._buffer = b''

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        """Метод data_received вызывается при получении данных в сокете"""

        self._buffer += data

        try:
            request = self._buffer.decode()
            # ждем данных, если команда не завершена символом \n
            if not request.endswith(self.sep):
                return

            self._buffer, message = b'', ''
            raw_data = self.driver(request.rstrip(self.sep))

            for key, values in raw_data.items():
                message += self.sep.join(f'{key} {value} {timestamp}' \
                                         for timestamp, value in sorted(values.items()))
                message += self.sep

            code = self.code_ok
        except (ValueError, UnicodeDecodeError, IndexError):
            message = self.error_message + self.sep
            code = self.code_err

        response = f'{code}{self.sep}{message}{self.sep}'
        # отправляем ответ
        self.transport.write(response.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(MetricsStorageServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server("127.0.0.1", 8888)
