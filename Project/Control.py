__author__ = 'joakim'
from NetworkCode import NetworkManager
import sys
import MBus


if sys.version_info < (3,):
    def b(x):
        return x
else:
    import codecs

    def b(x):
        return codecs.latin_1_encode(x)[0]


remote_host = '192.168.0.125'

if __name__ == '__main__':
    try:
        # POLLING FOR DATA
        # OPEN A CONNECTION TO THE MBUS MASTER
        nm = NetworkManager()
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
        # TODO: CREATE DB CONNECTION AND STORE DATA
        # CLOSE DOWN THE CONNECTION
        nm.close_remote_socket()
        exit(0)
    except ConnectionRefusedError:
        print('Couldn\'t connect! Exiting...')
        sys.exit(0)