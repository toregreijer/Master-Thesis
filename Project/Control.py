from NetworkCode import NetworkManager
from DatabaseCode import open_and_store, setup_db
from time import sleep
import MBus
import csv


remote_host = '192.168.1.41'
list_of_meter_units = []
alive = 1


def scan():
    """ Ping all addresses and return a list of those that respond """
    list_of_addresses = []
    for x in range(0, 250):
        sleep(1)
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
    # print(ping(address))
    # sleep2(1)
    # if address > 250:
    #    mbus_response = nm.send(MBus.req_ud2(0xFD))
    # else:
    mbus_response = nm.send(MBus.req_ud2(address))
    print('Sent: {}'.format(MBus.pretty_hex(MBus.req_ud2(address))))
    print('Received: {}'.format(MBus.pretty_hex(mbus_response)))
    if mbus_response:
        mbus_response = MBus.parse_telegram(mbus_response)
        print(MBus.pretty_print(mbus_response))  # Change to debug only

        print('Storing stuff in database...')
        open_and_store(mbus_response)
    else:
        print('Sent request to {}, but did not get a response.'.format(address))


def ping(address):
    """ Ping address and return the result, True or False. """
    address = int(address)
    print('Sent: {}'.format(MBus.parse_telegram(MBus.snd_nke(address))))
    return MBus.parse_telegram(nm.send(MBus.snd_nke(address)))


def send_custom(t):
    response = nm.send(bytes.fromhex(t))
    if response is None:
        return 'No response'
    else:
        return MBus.parse_telegram(response)


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
        choice = input('Please select option:\n'
                       '1. Scan MBus for units.\n'
                       '2. Request data from one unit.\n'
                       '3. Ping one unit.\n'
                       '4. Get addresses from file.\n'
                       '5. Custom telegram\n'
                       '6. Collect data\n'
                       '7. Exit\n'
                       ': ')
        if choice in ('1', 'scan', 's'):
            list_of_meter_units = scan()
        elif choice in ('2', 'request', 'r'):
            target = int(input('Which unit? '))
            request_data(target)
        elif choice in ('3', 'ping', 'p'):
            target = int(input('Which unit? '))
            print(ping(target))
        elif choice in ('4', 'get', 'g'):
            target = 'list_of_devices.csv'  # input('Which file? ')
            list_of_meter_units = read_file(target)
            print(list_of_meter_units)
        elif choice in ('5', 'custom', 'c'):
            txt = input(': ')
            print(send_custom(txt))
        elif choice in ('6', 'data', 'd'):
            while True:
                for i in range(1, 250):
                    request_data(i)
                    sleep(15)
        elif choice in ('7', 'exit', 'e'):
            break
    print('Exiting, goodbye!')
    exit(0)
