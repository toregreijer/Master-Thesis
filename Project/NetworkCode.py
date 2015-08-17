__author__ = 'Joakim'
import socket
import select


class NetworkManager(object):
    port = 11111
    local_host = ''
    remote_host = ''
    serversocket = socket

    def __init__(self, target_host='127.0.0.1'):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.localhost = socket.gethostname()
        self.remote_host = target_host
        # self.serversocket.bind((self.local_host, self.port))
        # self.serversocket.listen(10)
        # self.serversocket.setblocking(1)

    def send(self, data):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.remote_host, self.port))
        s.sendall(data)
        tmp = s.recv(255)
        s.close()
        return tmp

    def accept_connection(self):
        s = self.serversocket
        r, w, err = select.select([s], [], [], 0)
        if not r:
            return 0, 0
        else:
            print('Accepting connections now!')
            (client_socket, addr) = s.accept()
            client_socket.setblocking(1)
            return client_socket, addr

    def close_the_socket(self):
        self.serversocket.close()
