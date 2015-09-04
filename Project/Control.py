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

        for x in range(1):
            # SEND A PING TO MBUS ADDRESS X
            tmp = None
            tmp = nm.send(MBus.snd_nke(x))
            # IF THERE IS A UNIT AT ADDRESS X, REQUEST ITS DATA
            if tmp:
                tmp = nm.send(MBus.req_ud2(x))
                print('Sent stuff, got {} back!'.format(int(tmp)))
                # STORE THE DATA RECEIVED AT THE CORRECT PART OF THE DATABASE
                print('Storing stuff in database...')
                open_and_store(tmp)
            else:
                print('No answer at {}!'.format(x))

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


def initialize():
    # TODO: Put the setting up code here.
    pass


def scan():
    # TODO: Ping address 0 through 255, store addresses that responds.
    pass


def request_data(address):
    # TODO: Send REQ_UD2 to (address), store the response in the database.
    pass


def ping(address):
    # TODO: As scan, but for only one (address).
    pass

