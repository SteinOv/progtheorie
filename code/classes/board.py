import csv
from .gate import Gate
from .net import Net
import numpy as np
from copy import deepcopy


class Board:
    """
    main class that handles loading of gates and nets

    attributes:
    """

    def __init__(self, print_csv, netlist_csv):
        """initializes variables"""
        self.gates = {}
        self.gate_locations = []
        self.nets = []
        self.width = 0
        self.length = 0
        self.height = 7
        self.cost = 0

        self.load_gates(print_csv)
        self.grid = self.create_grid(self.width, self.length, self.height)
        self.load_nets(netlist_csv)

        # save the start of grid for algorithm to start over
        self.grid_reserve = deepcopy(self.grid)
        
        
    
    def load_gates(self, filename):
        """load gates from print csv file"""
        try:
            with open(filename) as file:
                data = csv.reader(file)
                next(data)

                for line in data:
                    # get gate with its coordinates
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
        """load nets from netlist csv file"""
        try:
            with open(filename) as file:
                data = csv.reader(file)
                next(data)

                # read through data with enumerate
                for i, line in enumerate(data):
                    # make sure line is not empty
                    if line:
                        # gate objects that are connected
                        gate_a, gate_b = self.gates[int(line[0])], self.gates[int(line[1])]

                        # create net object with id and gates that it connects
                        self.nets.append(Net(self, i, (gate_a, gate_b)))

                        # count number of connections of gate
                        self.gates[gate_a.gate_id].n_connections += 1
                        self.gates[gate_b.gate_id].n_connections += 1
                
            for net in self.nets:
                net.priority_num = net.connect[0].n_connections + net.connect[1].n_connections
                    
        except OSError:
            print(f"File {filename} not found")
            raise SystemExit

    def create_grid(self, width, length, height):
        """creates grid"""
        grid = [[[[] for z in range(height + 1)] for y in range(length + 1)] for x in range(width + 1)]
        
        # add gate locations to grid
        for gate in self.gates:
            x, y, z = self.gates[gate].loc
            grid[x][y][z].append(-1)
        return grid
    
    def reset_grid(self):
        """change the grid back to its starting state"""
        self.grid = deepcopy(self.grid_reserve)

    def is_collision(self, curr_loc, new_loc, goal):
        """
        check if nets are in collision
        returns empty set if not in collision else returns non-empty set
        """
        nets_1 = set(self.grid[curr_loc[0]][curr_loc[1]][curr_loc[2]])
        nets_2 = set(self.grid[new_loc[0]][new_loc[1]][new_loc[2]])
        
        # set is empty if no common element
        collision = nets_1 & nets_2

        # number of extra intersections for move
        n_intersections = 1 if nets_2 and new_loc != goal else 0

        # return true if in collision with wire or gate and number of extra intersections
        return collision or (new_loc in self.gate_locations and not new_loc == goal), n_intersections

    def calc_cost(self):
        '''calculate total cost of net configuration'''
        # combined length of all nets
        length = 0
        for net in self.nets:
            length += net.length

        # convert grid to 2D list
        list_2D = sum(sum(self.grid, []), [])

        # list of grid points with intersections
        intersection_nets = [li for li in list_2D if len(li) > 1 and not li.count(-1)]

        # total intersections
        total_intersections = sum([1 if len(grid_point) == 2 else 2 for grid_point in intersection_nets])

        print(f"total intersections: {total_intersections}")

        # total cost
        self.cost = length + 300 * total_intersections

    def manhattan(self, current_loc, new_loc):
        """calculate manhattan distance"""
        distance = 0
        for i in range(3):
            distance += abs(current_loc[i] - new_loc[i])
        return distance

    def find_new_loc(self, current_loc, move):
        """returns new location based on move"""
        new_loc = []
        for i, value in enumerate(current_loc):
            if i == move[0]:
                new_loc.append(value + move[1])
            else:
                new_loc.append(value)

        return tuple(new_loc)
    

