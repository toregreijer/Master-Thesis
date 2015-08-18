__author__ = 'joakim'
from NetworkCode import NetworkManager
import sqlite3

sqlite_file = 'the_great_db.sqlite'
table1 = 'house001'
field1 = 'unit_name'
field2 = 'datetime'
field3 = 'value'

remote_host = '192.168.0.125'
TELEGRAM_SIZE = 255
MBUS_ACK = b'\xE5'
MBUS_SND_NKE = b'\x10\x40\x00\x40\x16'
MBUS_RQD_UD = b'\x00'
MBUS_DATA = (b'\x68\x1D\x1D\x68'           # START:LENGTH:LENGTH:START
             b'\x08\x01\x72'               # CONTROL:ADDRESS:CONTROL_INFO
             b'\x44\x55\x66\x77\x88\x99'   # ACTIVE_DATA
             b'\x11\x02\x00\x00\x00\x00'   # MORE DATA
             b'\x86\x00\x82\xFF\x80\xFF'   # MORE DATA
             b'\x00\x00\x00\x00\x00\x00'   # MORE DATA
             b'\xDA\x0F\xCC\x16')

if __name__ == '__main__':
    # FIND AND OPEN THE DATABASE,
    # IF NONE EXISTS, CREATE A NEW ONE.
    # TODO: CREATE DATABASE!
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    # Creating a new SQLite table with 3 columns
    #c.execute('CREATE TABLE {tn} ({fn1} {ft1} PRIMARY KEY, {fn2} {ft2}, {fn3} {ft3})'
     #         .format(tn=table1, fn1=field1, ft1='TEXT', fn2=field2, ft2='TEXT', fn3=field3, ft3='INTEGER'))

    # Committing changes and closing the connection to the database file
    #conn.commit()
    conn.close()
    #
    # POLLING FOR DATA
    # OPEN A CONNECTION TO THE MBUS MASTER
    nm = NetworkManager()
    nm.open_remote_socket()
    # SEND A PING TO MBUS ADDRESS 0
    tmp = nm.send(MBUS_SND_NKE)
    tmp = ':'.join('{:02x}'.format(c) for c in tmp)
    print('Sent stuff, got [%s] back!' % tmp)
    # SEND 0 TO MBUS MASTER
    tmp = nm.send(b'\x00')
    tmp = ':'.join('{:02x}'.format(c) for c in tmp)
    print('Sent stuff, got [%s] back!' % tmp)
    # SEND A REQUEST FOR DATA TO THE MBUS MASTER,
    # FOR UNIT AT ADDRESS X
    #
    # STORE THE DATA RECEIVED AT THE CORRECT PART OF THE DATABASE
    # TODO: CREATE DB CONNECTION AND STORE DATA
    # CLOSE DOWN THE CONNECTION
    nm.close_remote_socket()
    exit(0)
