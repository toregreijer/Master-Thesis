# foo = bytes.fromhex(str(hex(24))[2:4])  # stupid, use below instead
foo = bytes.fromhex(format(24, 'X'))
manual = b'\x10\x40\x16' + foo + bytes.fromhex('FF')
bar = ':'.join('{:02X}'.format(x) for x in manual)
list_of_hexes = [hex(h) for h in list(manual)]
print('str: {0!s}  -  type: {1}'.format(foo, type(foo)))
print('str: {0!s}  -  type: {1}'.format(manual, type(manual)))
print('str: {0!s}  -  type: {1}'.format(bar, type(bar)))
print('str: {0!s}  -  type: {1}'.format(list_of_hexes, type(list_of_hexes)))
print(format(0, 'X'))
