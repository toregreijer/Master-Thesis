from NetworkCode import NetworkManager
from DatabaseCode import open_and_store, setup_db
import MBus

remote_host = '192.168.0.196'


def scan():
    """ Ping all addresses and return a list of those that respond """
    list_of_addresses = []
    for x in range(255):
            if ping(x):
                list_of_addresses.append(x)
                print('Discovered unit at address {}!'.format(x))
    return list_of_addresses


def request_data(address):
    """ Send REQ_UD2 to (address), store the response in the database. """
    tmp = nm.send(MBus.req_ud2(address))
    print('Sent request to {0}, got {1} back!'.format(address, tmp))
    print('Storing stuff in database...')
    open_and_store(tmp)
    print('Done!')


def ping(address):
    """ Ping address and return the result, True or False. """
    return nm.send(MBus.snd_nke(address))


if __name__ == '__main__':
    # TODO: Build some simple loop where the user can choose operations and change settings
    print('Welcome to the Control Unit, please wait a moment!\n')
    print('Setting up database...')
    setup_db()
    print('Connecting to MBus...')
    nm = NetworkManager()
    nm.open_remote_socket()

    targets = scan()
    for t in targets:
        request_data(t)

    print('Closing the connection...')
    nm.close_remote_socket()
    print('Exiting, goodbye!')
    exit(0)
