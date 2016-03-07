import MBus
import csv
import re


# print(len('1234'))
# print(bytes.fromhex('123405'))
# print(bytes.fromhex(MBus.rev(str(53412))))
# print(sum(bytes.fromhex('9988FF')))
# print(sum(bytes.fromhex(MBus.rev('9988FF'))))
# foo = bytes.fromhex(str(hex(24))[2:4])  # stupid, use below instead
# bytes_from_hex = bytes.fromhex(format(12, '02X'))           # == b'\x0c'
# manual = b'\x10\x40' + bytes_from_hex + b'\x01'  # b'\x10@\x0c\x...
# readable = ':'.join('{:02X}'.format(x) for x in manual)     # 10:40:0C:86:80:95:49
# list_of_hexes = [hex(h) for h in list(manual)]  # ['0x10', '0x40', '0xc', '0x86', '0x80', '0x95', '0x49']
# XX_list = [format(x, '02X') for x in manual]    # ['10', '40', '0C', '86', '80', '95', '49']
# print('bytes_from_hex: {0}  -  type: {1}'.format(bytes_from_hex, type(bytes_from_hex)))
# print('manual: {0}  -  type: {1}'.format(manual, type(manual)))
# print('readable: {0}  -  type: {1}'.format(readable, type(readable)))
# print('list_of_hexes: {0}  -  type: {1}'.format(list_of_hexes, type(list_of_hexes)))
# print(format(0, 'X'))
# print(int(list_of_hexes[1], 16))
# print(len(manual))
# print(XX_list)
# print(manual)
# print(manual[-1:])
# print([int(x, 16) for x in XX_list])
# print(bytes.fromhex(XX_list[2]))
# print(bytes.fromhex(format(14, '02X')))
# print(MBus.b(0x04+8))
# print(MBus.rsp_ud(1, 1000))
# print('\n'.join(['{:02}:{}{:>10}{:>10}{:>10}'.format(
# x, chr(x+64), hex(x*1024), hex(x*32), hex(x)) for x in range(1, 26)]))
# print(format(0b11010101 >> 4, '08b'))
# print(MBus.pretty_hex(68:15:15:68:08:33:72:54:42:00:13:B4:09:01:07:97:28:00:00:0C:13:91:29:00:00:B3:16))
# foo = MBus.parse_telegram(bytes.fromhex(' '.join('68:15:15:68:08:33:72:54:42:00:'
# '13:B4:09:01:07:97:28:00:00:0C:13:91:29:00:00:B3:16'.split(':'))))
# print(MBus.pretty_print(foo))
# 68:15:15:68:08:33:72:54:42:00:13:B4:09:01:07:97:28:00:00:0C:13:91:29:00:00:B3:16

# unit = "0.01Wh"
# print(unit)
# print(unit[0].isdigit())
# prefix = re.split(r'([a-zA-Z]+)', unit)[0]
# unit = unit.replace(prefix, '')
# print("prefix >{}<".format(prefix))
# print("unit >{}<".format(unit))
