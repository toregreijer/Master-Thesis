from NetworkCode import NetworkManager
from DatabaseCode import open_and_store, setup_db
import sys
import MBus

remote_host = '192.168.0.196'

if __name__ == '__main__':
    try:
        print('Welcome to the Control Unit, please wait a moment!\n')
        # SET UP THE DATABASE FOR FUTURE USE
        print('Setting up database...')
        setup_db()
        # POLLING FOR DATA
        # OPEN A CONNECTION TO THE MBUS MASTER
        print('Connecting to MBus...')
        nm = NetworkManager()
        nm.open_remote_socket()
        # SEND A PING TO MBUS ADDRESS 0
        # tmp = nm.send(MBus.SND_NKE)
        # tmp = ':'.join('{:02X}'.format(c) for c in tmp)
        # if tmp:
        print(MBus.build_snd_nke(0))
        tmp = nm.send(MBus.REQ_UD2)
        print('Sent stuff, got {} back!'.format(int(tmp)))

        # STORE THE DATA RECEIVED AT THE CORRECT PART OF THE DATABASE
        print('Storing stuff in database...')
        open_and_store(tmp)
        # CLOSE DOWN THE CONNECTION
        print('Closing the connection...')
        nm.close_remote_socket()
        print('Exiting, goodbye!')
        exit(0)
    except ConnectionRefusedError:
        print('Could not connect! (Connection refused) Exiting...')
        sys.exit(0)
    except TimeoutError:
        print('Could not connect! (Timeout) Exiting...')
        sys.exit(0)
