import socket
import select


class NetworkManager(object):
    port = 300
    local_host = ''
    remote_host = ''
    server_socket = socket
    remote_socket = socket

    def __init__(self, target_host='127.0.0.1'):
        self.localhost = socket.gethostname()
        self.remote_host = target_host

    def send(self, data):
        try:
            self.open_remote_socket()
            self.remote_socket.settimeout(1)
            self.remote_socket.sendall(data)
            tmp = self.remote_socket.recv(1024)
            if tmp:
                if tmp != b'\xe5':
                    while tmp[-1:] != b'\x16':
                        print(tmp)
                        tmp += self.remote_socket.recv(1024)
            self.close_remote_socket()
            return tmp
        except socket.timeout:
            print('Timeout error')
            return
        except socket.error:
            print('SOCKET ERROR!')
            return

    def accept_connection(self):
        s = self.server_socket
        r, w, err = select.select([s], [], [], 0)
        if not r:
            return 0, 0
        else:
            # print('Accepting connections now!')
            (client_socket, addr) = s.accept()
            client_socket.setblocking(1)
            return client_socket, addr

    def open_server_socket(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.local_host, self.port))
            self.server_socket.listen(10)
            self.server_socket.setblocking(1)
            # print('Opened: {}'.format(self.server_socket))
        except socket.error:
            print('General error opening server socket! Check NetworkCode!')
            exit(1)

    def close_server_socket(self):
        # print('Closing: {}'.format(self.server_socket))
        self.server_socket.close()

    def open_remote_socket(self):
        try:
            self.remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.remote_socket.connect((self.remote_host, self.port))
            # print('Opening, L={} R={}'.format(self.remote_socket.getsockname(), self.remote_socket.getpeername()))
        except socket.timeout:
            print('Timeout error opening remote socket!')
            # exit(1)
        except socket.error:
            print('General error opening remote socket! Check NetworkCode!')
            # exit(1)

    def close_remote_socket(self):
        try:
            # print('Closing, L={} R={}'.format(self.remote_socket.getsockname(), self.remote_socket.getpeername()))
            self.remote_socket.shutdown(socket.SHUT_RDWR)
            self.remote_socket.close()
        except socket.error:
            print('General error closing remote socket! Check NetworkCode!')
