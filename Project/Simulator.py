__author__ = 'Joakim'
from NetworkCode import NetworkManager
from random import randint
from time import sleep
import threading
import MBus


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

    def get_id(self):
        return self.id

    def run(self):
        while self.value < 15000:
            self.consume()
            sleep(5)
    # TODO: Catch keyboard interrupts and close down the simulator and all its threads safely.

if __name__ == '__main__':
    nm = NetworkManager()
    nm.open_server_socket()
    meter_units = []
    for x in range(1, 3):
        meter_units.append(MeterUnit(x, 'thread_name', x))
    for mu in meter_units:
        mu.start()
    while True:
        client_socket, address = nm.accept_connection()
        if client_socket is 0:
            continue
        # receive TELEGRAM_SIZE bytes
        telegram = client_socket.recv(MBus.TELEGRAM_SIZE)
        while telegram:
            # print(telegram)
            for mu in meter_units:
                print('Unit #%s: %s' % (mu.get_id(), hex(mu.get_value())))
            telegram = ':'.join('{:02x}'.format(c) for c in telegram)
            print('Received: %s from %s' % (telegram, (str(address))))

            # respond to client
            if telegram.startswith('10:40'):
                client_socket.sendall(MBus.ACK)
            elif telegram.startswith('10:5'):
                client_socket.sendall(MBus.RSP_UD)
            telegram = client_socket.recv(MBus.TELEGRAM_SIZE)
        client_socket.close()
    nm.close_server_socket()
