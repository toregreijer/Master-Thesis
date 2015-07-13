__author__ = 'Joakim'
import socket


class Networker(object):
    port = 42420
    local_host = ""
    remote_host = ""
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

    def receive(self):
        s = self.s
        s.bind((self.local_host, self.port))
        s.listen(5)
        operations = 0
        while operations < 3:
            # establish a connection
            client_socket, addr = s.accept()
            tmp = client_socket.recv(4096)
            tmp = ':'.join(x.encode('hex') for x in tmp)    # or ":".join("{:02x}".format(ord(c)) for c in s)
            client_socket.sendall('xE5')
            if not tmp:
                break
            print "Got a connection from %s, saying %s" % (str(addr), tmp)
            client_socket.close()
            operations += 1
        s.close()





"""

# client.py
import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# connection to hostname on the port.
s.connect((host, port))

# Receive no more than 1024 bytes
tm = s.recv(1024)

s.close()

print("The time got from the server is %s" % tm.decode('ascii'))


# server.py
import socket
import time

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

while True:
    # establish a connection
    clientsocket,addr = serversocket.accept()

    print("Got a connection from %s" % str(addr))
    currentTime = time.ctime(time.time()) + "\r\n"
    clientsocket.send(currentTime.encode('ascii'))
    clientsocket.close()


    # echo_server.py
import socket

host = ''        # Symbolic name meaning all available interfaces
port = 12345     # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
while True:
    data = conn.recv(1024)
    if not data: break
    conn.sendall(data)
conn.close()

Client:

# echo_client.py
import socket

host = socket.gethostname()
port = 12345                   # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.sendall(b'Hello, world')
data = s.recv(1024)
s.close()
print('Received', repr(data))
"""



