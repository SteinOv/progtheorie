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
        else:
            for net in self.board.nets:
                net.intersections = []
                net.num_of_intersections = 0

        # prior solution's cost
        self.board.cost = helpers.calc_cost(self.board)

        # create groups for hill climber
        self.create_groups()


    def __repr__(self):
        return "hill_climber"


    def run(self):
        """starts algorithm"""
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
                self.board.remove_net(net)
            
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
            self.board.remove_net(net)
        
        # return best permutation
        return best_permutation
            
    
    def create_groups(self):
        """creates groups based on number of intersections"""
        # add intersections to nets
        helpers.add_intersections(self.board.grid)

        # sort by number of intersections
        self.board.nets.sort(key=lambda net: net.num_of_intersections, reverse=True)
        
        # group nets
        nets = copy(self.board.nets)
        for net in nets:
            # get net with most intersections
            group = [net]
            
            # add intersecting nets to group
            for i in range(GROUP_SIZE - 1):
                # determine this group's size
                if i >= len(net.intersections):
                    break
                new_net = net.intersections[i]
                    
                if new_net in group:
                    continue
                
                group.append(new_net)

            self.grouped_nets.append(group)