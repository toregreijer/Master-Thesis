from NetworkCode import NetworkManager
from DatabaseCode import open_and_store, setup_db
import MBus

remote_host = '192.168.0.196'
port = 11111
list_of_meter_units = []
alive = 1


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
    print('Welcome to the Control Unit, please wait a moment!')
    print('Setting up database...')
    setup_db()
    print('Database ready.')
    nm = NetworkManager()
    # nm.open_remote_socket()
    user_choice = ''
    print('Connection established.')
    while alive:
        # TODO: Add options for settings, and connecting to the MBus here instead
        choice = input('Please select option:\n'
                       '1. Scan MBus for units.\n'
                       '2. Request data from one unit.\n'
                       '3. Print collected data for one unit.\n'
                       '4. Connect to an MBus.\n'
                       '5. Options\n'
                       '6. Speed Test\n'
                       '7. Exit\n'
                       ': ')
        if choice in ('1', 'scan', 's'):
            list_of_meter_units = scan()
        elif choice in ('2', 'request', 'r'):
            # TODO: Sanitize the input
            # while not target.isdigit() and 0 > int(target) > 255:
            target = input('Which unit? [0-255]  ')
            request_data(int(target))
        elif choice in ('3', 'print', 'p'):
            pass
        elif choice in ('4', 'connect', 'c'):
            nm.close_remote_socket()
            nm.open_remote_socket(remote_host, port)
        elif choice in ('5', 'options', 'o'):
            remote_host = input('Remote host? ')
            port = int(input('Port? '))
        elif choice in ('6', 'speed'):
            for i in range(30):
                for u in list_of_meter_units:
                    request_data(u)
        elif choice in ('7', 'exit', 'e'):
            break
    print('Closing the connection...')
    nm.close_remote_socket()
    print('Exiting, goodbye!')
    exit(0)
