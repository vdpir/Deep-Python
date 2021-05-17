import tempfile
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

    def send_data(self, send_string):
        return self.sock.sendall(send_string.encode("utf8"))

    def get_data(self):
        return self.sock.recv(1024).decode("utf8")

    def get(self, metric):
        if self.send_data("get {}\n".format(metric)) != None:
            raise ClientError()

        response_str = self.get_data()
        list_lines = response_str.split('\n')

        if list_lines == "ok\n\n":
            return dict()

        if list_lines == 'error\nwrong command\n\n':
            raise ClientError()

        metric_dict = dict()

        for line in list_lines[1:]:
            metric_obs = line.split(' ')
            if metric_obs[0] == '':
                break

            if metric_obs[0] in metric_dict:
                metric_dict[metric_obs[0]].append((int(metric_obs[2]),float(metric_obs[1])))
                metric_dict[metric_obs[0]] = list(sorted(metric_dict[metric_obs[0]], key=lambda item: item[0]))
            else:
                metric_dict[metric_obs[0]] = [(int(metric_obs[2]),float(metric_obs[1]))]
        return metric_dict

    def put(self, metric, value, timestamp = None):
        """put palm.cpu 23.7 1150864247\n"""
        if (timestamp == None):
            timestamp = int(time.time())

        if (self.send_data("put {} {} {}\n".format(metric, value, timestamp))) != None:
            raise ClientError()

        #response_str = self.get_data()

        #if (response_str != 'ok\\n\\n')
        #    raise ClientError()

