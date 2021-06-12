import asyncio

storage = dict()

class ClientServerProtocol(asyncio.Protocol):
    def process_data(self, data):
        try:
            command, payload = data.split(" ", 1)
        except Exception:
            return self.unknown_command()

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

        if not self.is_put_payload_valid(payload):
            return 'error\nwrong command\n\n'

        try:
            key, value, timestamp = payload.split(' ')

            if key not in storage:
                storage[key] = []

            for idx, tup in enumerate(storage[key]):
                if tup[1] == int(timestamp):
                    storage[key][idx] = (float(value), int(timestamp))
                    return 'ok\n\n'

            storage[key].append((float(value), int(timestamp)))
            storage[key]=list(set(storage[key]))

        except Exception as err:
            return 'error\nwrong command\n\n'

        return 'ok\n\n'

    def unknown_command(self):
        return 'error\nwrong command\n\n'

    def get_data(self, payload):
        if not self.is_get_payload_valid(payload):
            return 'error\nwrong command\n\n'
        payload = payload.replace('\n','').replace('\r','')

        if payload == "*":
            return self.metric_to_string(storage)

        if payload not in storage:
            return 'ok\n\n'

        return self.metric_to_string({payload : storage[payload]})

    def metric_to_string(self, items):
        if len(storage) == 0:
            return 'ok\n\n'

        result_str = []
        for key, tup_l in items.items():
            tup_l_sorted = sorted(tup_l, key=lambda x: x[1])
            lst = [key + ' ' + ' '.join(map(str, list(tup))) for tup in tup_l_sorted]
            result_str.extend(lst)
        return 'ok\n' + '\n'.join(result_str) + '\n\n'

    def is_put_payload_valid(self, payload):
        payload_splits=payload.split()
        if payload[:-2:-1] != '\n' or len(payload_splits) != 3 or payload.count('\n') > 1:
            return False

        try:
            key, value, timestamp = payload.split(' ')
            fl_val=float(value)
            int_tsmp = int(timestamp)
        except Exception:
            return False

        return True

    def is_get_payload_valid(self, payload):
        payload_splits = payload.split()
        if payload[:-2:-1] != '\n' or len(payload_splits) != 1:
            return False
        return True


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

#run_server('127.0.0.1', 8181)