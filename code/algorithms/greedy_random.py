import random
from copy import copy, deepcopy

DEVIATION = 25
DEVIATION_INCREASE = 10
MAX_RESETS = 500
MOVES = [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1)]

class greedy_random:
    """combination of random and greedy algorithm using manhattan distance"""

    def __init__(self, board):
        self.board = deepcopy(board)

    def __repr__(self):
        return "greedy_random"

    def run(self):
        """starts algorithm"""
        # allowed deviation for algorithm
        current_deviation = DEVIATION

        no_solution = True
        n_tries = 0

        # continue until solution found
        while no_solution:
            # determine route for each net
            for net in self.board.nets:
                # increase allowed deviation
                current_deviation += DEVIATION_INCREASE

                # starting data
                current_loc = net.connect[0].loc
                goal = net.connect[1].loc
                start_distance = self.board.manhattan(current_loc, goal)
                net_length = 0
                
                # coordinates of wire, start at gate
                wire_coordinates = [current_loc]

                n_resets = 0

                # continue until goal or limit is reached
                while current_loc != goal and n_resets < MAX_RESETS:
                    # possible moves
                    moves = MOVES.copy()

                    # continue until valid move found or no moves left
                    while moves:
                        # make move
                        move = random.choice(moves)
                        moves.remove(move)
                        new_loc = self.board.find_new_loc(current_loc, move)

                        # if move invalid try new move
                        if self.valid_move(wire_coordinates, current_loc, new_loc, goal, net_length, start_distance, current_deviation):
                            net_length += 1
                            wire_coordinates.append(new_loc)
                            current_loc = new_loc
                            break

                    n_resets += 1

                # if max resets reached, start over
                if n_resets == MAX_RESETS:
                    if net != 0:
                        self.board.reset_grid()
                    break
                
                # store wire coordinates in net
                net.route = wire_coordinates
                net.length = net_length

                # add net to grid
                for xyz in wire_coordinates:
                    self.board.grid[xyz[0]][xyz[1]][xyz[2]].append(net.net_id)

            # display every 100 tries
            if not n_tries % 100:
                print(f"Tried {n_tries} times")
            n_tries += 1

            # check if solution found
            if n_resets != MAX_RESETS:
                self.board.calc_cost()
                no_solution = False


    def valid_move(self, wire_coordinates, current_loc, new_loc, goal, net_length, dist_init, current_deviation):
        """determines if move is valid"""
        # move is outside of grid
        for i, j in zip(new_loc, (self.board.width, self.board.length, self.board.height)):
            if i > j or i < 0:
                return False

        # requirements
        check_a = not self.board.is_collision(current_loc, new_loc, goal)[0]
        check_b = self.board.manhattan(goal, new_loc) + net_length <= dist_init + current_deviation
        check_c = not new_loc in wire_coordinates

        return check_a & check_b & check_c

