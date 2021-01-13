import csv
from classes.gate import Gate
from classes.net import Net
import numpy as np


class Board:
    '''
    main class that handles loading of gates and nets

    attributes:

    '''

    def __init__(self, print_csv, netlist_csv):
        self.gates = {}
        self.nets = []
        self.width = 0
        self.length = 0
        self.height = 7
        self.cost = 0
        self.load_gates(print_csv)
        self.grid = self.create_grid(self.width, self.length, self.height)
        # print(f"length:{self.length}, width:{self.width}, height: {self.height}")
        # print(len(self.grid[0]))
        self.load_nets(netlist_csv)
        
    
    def load_gates(self, filename):
        '''load gates from print csv file'''

        try:
            with open(filename) as file:
                data = csv.reader(file)
                next(data)

                # read through data
                for line in data:
                    gate_id, x, y = int(line[0]), int(line[1]), int(line[2])
                    z = 0

                    # create Gate object
                    self.gates[gate_id] = Gate(gate_id, (x,y,z))

                    # set width and length to highest x and y plus 1
                    if x > self.width:
                        self.width = x + 1
                    if y > self.length:
                        self.length = y + 1
        except OSError:
            print(f"File {filename} not found")
            raise SystemExit

    def load_nets(self, filename):
        '''load nets from netlist csv file'''
        
        try:
            with open(filename) as file:
                data = csv.reader(file)
                next(data)

                # read through data with enumerate
                for i, line in enumerate(data):

                    # gate objects that are connected
                    gate_a, gate_b = self.gates[int(line[0])], self.gates[int(line[1])]

                    # create net object with id and gates that it connects
                    self.nets.append(Net(self, i, (gate_a, gate_b)))

                    # add length of wire to cost
                    self.cost += self.nets[i].length 
        except OSError:
            print(f"File {filename} not found")
            raise SystemExit

    def create_grid(self, width, length, height):
        return [[[[] for z in range(height + 1)] for y in range(length + 1)] for x in range(width + 1)]

    def is_collision(self, coord_1, coord_2):
        '''check if nets are in collision'''
        if len(coord_1) < 3: print(coord_1)
        if len(coord_2) < 3: print(coord_2)
        nets_1 = set(self.grid[coord_1[0]][coord_1[1]][coord_1[2]])
        nets_2 = set(self.grid[coord_2[0]][coord_2[1]][coord_2[2]])

        # returns True, if at least one common element
        return nets_1 & nets_2

    

