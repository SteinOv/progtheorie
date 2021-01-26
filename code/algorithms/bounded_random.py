import random
from copy import copy, deepcopy
from code.helpers import helpers


DEVIATION = 25
DEVIATION_INCREASE = 10
MAX_RESETS = 1000
MOVES = [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1)]


class bounded_random:
    """random algorithm with maximum deviation from manhattan distance"""

    def __init__(self, board):
        self.board = board


    def __repr__(self):
        return "bounded_random"


    def run(self):
        """starts algorithm"""
        # allowed deviation for algorithm
        current_deviation = DEVIATION

        no_solution = True

        # continue until solution found
        while no_solution:
            # determine route for each net
            for net in self.board.nets:
                # increase allowed deviation
                current_deviation += DEVIATION_INCREASE

                # starting data
                current_loc, goal = net.connect[0].loc, net.connect[1].loc
                start_distance = self.board.manhattan(current_loc, goal)
                
                net_length = 0
                
                # coordinates of wire, start at gate
                current_route = [current_loc]

                n_resets = 0

                # continue until goal or limit is reached
                while current_loc != goal and n_resets < MAX_RESETS:
                    
                    # make move
                    current_loc = self.move(MOVES.copy(), current_loc, current_route, goal, net_length,
                                     start_distance, current_deviation)
                    
                    # move succesfull
                    if current_loc:
                        current_route.append(current_loc)
                        net_length += 1
                    # move unsuccesfull, reset net route
                    else:
                        n_resets += 1
                        current_loc = net.connect[0].loc
                        current_route = [current_loc]
                        net_length = 0

                # if max resets reached, start over
                if n_resets >= MAX_RESETS:
                    self.board.reset_grid()
                    print(f"got stuck at net: {net}, restarting...")
                    break
                
                # store wire coordinates in net
                net.route = current_route
                net.length = net_length

                # add net to grid
                for x, y, z in current_route:
                    self.board.grid[x][y][z].append(net.net_id)

            # check if solution found
            if n_resets != MAX_RESETS:
                self.board.cost = helpers.calc_cost(self.board)
                no_solution = False


    def valid_move(self, current_route, current_loc, new_loc, goal, 
                   net_length, dist_init, current_deviation):
        """determines if move is valid"""
        # return false if move outside of grid
        grid_dimensions = (self.board.width, self.board.length, self.board.height)
        for i, j in zip(new_loc, grid_dimensions):
            if i > j or i < 0:
                return False

        # requirements
        check_a = not self.board.is_collision(current_loc, new_loc, goal)[0]
        check_b = self.board.manhattan(goal, new_loc) + net_length <= dist_init + current_deviation
        check_c = not new_loc in current_route

        return check_a & check_b & check_c


    def move(self, moves, current_loc, current_route, goal, net_length,
                        start_distance, current_deviation):
        """makes move, returns new location if successfull"""

        move = random.choice(moves)
        moves.remove(move)
        new_loc = self.board.find_new_loc(current_loc, move)

        # move valid, make move
        if self.valid_move(current_route, current_loc, new_loc, goal, 
                            net_length, start_distance, current_deviation):
            # return new location
            return new_loc

        # move invalid, try again
        elif moves:
            return self.move(moves, current_loc, current_route, goal, net_length,
                        start_distance, current_deviation)

        # move invalid and no moves left
        else:
            return False

