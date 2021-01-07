import csv
from gate import Gate
from net import Net

class Board:
    '''
    Main class that handles loading of gates and nets
    '''

    def __init__(self):
        self.gates = {}
        self.nets = {}
        self.width = 0
        self.length = 0
        self.height = None
    
    def load_gates(self, filename):
        '''Load gates from print csv file'''

        with open(filename) as file:
            data = csv.reader(file)
            next(data)

            # Read through data
            for line in data:
                gate_id, x, y = int(line[0]), int(line[1]), int(line[2])

                # Create Gate object
                self.gates[gate_id] = Gate(gate_id, (x, y))

                # Set width and length to highest x and y plus 1
                if x > self.width:
                    self.width = x + 1
                if y > self.length:
                    self.length = y + 1

    def load_nets(self, filename):
        '''Load nets from netlist csv file'''

        with open(filename) as file:
            data = csv.reader(file)
            next(data)

            # Read through data with enumerate
            for i, line in enumerate(data):

                #Gate objects that are connected
                gate_a, gate_b = self.gates[int(line[0])], self.gates[int(line[1])]

                #Create net object with id and gates that it connects
                self.nets[i] = Net(i, (gate_a, gate_b))