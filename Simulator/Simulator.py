__author__ = 'Joakim'
from NetworkCode import NetworkManager
from random import randint

# Init: create a bunch of MeterUnits, have some mainloop where they
# consume() in parallel, and the networkmanager can read their values and
# respond to incoming queries

TELEGRAM_SIZE = 255
MBUS_ACK = b'\xE5'


class MeterUnit(object):
    value = 0
    id = 0

    def __init__(self, id_number=0):
        self.value = randint(1000, 10000)
        self.id = id_number

    def consume(self):
        self.value += randint(1, 100)

    def get_value(self):
        return self.value

if __name__ == '__main__':
    nm = NetworkManager()
    mu = MeterUnit(1)
    while True:
        socket, address = nm.accept_connection()
        # receive PACKET_SIZE bytes
        tmp = socket.recv(TELEGRAM_SIZE)
        # tmp = ':'.join(':02x}'.format(c) for c in tmp)
        print("Received: %s from %s" % (tmp, (str(address))))
        # respond to client
        socket.sendall(MBUS_ACK)
        socket.close()

# ack_response = b'\xE5'
# rsp_ud = (b'\x68\x1D\x1D\x68'           # START:LENGTH:LENGTH:START
#          b'\x08\x01\x72'               # CONTROL:ADDRESS:CONTROL_INFO
#          b'\x44\x55\x66\x77\x88\x99'   # ACTIVE_DATA
#          b'\x11\x02\x00\x00\x00\x00'   # MORE DATA
#          b'\x86\x00\x82\xFF\x80\xFF'   # MORE DATA
#          b'\x00\x00\x00\x00\x00\x00'   # MORE DATA
#          b'\xDA\x0F\xCC\x16')          # DATA:DATA:CHECKSUM:STOP
