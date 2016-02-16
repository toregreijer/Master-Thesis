import socket
import select


class NetworkManager(object):
    port = 300
    mbus_master_address = '192.168.1.41'
    local_host = '127.0.0.1'
    remote_host = ''
    server_socket = socket
    remote_socket = socket

    def __init__(self):
        self.remote_host = self.local_host

    def switch_remote_host(self):
        if self.remote_host == self.local_host:
            self.remote_host = self.mbus_master_address
        else:
            self.remote_host = self.local_host

    def send(self, data):
        try:
            self.open_remote_socket()
            self.remote_socket.settimeout(1)
            self.remote_socket.sendall(data)
            tmp = self.remote_socket.recv(1024)
            # Some handling for troublesome MBus communication
            if tmp:  # Is the response more than None?
                if tmp != b'\xe5':  # If so, is it more than a simple ACK (E5)?
                    while tmp[-1:] != b'\x16':  # Then keep receiving until a complete telegram has arrived.
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
        except socket.timeout:
            print('Timeout error opening remote socket!')
        except socket.error:
            print('General error opening remote socket! Check NetworkCode!')

    def close_remote_socket(self):
        try:
            self.remote_socket.shutdown(socket.SHUT_RDWR)
            self.remote_socket.close()
        except socket.error:
            print('General error closing remote socket! Check NetworkCode!')
