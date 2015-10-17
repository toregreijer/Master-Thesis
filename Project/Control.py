from NetworkCode import NetworkManager
from DatabaseCode import open_and_store, setup_db
from datetime import datetime
import MBus

remote_host = '192.168.1.41'
port = 2401
list_of_meter_units = []
alive = 1


def scan():
    """ Ping all addresses and return a list of those that respond """
    list_of_addresses = []
    for x in range(51, 52):
            if ping(x):
                list_of_addresses.append(x)
                print('Discovered unit at address {}!'.format(x))
    return list_of_addresses


def scan_secondary():
    """ Ping all addresses and return a list of those that respond """
    list_of_addresses = []
    for x in range(0, 1000):
            if ping_secondary_addr(x):
                list_of_addresses.append(x)
                print('Discovered unit at address {}!'.format(x))
    return list_of_addresses


def request_data(address):
    """ Send REQ_UD2 to (address), store the response in the database. """
    # rq = MBus_Telegram(address, 'REQ_UD2'))
    # tmp = nm.send(rq.raw)
    tmp = nm.send(MBus.req_ud2(address))
    if tmp:
        tmp = MBus.parse_telegram(tmp)
        print('{}: Sent request to {}, got {} back!'.format(datetime.now(), address, tmp))
        print(tmp.pretty_print())

        # TODO: Parse the input, so we can store it accurately
        print('Storing stuff in database...')
        open_and_store(tmp.raw)
    else:
        print('{}: Sent request to {}, but did not get a response.'.format(datetime.now(), address))
    print('Done!')


def ping(address):
    """ Ping address and return the result, True or False. """
    print('Sent: {}'.format(MBus.snd_nke(address)))
    return MBus.parse_telegram(nm.send(MBus.snd_nke(address)))


def ping_secondary_addr(address):
    print('Sent: {}'.format(MBus.snd_nke_2(address)))
    return MBus.parse_telegram(nm.send(MBus.snd_nke_2(address)))


if __name__ == '__main__':
    print('Welcome to the Control Unit, please wait a moment!')
    print('Setting up database...')
    setup_db()
    print('Database ready.')
    nm = NetworkManager(remote_host)
    # nm.open_remote_socket(remote_host, port)
    user_choice = ''
    # print('Connection established.')
    while alive:
        # TODO: Add options for settings, and connecting to the MBus here instead
        choice = input('Please select option:\n'
                       '1. Scan MBus for units.\n'
                       '2. Request data from one unit.\n'
                       '3. Ping one unit.\n'
                       '4. Placeholder.\n'
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
        elif choice in ('3', 'ping', 'p'):
            target = int(input('Which unit? '))
            if target > 250:
                c = ping_secondary_addr(target)
            else:
                c = ping(int(target))
            print(c)
        elif choice in ('4', 'connect', 'c'):
            target = input('Which unit? ')
            print(ping_secondary_addr(int(target)))
        elif choice in ('5', 'options', 'o'):
            remote_host = input('Remote host? ')
            port = int(input('Port? '))
        elif choice in ('6', 'speed'):
            for i in range(30):
                for u in list_of_meter_units:
                    request_data(u)
        elif choice in ('7', 'exit', 'e'):
            break
    print('Exiting, goodbye!')
    exit(0)
