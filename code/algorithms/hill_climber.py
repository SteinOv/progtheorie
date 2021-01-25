from .a_star import a_star
from copy import deepcopy
import itertools


GROUP_SIZE = 3

class hill_climber(a_star):

    def __init__(self, board, filename="./data/output/output.csv"):
        self.board = deepcopy(board)
        self.board.read_output(filename)
        self.board.cost = self.board.calc_cost()

    def __repr__(self):
        return "hill_climber"
    
    def run(self):

        # group nets into separate lists
        grouped_nets = zip(*(iter(self.board.nets),) * GROUP_SIZE)
        for nets in grouped_nets:

            # save original route
            best_routes = [net.route for net in nets]
            # print(best_routes)

            # perform hill climber, new best route if improvement found
            improvement = self.rewire(nets, self.board.cost)
            if improvement:
                best_routes = improvement

            # add routes to nets
            for net in nets:
                # search for route matching to net
                for route in best_routes:
                    if route[0], route[-1] == net.connect[0].loc, net.connect[-1].loc
                        net.route = route
                self.board.add_net(net)
                print(net.route)
                # print(f"route: {net.route}, len: {net.length}")
            print(f"41 board cost: {self.board.cost}")    
            self.board.cost = self.board.calc_cost()
            print(f"43 board cost: {self.board.cost}")


    def rewire(self, nets, best_cost):
        """rewires nets"""
        print(f"best cost: {best_cost}")

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
            print(f"best cost: {best_cost}, rewire_cost: {rewire_cost}")
            if rewire_cost < best_cost:
                print(f"improvement found: from {best_cost} to {rewire_cost}")
                best_permutation = [net.route for net in nets]
                self.board.cost = best_cost = rewire_cost
                print(f"board cost: {self.board.cost}")
                
        
        # remove nets from grid
        for net in nets:
            print(net.route)
            self.board.rem_net(net)
        
        # return best permutation
        return best_permutation
            
        