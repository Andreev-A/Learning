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
