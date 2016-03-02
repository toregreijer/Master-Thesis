import re
from random import randint
from MBusExtensions import decode_vif, decode_vife, decode_vife_a, decode_vife_b


TELEGRAM_SIZE = 5
TELEGRAM_FORMAT = ['SINGLE', 'SHORT', 'LONG']
TELEGRAM_TYPE = ['ACK', 'SND_NKE', 'SND_UD', 'REQ_UD2', 'RSP_UD']
ACK = b'\xE5'


def parse_telegram(t):
    if t:
        return MBusTelegram(t)
    else:
        return


def b(x):
    """ Take an integer value and return the 2 last digits of the hexadecimal representation in bytes
     :param x: integer value to convert """
    return bytes.fromhex(format(x, '02X')[-2:])


def rev(h):
    """ Take a string with hex values and change low- to high-order.
     :param h: ... """
    original = h
    result = ''
    if len(h) % 2 != 0:
        original = '0' + original
    for i in range(len(original)//2):
        result = original[:2] + result
        original = original[2:]
    return result


def random_byte(max_value=200):
    return b(randint(1, max_value))


def snd_nke(a):
    if a <= 250:
        addr = b(a)
        cs = b(0x40 + a)
        return b'\x10\x40' + addr + cs + b'\x16'
    else:
        addr = bytes.fromhex(rev(str(a)))
        cs = b(0x59E + sum(addr))
        while len(addr) < 4:
            addr += b'\x00'
        return b'\x68\x0B\x0B\x68\x53\xFD\x52' + addr + b'\xFF\xFF\xFF\xFF' + cs + b'\x16'


def req_ud2(a):
    if a > 250:
        return b'\x10\x7B\xFD\x78\x16'
    else:
        hex_addr = b(a)
        hex_checksum = b(0x7B+a)
        return b'\x10\x7B' + hex_addr + hex_checksum + b'\x16'


def rsp_ud():
    """
    VARIABLE DATA BLOCK
    BITS!
    DIF = 04 = 0000 0100 = not ext, LSB of storage is 0, function is instantaneous value, data is 32bit int.
    VIB = no ext, then 7 random bits, from 000 0000 to 0110 1011 (int 107)
    DATA = 32bit int = 4 random bytes
    """
    address = random_byte()
    unit_id = random_byte(153) + random_byte(153) + random_byte(153) + random_byte(153)
    manufacturer = random_byte() + random_byte()
    medium = random_byte(10)
    data = random_byte() + random_byte() + random_byte() + random_byte()
    vib = random_byte(107)
    cs = b(sum(b'\x08' + address + b'\x72' + unit_id + manufacturer + b'\x01' +
               medium + b'\x01\x00\x00\x00' + b'\x04' + vib + data))

    return b'\x68\x15\x15\x68\x08' + address + b'\x72' + \
           unit_id + manufacturer + b'\x01' + medium + b'\x01\x00\x00\x00' + \
           b'\x04' + vib + data + cs + b'\x16'


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
    # TODO: "Variable length" and "Special functions" code need further handling."
    dif = int(dif, 16)
    # Shows if there's a DIFE following this DIF.
    extension_bit = (dif & 0x80) != 0
    # Least significant bit of storage number. 0: Actual value, 1: historic value. Higher numbers requires DIFE.
    lsb_of_storage = (dif & 0x40) >> 6
    # The function field gives the type of data as follows.
    function_field = (dif & 0x30) >> 4
    function_codes = ['Instantaneous value', 'Maximum value', 'Minimum value', 'Value during error state']
    # The data field shows how the data from the master must be interpreted in respect of length
    # and coding. The following table contains the possible coding of the data field:
    data_field = (dif & 0x0F)
    data_codes = ['No data', '8bit Integer', '16bit Integer', '24bit Integer',
                  '32bit Integer', '32bit Real', '48bit Integer', '64bit Integer',
                  'Selection for Readout', '2 digit BCD', '4 digit BCD', '6 digit BCD',
                  '8 digit BCD', 'Variable length', '12 digit BCD', 'Special functions']
    data_length = [0, 1, 2, 3, 4, 4, 6, 8, 0, 1, 2, 3, 4, 1, 6, 0]

    return extension_bit, lsb_of_storage, function_codes[function_field], \
        data_codes[data_field], data_length[data_field]


def decode_dife(dife):
    # TODO: Parse the other 7 bits.
    dife = int(dife, 16)
    # Shows if there's another DIFE following this one.
    extension_bit = (dife & 0x80) != 0
    # Next most significant bit of the device subunit, from least to most, I think.
    subunit = (dife & 0x40) >> 6
    # Tariff code..?
    tariff = (dife & 0x30) >> 4
    # Next most significant bit of the storage number, from least to most, I think.
    storage_bits = (dife & 0x0F)

    return extension_bit, subunit, tariff, storage_bits


def combine_value_and_unit(value, unit):
    # Check to see if a conversion is needed
    # If so, split the prefix and suffix,
    # returning the value multiplied with the prefix, and the suffix
    if unit:
        if unit[0].isdigit():
            prefix = re.split(r'([a-zA-Z]+)', unit)[0]
            unit = unit.replace(prefix, '')
            return int(value*float(prefix)), unit
    return value, unit


def pretty_data_block(data_block):
    """ Return a readable string representing a block of data
     :param data_block: ... """
    return '\nCoding: {0[0]}\n' \
           'Function: {0[1]}\n' \
           'Description: {0[2]}\n' \
           'Value: {0[3]} {0[4]}\n' \
           'Subunit: {0[5]}\n' \
           'Tariff: {0[6]}\n' \
           'Storage Number: {0[7]}\n'.format(data_block)


def pretty_hex(bs):
    if bs is None:
        return
    else:
        return ':'.join([format(x, '02X') for x in bs])


def pretty_print(mbt):
    """ Return a readable string with the important parts of the telegram
    :param mbt: mbus telegram """
    # TODO: Subunit, tariff, and storage is only interesting if there was a DIF, so they aren't 0 0 0.
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
                    # Read and parse the DIF
                    dif = user_data_list.pop(0)
                    ext_d, lsb_of_storage, func, coding, length = decode_dif(dif)
                    # After the DIF is parsed, parse 0-10 DIFE's.
                    tmp_subunit = 0
                    tmp_tariff = 0
                    tmp_storage = 0
                    dife_number = 0
                    while ext_d:
                        dife = user_data_list.pop(0)
                        ext_d, subunit, tariff, storage = decode_dife(dife)
                        if dife_number == 0:
                            tmp_subunit = subunit
                            tmp_tariff = tariff
                            tmp_storage = storage
                        else:
                            tmp_subunit += (subunit << 1)
                            tmp_tariff += (tariff << 2)
                            tmp_storage += (storage << 4)
                        dife_number += 1
                    final_subunit = tmp_subunit
                    final_tariff = tmp_tariff
                    final_storage = (tmp_storage << 1) + lsb_of_storage

                    # Read and parse the VIF
                    vif = user_data_list.pop(0)
                    ext_v, description, unit = decode_vif(vif)
                    # After the VIF is parsed, parse 0-10 VIFE's.
                    # Check to see if an extended VIF code needs to be read from the first VIFE
                    if description.startswith('EXT_A'):
                        vife = user_data_list.pop(0)
                        ext_v, description, unit = decode_vife_a(vife)
                    if description.startswith('EXT_B'):
                        vife = user_data_list.pop(0)
                        ext_v, description, unit = decode_vife_b(vife)
                    # TODO: Handle Manufacturer specific coding, plain ascii, and other weird stuff
                    while ext_v:
                        vife = user_data_list.pop(0)
                        ext_v, description, unit = decode_vife(vife)

                    # After the data record header is done, parse the actual data.
                    data_data = ''
                    for x in range(length):
                        data_data = user_data_list.pop(0) + data_data
                    value = 0
                    if data_data:
                        if 'BCD' in coding:
                            value = int(data_data)
                        else:
                            value = int(data_data, 16)
                    value, unit = combine_value_and_unit(value, unit)
                    # TODO: Subunit, tariff, and storage is only interesting if there was a DIFE, so they aren't 0 0 0.
                    user_data_block = [coding, func, description, value, unit,
                                       final_subunit, final_tariff, final_storage]
                    # self.pretty_data_block(user_data_block)
                    self.data_blocks.append(user_data_block)

        assert self.type in TELEGRAM_TYPE
        assert self.format in TELEGRAM_FORMAT

    def __str__(self):
        return ':'.join(self.hex_list)
