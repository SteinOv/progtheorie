from .a_star import a_star
from copy import deepcopy
import itertools


GROUP_SIZE = 4

class hill_climber(a_star):

    def __init__(self, board, i, filename="./data/output/output.csv"):
        self.board = deepcopy(board)

        # first iteration, read in output.csv
        if i == 0:
            self.board.read_output(filename)
        self.board.cost = self.board.calc_cost()

    def __repr__(self):
        return "hill_climber"
    
    def run(self):

        # group nets into separate lists
        grouped_nets = list(zip(*(iter(self.board.nets),) * GROUP_SIZE))

        # add remaining nets into last group
        if len(self.board.nets) % GROUP_SIZE:
            grouped_nets.append([self.board.nets[-i] for i in range(1, GROUP_SIZE + 1)])
        
        for nets in grouped_nets:

            # save original route
            best_routes = [net.route for net in nets]

            # perform hill climber, new best route if improvement found
            improvement = self.rewire(nets, self.board.cost)
            if improvement:
                best_routes = improvement

            # add routes to nets
            for net in nets:
                # search for route matching to net
                for route in best_routes:
                    if (route[0], route[-1]) == (net.connect[0].loc, net.connect[-1].loc):
                        net.route = route
                self.board.add_net(net)
            self.board.cost = self.board.calc_cost()


    def rewire(self, nets, best_cost):
        """rewires nets"""

        # gives all possible permutations of nets
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
                    net.route = route
                    self.board.add_net(net)
                    solution_found = True

                # skip permutation
                else:
                    solution_found = False
                    print("skip permutation")
                    break
            
            # no solution found in A* search
            if not solution_found:
                continue

            # check if current permutation is an improvement
            rewire_cost = self.board.calc_cost()
            if rewire_cost < best_cost:
                print(f"improvement found: from {best_cost} to {rewire_cost}")
                best_permutation = [net.route for net in nets]
                self.board.cost = best_cost = rewire_cost
                
        
        # remove nets from grid
        for net in nets:
            self.board.rem_net(net)
        
        # return best permutation
        return best_permutation
            
        