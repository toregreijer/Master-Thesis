import socket
import select


class NetworkManager(object):
    port = 11111
    local_host = ''
    remote_host = ''
    server_socket = socket
    remote_socket = socket

    def __init__(self, target_host='127.0.0.1'):
        self.localhost = socket.gethostname()
        self.remote_host = target_host

    def send(self, data):
        self.remote_socket.sendall(data)
        tmp = self.remote_socket.recv(255)
        return tmp

    def accept_connection(self):
        s = self.server_socket
        r, w, err = select.select([s], [], [], 0)
        if not r:
            return 0, 0
        else:
            print('Accepting connections now!')
            (client_socket, addr) = s.accept()
            client_socket.setblocking(1)
            return client_socket, addr

    def open_server_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.local_host, self.port))
        self.server_socket.listen(10)
        self.server_socket.setblocking(1)

    def close_server_socket(self):
        self.server_socket.close()

    def open_remote_socket(self):
        self.remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.remote_socket.connect((self.remote_host, self.port))

    def close_remote_socket(self):
        self.remote_socket.close()
