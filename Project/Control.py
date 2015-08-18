__author__ = 'joakim'
from NetworkCode import NetworkManager

remote_host = '192.168.0.125'
TELEGRAM_SIZE = 255
MBUS_ACK = b'\xE5'
MBUS_DATA = (b'\x68\x1D\x1D\x68'           # START:LENGTH:LENGTH:START
             b'\x08\x01\x72'               # CONTROL:ADDRESS:CONTROL_INFO
             b'\x44\x55\x66\x77\x88\x99'   # ACTIVE_DATA
             b'\x11\x02\x00\x00\x00\x00'   # MORE DATA
             b'\x86\x00\x82\xFF\x80\xFF'   # MORE DATA
             b'\x00\x00\x00\x00\x00\x00'   # MORE DATA
             b'\xDA\x0F\xCC\x16')

if __name__ == '__main__':
    nm = NetworkManager()
    nm.open_remote_socket()
    tmp = nm.send(b'\x10\x40\x00\x40\x16')
    print('Sent stuff, got [%s] back!' % tmp)
    nm.send(b'\x00')
    nm.close_remote_socket()
    exit(0)
