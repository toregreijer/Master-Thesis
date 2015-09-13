import MBus
m = MBus.rsp_ud(1, 69)
mbt = MBus.MBusTelegram(m)
print(mbt)
print(MBus.rev(format(69, '02X')))
print(bytes.fromhex(MBus.rev(format(3415, '02X'))))
# print(sum(bytes.fromhex('9988FF')))
# print(sum(bytes.fromhex(MBus.rev('9988FF'))))
# foo = bytes.fromhex(str(hex(24))[2:4])  # stupid, use below instead
bytes_from_hex = bytes.fromhex(format(12, '02X'))           # == b'\x0c'
manual = b'\x10\x40' + bytes_from_hex + b'\x01'  # b'\x10@\x0c\x...
readable = ':'.join('{:02X}'.format(x) for x in manual)     # 10:40:0C:86:80:95:49
list_of_hexes = [hex(h) for h in list(manual)]  # ['0x10', '0x40', '0xc', '0x86', '0x80', '0x95', '0x49']
XX_list = [format(x, '02X') for x in manual]    # ['10', '40', '0C', '86', '80', '95', '49']
print('bytes_from_hex: {0}  -  type: {1}'.format(bytes_from_hex, type(bytes_from_hex)))
print('manual: {0}  -  type: {1}'.format(manual, type(manual)))
print('readable: {0}  -  type: {1}'.format(readable, type(readable)))
print('list_of_hexes: {0}  -  type: {1}'.format(list_of_hexes, type(list_of_hexes)))
# print(format(0, 'X'))
# print(int(list_of_hexes[1], 16))
# print(len(manual))
print(XX_list)
# print([int(x, 16) for x in XX_list])
# print(bytes.fromhex(XX_list[2]))
# print(bytes.fromhex(format(14, '02X')))
# print(MBus.b(0x04+8))
# print(MBus.rsp_ud(1, 1000))
"""
one = format(12345, '02X')
print(one)
two = ''
for i in range(len(one)//2):
    two = one[:2] + two
    one = one[2:]
    # two += one[len(one)-2:len(one)]
    # one = one[0:len(one)-2]
print(two)
four = int('3039', 16)
print(four)
"""
"""
for i in range(60, 150):
    ii = format(i, '02X')
    print('{} == {}'.format(ii, bytes.fromhex(ii)))
"""
