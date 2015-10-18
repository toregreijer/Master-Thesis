from NetworkCode import NetworkManager
from DatabaseCode import open_and_store, setup_db
from datetime import datetime
import MBus
import csv

remote_host = '192.168.1.41'
port = 2401
list_of_meter_units = []
alive = 1


def scan():
    """ Ping all addresses and return a list of those that respond """
    list_of_addresses = []
    for x in range(1, 250):
            if ping(x):
                list_of_addresses.append(x)
                print('Discovered unit at address {}!'.format(x))
    return list_of_addresses


def scan_secondary():
    """ Ping all addresses and return a list of those that respond """
    list_of_addresses = []
    for x in range(11111111, 99999999):
            if ping(x):
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
    address = int(address)
    if address > 250:
        print('Sent: {}'.format(MBus.parse_telegram(MBus.snd_nke_2(address))))
        return MBus.parse_telegram(nm.send(MBus.snd_nke_2(address)))
    else:
        print('Sent: {}'.format(MBus.parse_telegram(MBus.snd_nke(address))))
        return MBus.parse_telegram(nm.send(MBus.snd_nke(address)))


def read_file(file):
    res = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[1].isdigit():
                res.append(int(row[1]))
    return res

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
                       '4. Get addresses from file.\n'
                       '5. Options\n'
                       '6. Speed Test\n'
                       '7. Exit\n'
                       ': ')
        if choice in ('1', 'scan', 's'):
            list_of_meter_units = scan()
        elif choice in ('2', 'request', 'r'):
            target = input('Which unit?')
            request_data(int(target))
        elif choice in ('3', 'ping', 'p'):
            target = int(input('Which unit? '))
            print(ping(target))
        elif choice in ('4', 'get', 'g'):
            target = 'list_of_devices.csv'  # input('Which file? ')
            list_of_meter_units = read_file(target)
            print(list_of_meter_units)
        elif choice in ('5', 'options', 'o'):
            remote_host = input('Remote host? ')
            port = int(input('Port? '))
        elif choice in ('6', 'speed'):
            for i in range(3):
                for u in list_of_meter_units:
                    ping(u)
                    # request_data(u)
        elif choice in ('7', 'exit', 'e'):
            break
    print('Exiting, goodbye!')
    exit(0)
