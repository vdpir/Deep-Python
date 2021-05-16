mport tempfile
import os
import time
import socket

class ClientError(Exception):
    """Exception raised for errors in the put.
    """
    pass

class Client:
    """Класс Client  реализует соединение с сервером метрик"""

    def __init__(self, server_ip, server_port, timeout = None):
        self.sock = socket.create_connection((server_ip, server_port), timeout)


    def get(self, metric):
        if self.sock.sendall("get {}\\n".format(metric).encode("utf8")) != None:
            raise ClientError()

        data = self.sock.recv(1024)
        response_str = data.decode("utf8")
        list_lines = response_str.split('\\n')

        if list_lines == "ok\\n\\n":
            return dict()

        if list_lines == "error\\nwrong command\\n\\n":
            raise ClientError()

        metric_dict = dict()

        for line in list_lines:
            metric_obs = line.split(' ')
            metric_obs[0]

            if metric_obs[0] in metric_dict:
                metric_dict[metric_obs[0]].append((int(metric_obs[1]),float(metric_obs[2])))
            else:
                metric_dict[metric_obs[0]] = [(int(metric_obs[1]),float(metric_obs[2]))]


        # TODO sort dict
        return metric_dict

    def put(self, metric, value, timestamp = None):
        """put palm.cpu 23.7 1150864247\n"""
        if (timestamp == None):
            timestamp = int(time.time())

        if (self.sock.sendall("put {} {} {}\\n".format(metric, value, timestamp).encode("utf8")) != None):
            raise ClientError()

        data = self.sock.recv(1024)
        response_str = data.decode("utf8")
        #if (response_str != 'ok\\n\\n')
        #    raise ClientError()

