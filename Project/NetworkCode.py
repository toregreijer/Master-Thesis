import socket
import select
import logging


class NetworkManager(object):
    port = 300
    mbus_master_address = '192.168.1.41'
    netbook_address = '192.168.1.175'
    local_host = '127.0.0.1'
    remote_host = ''
    server_socket = socket
    remote_socket = socket

    def __init__(self):
        self.local_host = socket.gethostname()
        self.remote_host = self.netbook_address
        logging.debug('NetworkManager up and running.')

    def set_port(self, p):
        self.port = p
        logging.info('New port set to {}'.format(p))

    def set_mbus_master(self, host):
        self.mbus_master_address = host
        logging.info('New MBus master set to {}'.format(host))

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
            logging.error('send() : Timeout error.')
            return
        except socket.error:
            logging.error('send() : Socket error.')
            return

    def accept_connection(self):
        s = self.server_socket
        r, w, err = select.select([s], [], [], 0)
        if not r:
            return 0, 0
        else:
            logging.debug('Accepting connections now!')
            (client_socket, addr) = s.accept()
            client_socket.setblocking(1)
            return client_socket, addr

    def open_server_socket(self,  port_arg=300):
        self.port = port_arg
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((socket.gethostname(), self.port))
            self.server_socket.listen(10)
            self.server_socket.setblocking(1)
        except socket.error:
            logging.error('General error opening server socket! Check NetworkCode!')
            exit(1)

    def close_server_socket(self):
        logging.debug('Closing: {}'.format(self.server_socket))
        self.server_socket.close()

    def open_remote_socket(self):
        try:
            self.remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.remote_socket.connect((self.remote_host, self.port))
        except socket.timeout:
            logging.error('Timeout error opening remote socket!')
        except socket.error:
            logging.error('General error opening remote socket! Check NetworkCode!')

    def close_remote_socket(self):
        try:
            self.remote_socket.shutdown(socket.SHUT_RDWR)
            self.remote_socket.close()
        except socket.error:
            logging.error('General error closing remote socket! Check NetworkCode!')
