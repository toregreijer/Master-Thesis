from NetworkCode import NetworkManager
from random import randint
from time import sleep
import threading
import MBus
import sys

NUM_UNITS = 1
client_socket = 0


class MeterUnit(threading.Thread):
    value = 0
    id = 0
    active = 1

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
        while self.active and self.value < 15000:
            self.consume()
            sleep(1)

    def shutdown(self):
        self.active = 0

if __name__ == '__main__':
    print('Starting simulator...')
    var = input('Number of units to simulate: ')
    if var.isdigit():
        NUM_UNITS = int(var)
    else:
        print('Input not recognized as digits, using default value (1) instead.')
    nm = NetworkManager()
    nm.open_server_socket()
    print('Listening for incoming connections on port {} at address {}'.format(str(nm.port), nm.local_host))
    meter_units = []
    print('Starting {NU} meter units'.format(NU=NUM_UNITS))
    for x in range(0, NUM_UNITS):
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
            # print(client_socket)
            telegram = client_socket.recv(1024)
            while telegram:
                # DEBUG OUTPUT
                # print(telegram)
                # for mu in meter_units:  # debug output, remove before release
                    # print('Unit #{id}: {val}'.format(id=mu.get_id(), val=mu.get_value()))

                # telegram = ':'.join('{:02X}'.format(c) for c in telegram)
                mbt = MBus.parse_telegram(telegram)
                print('Received: {t} from {src}'.format(t=mbt, src=(str(address))))

                if mbt.type == 'SND_NKE':
                    if 0 <= int(mbt.fields['address'], 16) < len(meter_units):
                        # if meter_units[int(orders[2])]:
                        print('Responded with E5\n')
                        client_socket.sendall(MBus.ACK)
                elif mbt.type == 'SND_UD':
                    client_socket.sendall(MBus.ACK)
                elif mbt.type == 'REQ_UD2':
                    if 0 <= int(mbt.fields['address'], 16) < len(meter_units):
                        '''
                        response = bytes.fromhex(' '.join('68:15:15:68:08:33:72:'
                                                          '54:42:00:13:B4:09:01:07:E9:28:00:00:'
                                                          '0C:13:98:25:00:00:08:16'.split(':')))
                        '''
                        response = bytes.fromhex(
                            ' '.join(''
                                  '68:DF:DF:68:08:79:72:80:53:08:35:C5:14:01:0D:D1:'
                                  '00:00:00:04:78:44:5C:17:02:04:6D:32:0F:E2:1C:04:13:60:8E:13:00:04:06:10:00:00:00:'
                                  '84:10:06:97:1B:00:00:84:20:06:00:00:00:00:84:30:06:00:00:00:00:84:40:14:00:00:00:'
                                  '00:84:80:40:14:00:00:00:00:04:3B:00:00:00:00:04:2B:00:00:00:00:02:5B:1D:00:02:5F:'
                                  '1D:00:04:61:BA:FF:FF:FF:02:27:D0:02:01:FD:17:00:04:90:28:E8:03:00:00:42:6C:DF:1C:'
                                  '44:13:6D:01:00:00:44:06:00:00:00:00:C4:10:06:01:00:00:00:C4:20:06:00:00:00:00:C4:'
                                  '30:06:00:00:00:00:C4:40:14:00:00:00:00:C4:80:40:14:00:00:00:00:82:01:6C:BF:1C:84:'
                                  '01:13:41:01:00:00:84:01:06:00:00:00:00:84:11:06:00:00:00:00:84:21:06:00:00:00:00:'
                                  '84:31:06:00:00:00:00:84:41:14:00:00:00:00:84:81:40:14:00:00:00:00:'
                                  '74:16'.split(':')))
                        # '''
                        # response = MBus.rsp_ud(mbt.A, meter_units[mbt.A].get_value())
                        # mbt_r = MBus.MBusTelegram(response)
                        # print('Responded with value {} [{}]'.format(
                        #     meter_units[int(mbt.fields['address'])].get_value(), mbt_r))
                        client_socket.sendall(response)
                telegram = client_socket.recv(1024)
        except ConnectionResetError:
            print('\nConnection aborted by other party.')
            client_socket.close()
            continue
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
    print('Simulation over, exiting!')
