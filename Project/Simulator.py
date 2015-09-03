from NetworkCode import NetworkManager
from random import randint
from time import sleep
import threading
import MBus
import sys

NUM_UNITS = 3


class MeterUnit(threading.Thread):
    value = 0
    id = 0
    exit_flag = 0

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
        while not self.exit_flag and self.value < 15000:
            self.consume()
            sleep(1)

    def shutdown(self):
        self.exit_flag = 1

if __name__ == '__main__':
    print('Starting simulator!')
    nm = NetworkManager()
    nm.open_server_socket()
    print('Listening for incoming connections!')
    meter_units = []
    print('Starting {NU} meter units'.format(NU=NUM_UNITS))
    for x in range(1, NUM_UNITS):
        meter_units.append(MeterUnit(x, 'thread_name', x))
    for mu in meter_units:
        mu.setDaemon(1)
        mu.start()
    print('Simulator is running with {NU} units(threads), waiting for requests...'.format(NU=NUM_UNITS))
    while True:
        try:
            client_socket, address = nm.accept_connection()
            if client_socket is 0:
                continue
            # receive TELEGRAM_SIZE bytes
            telegram = client_socket.recv(MBus.TELEGRAM_SIZE)
            while telegram:
                print(telegram)
                for mu in meter_units:  # debug output, remove before release
                    print('Unit #{id}: {val}'.format(id=mu.get_id(), val=mu.get_value()))
                telegram = ':'.join('{:02X}'.format(c) for c in telegram)
                print('Received: {t} from {src}'.format(t=telegram, src=(str(address))))
                orders = MBus.parse_telegram(telegram)
                # respond to client
                if orders[1] == '40':
                    if int(orders[2]) <= len(meter_units):
                        client_socket.sendall(MBus.ACK)
                elif orders[1] == '5B' or orders[1] == '7B':
                    if int(orders[2]) <= len(meter_units):
                        client_socket.sendall(str.encode(str(meter_units[int(orders[2])].get_value())))
                        # client_socket.sendall(MBus.RSP_UD)
                telegram = client_socket.recv(MBus.TELEGRAM_SIZE)
        except KeyboardInterrupt:
            print('\n\nInterrupted by user, exiting...')
            nm.close_server_socket()
            for mu in meter_units:
                mu.shutdown()
                print('Waiting for {tn} to finish...'.format(tn=mu.get_id()))
                mu.join()
                print('{tn} finished successfully.'.format(tn=mu.get_id()))
            sys.exit(1)
        client_socket.close()
    nm.close_server_socket()
