from .a_star import a_star
from copy import deepcopy
import itertools
from code.helpers import helpers


GROUP_SIZE = 3


class hill_climber(a_star):
    """hill climber optimization algorithm"""

    def __init__(self, board, i, filename="./data/output/output.csv"):
        self.board = board

        # read output file if first iteration
        if i == 0:
            self.board.read_output(filename)

        # prior solution's cost
        self.board.cost = helpers.calc_cost(self.board)


    def __repr__(self):
        return "hill_climber"


    def run(self):
        """starts algorithm"""
        # number of nets
        n_nets = len(self.board.nets)

        # group nets into separate lists
        grouped_nets = [self.board.nets[i - GROUP_SIZE: i] for i in range(2, n_nets)]
        
        for nets in grouped_nets:
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
            
    