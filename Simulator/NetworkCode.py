__author__ = 'Joakim'
import socket


class NetworkManager(object):
    port = 11111
    local_host = ''
    remote_host = ''
    s = socket

    def __init__(self, target_host='127.0.0.1'):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.localhost = socket.gethostname()
        self.remote_host = target_host

    def send(self, data):
        s = self.s
        s.connect((self.remote_host, self.port))
        s.sendall(data)
        s.close()

    def accept_connection(self):
        s = self.s
        s.bind((self.local_host, self.port))
        s.listen(5)
        # operations = 0
        # establish a connection
        print('Accepting connections now!')
        client_socket, addr = s.accept()
        # s.close()
        return client_socket, addr

        # while operations < 5:

        # receive 1024 bytes
        # print("Receiving!")
        # tmp = client_socket.recv(255)
        # print(tmp)
        # tmp = ':'.join(':02x}'.format(c) for c in tmp)
        # ALTERNATIVE ':'.join(x.encode('hex') for x in tmp)

        # client_socket.sendall(b'\xE5')
        # debug printouts
        # print('0xE5'.encode('utf-8'))
        # print(int('0xE5', 16))
        # print(hex(229))

        # break if we didn't receive anything
        # if not tmp:
        #     client_socket.close()
        #     break

        # print some debug info
        # print('Got a connection from %s, saying %s' % (str(addr), tmp))
        # close the socket
        # client_socket.close()
        # increment operations
        # operations += 1
        # client_socket.close()

