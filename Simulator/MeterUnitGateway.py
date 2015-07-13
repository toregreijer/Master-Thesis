from random import randint

__author__ = 'joakim'


class MeterUnitGateway(object):

    id_array = {1: 1000, 2: 2000, 3: 3000}

    def __init__(self):
        # while 1:
        self.consume(randint(1, 2))
        self.parse_data()

    def consume(self, unit_id):
        self.id_array[unit_id] += 100

    def parse_data(self):
        pass
        # Use networker to get incoming data
        # Parse bytes to correct command
        # Send appropriate response, somehow
