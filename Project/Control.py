from NetworkCode import NetworkManager
from DatabaseCode import open_and_store, setup_db
import sys
import MBus

remote_host = '192.168.0.196'

if __name__ == '__main__':
    try:
        # var = input('Welcome to the Control Unit, shall I proceed?\n')
        # SET UP THE DATABASE FOR FUTURE USE
        setup_db()
        # POLLING FOR DATA
        # OPEN A CONNECTION TO THE MBUS MASTER
        nm = NetworkManager(remote_host)
        nm.open_remote_socket()
        # SEND A PING TO MBUS ADDRESS 0
        addr = 00
        tmp = nm.send(MBus.SND_NKE)
        tmp = ':'.join('{:02x}'.format(c) for c in tmp)
        print('Sent stuff, got [%s] back!' % tmp)

        # SEND A REQUEST FOR DATA TO THE MBUS MASTER,
        # FOR UNIT AT ADDRESS X
        #
        # STORE THE DATA RECEIVED AT THE CORRECT PART OF THE DATABASE

        open_and_store(tmp)

        # CLOSE DOWN THE CONNECTION
        nm.close_remote_socket()
        exit(0)
    except ConnectionRefusedError:
        print('Could not connect! Exiting...')
        sys.exit(0)
