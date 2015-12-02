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
    if a <= 250:
        hex_addr = b(a)
        hex_checksum = b(0x40+a)
        return b'\x10\x40' + hex_addr + hex_checksum + b'\x16'
    else:
        addr = bytes.fromhex(rev(str(a)))
        cs = bytes.fromhex(hex(0x59E + sum(addr))[-2:])
        while len(addr) < 4:
            addr += b'\x00'
        return b'\x68\x0B\x0B\x68\x53\xFD\x52' + addr + b'\xFF\xFF\xFF\xFF' + cs + b'\x16'


def req_ud2(a):
    # TODO: Add functionality to handle both primary and secondary addresses
    if a > 250:
        return b'\x10\x7B\xFD\x78\x16'
    else:
        hex_addr = b(a)
        hex_checksum = b(0x7B+a)
        return b'\x10\x7B' + hex_addr + hex_checksum + b'\x16'
    # else:
        # addr = bytes.fromhex(rev(str(a)))
        # cs = bytes.fromhex(hex(0x5A6 + sum(addr))[-2:])
        # while len(addr) < 4:
        #     addr += b'\x00'
        # return b'\x68\x0B\x0B\x68\x5B\xFD\x52' + addr + b'\xFF\xFF\xFF\xFF' + cs + b'\x16'


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
    # while len(result) < 12:
    #    result += '00'
    return result


def decode_mf(b1, b2):
        h = b2 + b1
        name = \
            chr(((int(h, 16) & 0xFC00)//1024)+64) + \
            chr(((int(h, 16) & 0x3E0)//32)+64) + \
            chr(((int(h, 16) & 0x1F)+64))
        return name


def decode_medium(m):
    list_of_mediums = ['Other', 'Oil', 'Electricity', 'Gas',
                       'Heat (Outlet)', 'Steam', 'Hot Water', 'Water',
                       'Heat Cost Allocator', 'Compressed Air',
                       'Cooling Load Meter (Outlet)', 'Cooling Load Meter (Inlet)',
                       'Heat (Inlet)', 'Heat / Cooling Load Meter',
                       'Bus / System', 'Unknown Medium', 'Reserved',
                       'Reserved', 'Reserved', 'Reserved', 'Reserved',
                       'Reserved', 'Cold Water', 'Dual Water',
                       'Pressure', 'A/D Converter', 'Reserved']
    n = int(m, 16)
    if n >= 32:
        return 'Reserved'
    else:
        return list_of_mediums[n]


def decode_dif(dif):
    dif = int(dif, 16)
    extension_bit = (dif & 0x80) != 0
    # LSB_of_storage = (dif & 0x40) != 0
    function_field = (dif & 0x30) >> 4
    data_field = (dif & 0x0F)

    # The function field gives the type of data as follows:
    function_codes = ['Instantaneous ', 'Maximum ', 'Minimum ', 'Value during error state']

    # The data field shows how the data from the master must be interpreted in respect of length
    # and coding. The following table contains the possible coding of the data field:
    data_codes = ['No data', '8bit Integer', '16bit Integer', '24bit Integer',
                  '32bit Integer', '32bit Real', '48bit Integer', '64bit Integer',
                  'Selection for Readout', '2 digit BCD', '4 digit BCD', '6 digit BCD',
                  '8 digit BCD', 'Variable length', '12 digit BCD', 'Special functions']
    data_length = [0, 1, 2, 3, 4, 4, 6, 8, 0, 1, 2, 3, 4, 1, 6, 0]

    return extension_bit, function_codes[function_field], \
        data_codes[data_field], data_length[data_field]


def decode_dife(dife):
    dife = int(dife, 16)
    extension_bit = (dife & 0x80) != 0
    return extension_bit


def decode_vife(vife):
    vife = int(vife, 16)
    extension_bit = (vife & 0x80) != 0
    return extension_bit


def decode_vif(vif):
    vif = int(vif, 16)
    extension_bit = (vif & 0x80) != 0
    code = (vif & 0x7F) >> 3
    zzz = vif & 0b00000111
    if code == 0:
        quantity = pow(10, (zzz-3))
        description = 'Energy'
        si_unit = '{}Wh'.format(quantity)
    elif code == 1:
        quantity = pow(10, (zzz-3))
        description = 'Energy'
        si_unit = '{}kJ'.format(quantity)
    elif code == 2:
        quantity = pow(10, (zzz-3))
        description = 'Volume'
        si_unit = '{}L'.format(quantity)
    elif code == 3:
        quantity = pow(10, (zzz-3))
        description = 'Mass'
        si_unit = '{}kg'.format(quantity)
    elif code == 4:
        quantity = pow(10, (zzz-3))
        description = 'Time stuff ******************************'
        si_unit = '{}hhh'.format(quantity)
    elif code == 5:
        quantity = pow(10, (zzz-3))
        description = 'Power'
        si_unit = '{}W'.format(quantity)
    elif code == 6:
        quantity = pow(10, (zzz-3))
        description = 'Power'
        si_unit = '{}kJ/h'.format(quantity)
    elif code == 7:
        quantity = pow(10, (zzz-3))
        description = 'Volume Flow'
        si_unit = '{}L/h'.format(quantity)
    elif code == 8:
        quantity = pow(10, (zzz-4))
        description = 'Volume Flow Ext.'
        si_unit = '{}L/min'.format(quantity)
    elif code == 9:
        quantity = pow(10, (zzz-6))
        description = 'Volume Flow Ext.'
        si_unit = '{}L/s'.format(quantity)
    elif code == 10:
        quantity = pow(10, (zzz-3))
        description = 'Mass Flow'
        si_unit = '{}kg/h'.format(quantity)
    elif code == 11:
        quantity = pow(10, (zzz-3))
        description = 'Flow Temperature / Return Temperature  *******'
        si_unit = '{}C'.format(quantity)
    elif code == 12:
        quantity = pow(10, (zzz-3))
        description = 'Temp diff (K)/ External temp (C)'
        si_unit = '{}K'.format(quantity)
    elif code == 13:
        quantity = pow(10, (zzz-3))
        description = 'Pressure (bar)/ Time point (time)/ Units for HCA / Reserved'
        si_unit = '{}L/h'.format(quantity)
    elif code == 14:
        quantity = pow(10, (zzz-3))
        description = 'Averaging Duration (time coded) / Actuality duration'
        si_unit = '{}L/h'.format(quantity)
    elif code == 15:
        quantity = pow(10, (zzz-3))
        description = 'Fabrication Number / Enhanced / Bus Address'
        si_unit = '{}L/h'.format(quantity)
    else:
        quantity = pow(10, (zzz-3))
        description = 'Magic Dust'
        si_unit = '{}kg'.format(quantity)

    return extension_bit, description, si_unit


def pretty_data_block(data_block):
    """ Return a readable string representing a block of data """
    return '\nCoding: {0[0]}\nType: {0[1]}{0[2]}\nValue: {0[3]} {0[4]}\n'.format(data_block)


def pretty_hex(bs):
    if bs is None:
        return
    else:
        return ':'.join([format(x, '02X') for x in bs])


def pretty_print(mbt):
    """ Return a readable string with the important parts of the telegram """
    part_one = 'Address: {} (Hexadecimal)\n' \
               'ID: {}\n' \
               'Manufacturer: {}\n' \
               'Medium: {}\n'.format(mbt.fields['address'],
                                     mbt.fields['id'],
                                     mbt.fields['mf'],
                                     mbt.fields['medium'])
    part_two = ''
    for block in mbt.data_blocks:
        part_two += pretty_data_block(block)

    return part_one + part_two


class MBusTelegram:
    raw = b''
    hex_list = []
    fields = None   # [keywords, id, mf, medium]
    keywords_short = ['start', 'control', 'address', 'checksum', 'stop']
    keywords_long = ['start', 'length', 'length', 'start',
                     'control', 'address', 'control_info']
    fixed_data_header = ['id1', 'id2', 'id3', 'id4', 'mf1', 'mf2',
                         'ver', 'medium', 'access', 'status', 'sig1', 'sig2']
    format = ''
    type = ''

    data_blocks = []    # coding, func, description, value, unit
    mdh = False

    def __init__(self, t):
        self.raw = t
        self.hex_list = [format(x, '02X') for x in t]
        del self.data_blocks[:]
        if len(t) == 1:  # 1 byte, ACK, Slave -> Master
            self.format = 'SINGLE'
            self.type = 'ACK'

        elif len(t) == 5:  # 5 bytes, Short Frame, Master -> Slave
            self.format = 'SHORT'

            # Telegram header
            self.fields = dict(zip(self.keywords_short, self.hex_list))

            # SND_NKE: C = 40.
            if self.fields['control'] == '40':
                self.type = 'SND_NKE'

            # REQ_UD2: C = 5B or 7B.
            elif self.fields['control'] == '5B' or self.fields['control'] == '7B':
                self.type = 'REQ_UD2'

        else:  # More than 5 bytes, Long Frame, SND_UD or RSP_UD. Data transfer, both ways.
            self.format = 'LONG'

            # Telegram header
            self.fields = dict(zip(self.keywords_long, self.hex_list))

            # SND_UD: C = 53 or 73. Long Frame, Master -> Slave
            if self.fields['control'] == '53' or self.fields['control'] == '73':
                self.type = 'SND_UD'

            # RSP_UD: C = 08 or 18. Long Frame, Slave -> Master
            elif self.fields['control'] == '08' or self.fields['control'] == '18':
                self.type = 'RSP_UD'

                # Manufacturer specific data present?
                self.mdh = '0F' in self.hex_list[19:] or '1F' in self.hex_list[19:]

                # Fixed data header
                d = dict(zip(self.fixed_data_header, self.hex_list[7:19]))
                identification = d['id4'] + d['id3'] + d['id2'] + d['id1']
                self.fields.update({'id': identification})
                manufacturer = decode_mf(d['mf1'], d['mf2'])
                self.fields.update({'mf': manufacturer})
                medium = decode_medium(d['medium'])
                self.fields.update({'medium': medium})

                user_data_list = self.hex_list[19:-2]
                while user_data_list:
                    dif = user_data_list.pop(0)
                    ext_d, func, coding, length = decode_dif(dif)
                    if ext_d:
                        dife = user_data_list.pop(0)
                        while decode_dife(dife):  # do dis 0-10 times
                            dife = user_data_list.pop(0)
                    vif = user_data_list.pop(0)
                    ext_v, description, unit = decode_vif(vif)
                    if ext_v:
                        vife = user_data_list.pop(0)
                        while decode_vife(vife):  # do dis 0-10 times
                            vife = user_data_list.pop(0)
                    data_data = ''
                    for x in range(length):
                        data_data = user_data_list.pop(0) + data_data
                    value = 0
                    if data_data:
                        if 'BCD' in coding:
                            value = int(data_data)
                        else:
                            value = int(data_data, 16)
                    user_data_block = [coding, func, description, value, unit]
                    # self.pretty_data_block(user_data_block)
                    self.data_blocks.append(user_data_block)

        assert self.type in TELEGRAM_TYPE
        assert self.format in TELEGRAM_FORMAT
        # TODO: Assert self.CS == calculate_new_CS(raw) ..typ?

    def __str__(self):
        return ':'.join(self.hex_list)
