__author__ = 'Joakim'
from NetworkCode import NetworkManager
from random import randint
from time import sleep
import threading

# Init: create a bunch of MeterUnits, have some mainloop where they
# consume() in parallel, and the network manager can read their values and
# respond to incoming queries

TELEGRAM_SIZE = 255
MBUS_ACK = b'\xE5'
MBUS_DATA = (b'\x68\x1D\x1D\x68'           # START:LENGTH:LENGTH:START
             b'\x08\x01\x72'               # CONTROL:ADDRESS:CONTROL_INFO
             b'\x44\x55\x66\x77\x88\x99'   # ACTIVE_DATA
             b'\x11\x02\x00\x00\x00\x00'   # MORE DATA
             b'\x86\x00\x82\xFF\x80\xFF'   # MORE DATA
             b'\x00\x00\x00\x00\x00\x00'   # MORE DATA
             b'\xDA\x0F\xCC\x16')


class MeterUnit(threading.Thread):
    value = 0
    id = 0

    def __init__(self, thread_id, name, id_number=0):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.value = randint(1000, 10000)
        self.id = id_number

    def consume(self):
        self.value += randint(1, 10)

    def get_value(self):
        return self.value

    def run(self):
        while self.value < 15000:
            self.consume()
            sleep(5)


if __name__ == '__main__':
    nm = NetworkManager()
    meter_units = []
    for x in range(1, 3):
        meter_units.append(MeterUnit(x, 'thread_name', x))
    # mu2 = MeterUnit(2, 't2', 2)
    # mu3 = MeterUnit(3, 't3', 3)
    for mu in meter_units:
        mu.start()
    # mu2.start()
    # mu3.start()
    while True:
        client_socket, address = nm.accept_connection()
        if client_socket is 0:
            continue
        # receive PACKET_SIZE bytes
        telegram = client_socket.recv(TELEGRAM_SIZE)
        while telegram:
            print(telegram)
            for mu in meter_units:
                print(mu.get_value())
            # print(mu2.get_value())
            # print(mu3.get_value())
            telegram = ':'.join('{:02x}'.format(c) for c in telegram)
            print('Received: %s from %s' % (telegram, (str(address))))

            # respond to client
            if telegram.startswith('10:40'):
                client_socket.sendall(MBUS_ACK)
            else:
                client_socket.sendall(MBUS_DATA)
            telegram = client_socket.recv(TELEGRAM_SIZE)
            # telegram = ''

        client_socket.close()
    nm.close_the_socket()

# ack_response = b'\xE5'
# rsp_ud = (b'\x68\x1D\x1D\x68'           # START:LENGTH:LENGTH:START
#          b'\x08\x01\x72'               # CONTROL:ADDRESS:CONTROL_INFO
#          b'\x44\x55\x66\x77\x88\x99'   # ACTIVE_DATA
#          b'\x11\x02\x00\x00\x00\x00'   # MORE DATA
#          b'\x86\x00\x82\xFF\x80\xFF'   # MORE DATA
#          b'\x00\x00\x00\x00\x00\x00'   # MORE DATA
#          b'\xDA\x0F\xCC\x16')          # DATA:DATA:CHECKSUM:STOP
