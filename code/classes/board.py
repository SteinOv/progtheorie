import csv
import ast
from .gate import Gate
from .net import Net
from copy import deepcopy


class Board:
    """
    handles loading of gates, nets and grid
    main methods for use in algorithms
    """

    def __init__(self, print_csv, netlist_csv):
        self.gates = {}
        self.gate_locations = []
        self.nets = []
        self.width = 0
        self.length = 0
        self.height = 7
        self.cost = 0

        # load gates and nets
        self.load_gates(print_csv)
        self.load_nets(netlist_csv)

        # create grid
        self.grid = self.create_grid(self.width, self.length, self.height)

        # save start state of grid
        self.grid_reserve = deepcopy(self.grid)

    
    def load_gates(self, filename):
        """loads gates from print csv file"""
        # try to open file
        try:
            with open(filename) as file:
                data = csv.reader(file)
                next(data)

                # for every gate
                for line in data:
                    # get id and coordinates
                    gate_id, x, y, z = int(line[0]), int(line[1]), int(line[2]), 0

                    # create Gate object
                    self.gates[gate_id] = Gate(gate_id, (x, y, z))
                    self.gate_locations.append((x, y, z))

                    # set width and length of grid
                    if x > self.width:
                        self.width = x + 1
                    if y > self.length:
                        self.length = y + 1

        except OSError:
            print(f"File {filename} not found")
            raise SystemExit


    def load_nets(self, filename):
        """loads nets from netlist csv file"""
        # try to open file
        try:
            with open(filename) as file:
                data = csv.reader(file)
                next(data)

                # for every net
                for i, line in enumerate(data):
                    # if line is not empty
                    if line:
                        # gates connected by net
                        gate_a, gate_b = self.gates[int(line[0])], self.gates[int(line[1])]

                        # create Net object
                        self.nets.append(Net(self, i, (gate_a, gate_b)))

                        # count number of connections of gate
                        self.gates[gate_a.gate_id].n_connections += 1
                        self.gates[gate_b.gate_id].n_connections += 1
                
            # set priority of nets
            for net in self.nets:
                net.priority_num = net.connect[0].n_connections + net.connect[1].n_connections
                    
        except OSError:
            print(f"File {filename} not found")
            raise SystemExit


    def create_grid(self, width, length, height):
        """creates grid"""
        # create 3D grid
        grid = [[[[] for z in range(height + 1)]
                     for y in range(length + 1)] 
                     for x in range(width + 1)]
        
        # add gate locations to grid
        for gate in self.gates:
            x, y, z = self.gates[gate].loc
            grid[x][y][z].append(-1)
        return grid
    
    
    def reset_grid(self):
        """resets grid"""
        self.grid = deepcopy(self.grid_reserve)

    
    def read_output(self, output_csv):
        """reads output.csv into board"""
        with open(output_csv) as file:
            data = csv.reader(file)
            next(data)

            # for every net in output
            for line in data:

                # stop if at end of file
                if line[0][0] != '(':
                    break

                # search for matching net in self.nets
                match = False
                for net in self.nets:
                    # if matching net found
                    if line[0] == str(net.connect).replace(" ", ""):

                        # save route and add net to grid
                        net.route = ast.literal_eval(line[1])
                        net.length = len(net.route) - 1
                        for x, y, z in net.route:
                            self.grid[x][y][z].append(net)
                        
                        # match found
                        match = True
                        break
                    
                if match == False:
                    print("One or more nets in netlist and output.csv do not match")
                    raise SystemExit
        

    def add_net(self, net):
        """adds net to grid"""
        for x, y, z in net.route:
            self.grid[x][y][z].append(net)
        net.length = len(net.route) - 1

    def rem_net(self, net):
        """removes net from grid"""

        # remove each wire from grid
        for x, y, z in net.route:
            self.grid[x][y][z].remove(net)
        
        # reset net length to 0
        net.length = 0
        net.route = []
