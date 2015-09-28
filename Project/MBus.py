from random import randint


TELEGRAM_SIZE = 5
TELEGRAM_FORMAT = ['SINGLE', 'SHORT', 'LONG']
TELEGRAM_TYPE = ['ACK', 'SND_NKE', 'SND_UD', 'REQ_UD2', 'RSP_UD']
ACK = b'\xE5'
data_params = (b'\x42\x00\x00\x00'           # UNIT ID NUMBER
               b'\x42\x42'                   # MANUFACTURERS MARK
               b'\x04'                       # VERSION NUMBER OF MBUS INTERFACE FW
               b'\x02'                       # MEDIUM: ELECTRICITY
               b'\x00'                       # ACCESS NUMBER: 00->FF->00
               b'\x00'                       # MBUS INTERFACE STATUS
               b'\x00\x00'                   # SIGNATURE, NOT USED, ALWAYS 0000
               b'\x86\x00\x82\xFF\x80\xFF'   # READOUT DATA PARAMETRISED
               b'\x00')

# SND_NKE = b'\x10\x40\x00\x40\x16'       # START:CONTROL:ADDRESS:CHECKSUM:STOP
# REQ_UD2 = b'\x10\x5B\x00\x5B\x16'       # START:CONTROL:ADDRESS:CHECKSUM:STOP

RSP_UD = (b'\x68\x1D\x1D\x68'           # START:LENGTH:LENGTH:START
          b'\x08\x01\x72'               # CONTROL:ADDRESS:CONTROL_INFO
          b'\x42\x00\x00\x00'           # UNIT ID NUMBER
          b'\x42\x42'                   # MANUFACTURERS MARK
          b'\x04'                       # VERSION NUMBER OF MBUS INTERFACE FW
          b'\x02'                       # MEDIUM: ELECTRICITY
          b'\x00'                       # ACCESS NUMBER: 00->FF->00
          b'\x00'                       # MBUS INTERFACE STATUS

          b'\x00\x00'                   # SIGNATURE, NOT USED, ALWAYS 0000
          b'\x86\x00\x82\xFF\x80\xFF'   # READOUT DATA PARAMETRISED
          b'\x00'                       # PHASE SOMETHING

          b'\x45\x00\x00\x00\x00\x00'   # VALUE
          b'\x0F'                       # DIF: 0F = no more data; 1F = other data to send
          b'\xCC'                       # CHECKSUM
          b'\x16')                      # STOP CHARACTER


def parse_telegram(t):
    if t:
        return MBusTelegram(t)
    else:
        return


def snd_nke(a):
    hex_addr = b(a)                 # bytes.fromhex(format(a, '02X'))
    hex_checksum = b(0x40+a)        # bytes.fromhex(format(0x40 + a, '02X')[-2:])
    return b'\x10\x40' + hex_addr + hex_checksum + b'\x16'


def snd_nke_2(a):
    addr = bytes.fromhex(rev(str(a)))
    cs = bytes.fromhex(hex(0x5BE + sum(addr))[-2:])
    while len(addr) < 8:
        addr += b'\x00'
    return b'\x68\x0B\x0B\x68\x73\xFD\x52' + addr + b'\xFF\xFF\xFF\xFF' + cs + b'\x16'


def req_ud2(a):
    hex_addr = b(a)                 # bytes.fromhex(format(a, '02X'))
    hex_checksum = b(0x5B+a)        # bytes.fromhex(format(0x5B + a, '02X')[-2:])
    return b'\x10\x5B' + hex_addr + hex_checksum + b'\x16'


def rsp_ud(a, value):
    start = 0x68                        # int
    stop = 0x16                         # int
    control = 0x08                      # int
    dif = 0x0F                          # int
    ci = 0x72                           # int
    address = a                         # int
    data = bytes.fromhex(rev(format(value, '02X')))    # low order first
    first_rnd_block = b''                  # bytes
    for i in range(20):
        first_rnd_block += b(randint(0, 100))
    length = len(data + data_params)+4

    checksum = bytes.fromhex(hex(control + address + ci + dif + sum(data_params) + sum(data))[-2:])

    telegram = b(start) + b(length) + b(length) + b(start) + \
        b(control) + b(address) + b(ci) + data_params + data + \
        b(dif) + checksum + b(stop)

    return telegram


def b(x):
    """ Take an integer value and return the hexadecimal representation in bytes """
    return bytes.fromhex(format(x, '02X')[-2:])


def rev(h):
    """ Take a string with hex values and change low- to high-order. """
    original = h
    result = ''
    if len(h) % 2 != 0:
        original = '0' + original
    for i in range(len(original)//2):
        result = original[:2] + result
        original = original[2:]
    while len(result) < 12:
        result += '00'
    return result


class MBusTelegram:
    raw = b''
    hex_list = []
    L = 0
    C = 0
    A = 0
    CI = 0
    CS = 0
    format = ''
    payload = ''
    type = ''

    def __init__(self, t):
        self.raw = t
        self.hex_list = [format(x, '02X') for x in t]  # [hex(h).upper() for h in list(b)]
        if len(t) == 1:
            self.format = 'SINGLE'
            self.type = 'ACK'
        elif len(t) == 5:
            # 5 bytes, short telegram, SND_NKE or REQ_UD2. Received by sim only.
            self.format = 'SHORT'
            self.C = self.hex_list[1]
            self.A = int(self.hex_list[2], 16)  # Should A be 0 to 255(int), or '00' to 'FF'(str)?
            self.CS = self.hex_list[3]
            if self.hex_list[1] == '40':
                self.type = 'SND_NKE'
            elif self.hex_list[1] == '5B' or self.hex_list[1] == '7B':
                self.type = 'REQ_UD2'
        else:
            # Length > 5, long telegram, SND_UD or RSP_UD. Data transfer, both ways.
            self.format = 'LONG'
            self.A = int(self.hex_list[5], 16)
            self.C = self.hex_list[4]
            self.L = self.hex_list[1]  # TODO: Do we need these?
            self.CI = self.hex_list[6]
            self.CS = self.hex_list[-1:]
            # SND_UD: C==53 / 73 Long Frame Master send data to Slave
            if self.C == '53' or self.C == '73':
                self.type = 'SND_UD'
            # RSP_UD: C==08 / 18 Long Frame Data transfer from Slave to Master
            elif self.C == '08' or self.C == '18':
                self.type = 'RSP_UD'
        assert self.type in TELEGRAM_TYPE
        assert self.format in TELEGRAM_FORMAT
        # TODO: Assert self.CS == calculate_new_CS(raw) ..typ?

    def __str__(self):
        # return ':'.join('{:02X}'.format(c) for c in self.raw)
        return ':'.join(self.hex_list)
