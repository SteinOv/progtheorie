import random
from copy import copy, deepcopy

# max deviation from ideal route
DEVIATION = 25
DEVIATION_INCREASE = 10
MAX_RESETS = 500

class greedy_random:
    """
    combination of random and greedy algorithm using manhattan distance    
    """

    def __init__(self, board):
        self.board = deepcopy(board)

    def __repr__(self):
        return "greedy_random"

    def run(self):
        """combines greedy and random"""
        # allowed deviation for algorithm
        current_deviation = DEVIATION

        no_solution = True
        n_tries = 0

        # continue until solution is found
        while no_solution:
            # determine route for each net individually
            for net in self.board.nets:
                # increase the allowed deviation
                current_deviation += DEVIATION_INCREASE

                # starting data
                current_loc = net.connect[0].loc
                goal = net.connect[1].loc
                start_distance = self.board.manhattan(current_loc, goal)
                net_length = 0
                
                # coordinates of the wire, start at gate
                wire_coordinates = [current_loc]

                n_resets = 0

                # continue until goal or limit is reached
                while current_loc != goal and n_resets < MAX_RESETS:
                    # possible moves
                    moves = [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1)]

                    # continue until no possible moves left
                    while moves:
                        # choose a move
                        move = random.choice(moves)
                        moves.remove(move)
                        
                        # create new location
                        new_loc = self.board.find_new_loc(current_loc, move)

                        # check if move is valid, continue
                        if self.valid_move(wire_coordinates, current_loc, new_loc, goal, net_length, start_distance, current_deviation):
                            net_length += 1
                            wire_coordinates.append(new_loc)
                            current_loc = new_loc
                            break

                    n_resets += 1

                # if max resets reached start over
                if n_resets == MAX_RESETS:
                    if net != 0:
                        self.board.reset_grid()
                    break
                
                # add all wire coordinates to net's route
                net.route = wire_coordinates
                net.length = net_length

                # add all wire coordinates to board
                for xyz in wire_coordinates:
                    self.board.grid[xyz[0]][xyz[1]][xyz[2]].append(net.net_id)

            # display every 100 iterations
            if not n_tries % 100:
                print(f"Tried {n_tries} times")
            n_tries += 1

            # solution found, so quit loop
            if n_resets != MAX_RESETS:
                self.board.calc_cost()
                no_solution = False


    def valid_move(self, wire_coordinates, current_loc, new_loc, goal, net_length, dist_init, current_deviation):
        """determine if move is valid"""
        # move is outside of grid
        for i, j in zip(new_loc, (self.board.width, self.board.length, self.board.height)):
            if i > j or i < 0:
                return False

        check_a = not self.board.is_collision(current_loc, new_loc, goal)[0]
        check_b = self.board.manhattan(goal, new_loc) + net_length <= dist_init + current_deviation
        check_c = not new_loc in wire_coordinates

        return check_a & check_b & check_c

