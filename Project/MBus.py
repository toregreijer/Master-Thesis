TELEGRAM_SIZE = 5
ACK = b'\xE5'
SND_NKE = b'\x10\x40\x00\x40\x16'       # START:CONTROL:ADDRESS:CHECKSUM:STOP
REQ_UD2 = b'\x10\x5B\x00\x5B\x16'       # START:CONTROL:ADDRESS:CHECKSUM:STOP
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
    return t.split(':')


def build_snd_nke(a):
    # return b'\x10\x40' + str.encode('{:02X}'.format(a)) + b'\x40\x16'
    return b'\x10\x40' + bytearray(a) + b'\x40\x16'
    # still no luck


def build_req_ud2(a):
    pass
