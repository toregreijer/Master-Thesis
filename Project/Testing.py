foo = bytes.fromhex(str(18))
manual = b'\x10\x40\x16' + foo
bar = ':'.join('{:02X}'.format(x) for x in manual)
print('str: {0!s}  -  repr: {0!r}'.format(foo))
print('str: {0!s}  -  repr: {0!r}'.format(manual))
print('str: {0!s}  -  repr: {0!r}'.format(bar))