__author__ = 'Joakim'
from MeterUnitGateway import MeterUnitGateway
from Networking import Networker


meters = MeterUnitGateway()
# meters.listen()
networker = Networker()
networker.receive()

"""
respond to client
ack_response = b'\xE5'
rsp_ud = (b'\x68\x1D\x1D\x68'           # START:LENGTH:LENGTH:START
          b'\x08\x01\x72'               # CONTROL:ADDRESS:CONTROL_INFO
          b'\x44\x55\x66\x77\x88\x99'   # ACTIVE_DATA
          b'\x11\x02\x00\x00\x00\x00'   # MORE DATA
          b'\x86\x00\x82\xFF\x80\xFF'   # MORE DATA
          b'\x00\x00\x00\x00\x00\x00'   # MORE DATA
          b'\xDA\x0F\xCC\x16')          # DATA:DATA:CHECKSUM:STOP

"""
