from .a_star import a_star
from copy import copy, deepcopy
import itertools
from code.helpers import helpers


GROUP_SIZE = 3


class hill_climber(a_star):
    """hill climber optimization algorithm"""

    def __init__(self, board, i, filename="./data/output/output.csv"):
        self.board = board
        self.grouped_nets = []
        
        # read output file if first iteration
        if i == 0:
            self.board.read_output(filename)

        # prior solution's cost
        self.board.cost = helpers.calc_cost(self.board)

        # add intersections to nets and sort by number of intersections
        helpers.add_intersections(self.board.grid)
        self.board.nets.sort(key=lambda net: net.num_of_intersections)
        nets = copy(self.board.nets)
        
        # TODO
        while nets:
            # take net with most intersections
            net = nets.pop()
            group = [net]
            
            i = 0
            # j = -1
            while i < GROUP_SIZE - 1:
                i += 1
                
                # if not enough intersecting nets, add net with most intersections
                try:
                    new_net = net.intersections[i]
                except IndexError:
                    # new_net = self.board.nets[j]
                    break
                    
                # net already in group
                if new_net in group: 
                    break
                    # j += -1
                    # new_net = self.board.nets[j]
                # j += -1
                    
                # add intersecting net to group and remove from board
                group.append(new_net)
                # if new_net in nets: nets.remove(new_net)
            # if len(group) > 1:
            self.grouped_nets.append(group)


    def __repr__(self):
        return "hill_climber"


    def run(self):
        """starts algorithm"""
        # number of nets
        # n_nets = len(self.board.nets)

        

        # group nets into separate lists
        # grouped_nets = [self.board.nets[i - GROUP_SIZE: i] for i in range(2, n_nets)]

        print(f"net groups: {self.grouped_nets}")
        
        for nets in self.grouped_nets:
            # save original route
            best_routes = [net.route for net in nets]

            # new best route if improvement found
            improvement = self.rewire(nets, self.board.cost)
            if improvement:
                best_routes = improvement

            for net in nets:
                # search for route matching to net
                for route in best_routes:
                    if (route[0], route[-1]) == (net.connect[0].loc, net.connect[-1].loc):
                        net.route = route

                self.board.add_net(net)

            self.board.cost = helpers.calc_cost(self.board)


    def rewire(self, nets, best_cost):
        """rewires nets"""
        # all permutations of nets
        permutations = list(itertools.permutations(nets))
        best_permutation = []
        
        solution_found = False

        while permutations:
            # current permutation
            nets = permutations.pop()

            # remove nets from grid
            for net in nets:
                self.board.rem_net(net)
            
            # replace nets
            for net in nets:
                # find solution
                route = self.a_star_search(net)
                if route:
                    solution_found = True
                    net.route = route
                    self.board.add_net(net)
                else:
                    solution_found = False
                    print("skip permutation")
                    break
            
            # no solution for this permutation
            if not solution_found:
                continue

            # check if current permutation is improvement
            rewire_cost = helpers.calc_cost(self.board)
            if rewire_cost < best_cost:
                print(f"improvement found: from {best_cost} to {rewire_cost}")
                best_permutation = [net.route for net in nets]
                self.board.cost = best_cost = rewire_cost
                
        # remove nets from grid
        for net in nets:
            self.board.rem_net(net)
        
        # return best permutation
        return best_permutation
            
    