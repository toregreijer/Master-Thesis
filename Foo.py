__author__ = 'Joakim'
from Networking import Networker
raspberry = "192.168.0.125"
n1 = Networker(raspberry)
n1.send('Testicles!')
