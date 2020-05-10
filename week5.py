import socket
import time
from collections import defaultdict


class ClientError(Exception):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

    def put(self, metric_name, metric_value, timestamp=None):
        if not timestamp:
            timestamp = str(int(time.time()))
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            data = f"put {metric_name} {metric_value} {timestamp}\n"
            try:
                sock.send(data.encode('utf-8'))
            except socket.error:
                raise ClientError
            data_for_user = sock.recv(1024).decode('utf-8')
            status, _ = data_for_user.split("\n", 1)
            if status == "error":
                raise ClientError

    def get(self, metric_name):
        data = defaultdict(list)
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            user_request = f"get {metric_name}\n"
            try:
                sock.send(user_request.encode('utf-8'))
            except socket.error:
                raise ClientError(socket.error)
            data_for_user = sock.recv(1024).decode('utf-8')

            if data_for_user == 'ok\n\n':
                return {}
            status, payload = data_for_user.split("\n", 1)
            payload = payload.strip()
            if status == "error":
                raise ClientError(payload)
            data_for_user = [x.split() for x in data_for_user.split('\n')[1:] if len(x) > 1]
            try:
                [data[i[0]].append((int(i[2]), float(i[1]))) for i in data_for_user]
            except Exception:
                raise ClientError
        if metric_name == '*':
            return dict(data)
        else:
            data = {metric_name: sorted(data.get(metric_name), key = lambda v: v[0])}
            return data
