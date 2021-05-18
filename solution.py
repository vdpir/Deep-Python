import asyncio

storage = dict()

class ClientServerProtocol(asyncio.Protocol):

    def process_data(self, data):
        #"put {key} {value} {timestamp}
        command, payload = data.split(" ", 1)

        if command == 'put':
            return self.put_data(payload)
        else:
            if command == 'get':
                return self.get_data(payload)
            else:
                return self.unknown_command()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def put_data(self, payload):
        try:
            key, value, timestamp = payload.split(' ')

            if key not in storage:
                storage[key] = []
            storage[key].append((float(value), int(timestamp)))
        except Exception as err:
            return 'error\nwrong command\n\n'

        return 'ok\n\n'

    def unknown_command(self):
        return 'error\nwrong command\n\n'

    def get_data(self, payload):
        payload = payload.replace('\n','')
        print(payload)
        if payload  == "*":
            print('ok\n' + '\n'.join([' '.join([key, tup]) for key, tup in storage]) + '\n')
            return 'ok\n'+ '\n'.join([' '.join(key,tup) for key, tup in storage]) + '\n'

        if payload not in storage:
            return 'ok\n\n'

        return  'ok\n'+ '\n'.join([' '.join([payload,tup]) for tup in storage[payload]]) + '\n'


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
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

run_server('127.0.0.1', 8181)
