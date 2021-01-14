import random
from copy import copy, deepcopy

# max deviation from ideal route
DEVIATION = 50
DEVIATION_INCREASE = 10
MAX_RESETS = 500

class greedy_random:
    '''
    combination of random and greedy algorithm using manhattan distance
    
    '''

    def __init__(self, board):
        self.board = deepcopy(board)

    def __repr__(self):
        return "greedy_random"

    def run(self):
        """combines greedy and random"""
        random.seed(500) # TODO remove seed
        current_deviation = DEVIATION

        # True as long as no solution is found
        no_solution = True
        count = 0
        while no_solution:
            
            # determine route for each net individually
            for net in self.board.nets:
                current_deviation += DEVIATION_INCREASE

                curr_location = net.connect[0].loc
                goal = net.connect[1].loc
                start_distance = self.manhattan(curr_location, goal)
                net_length = 0
                
                # coordinates of the wire, start at gate
                wire_coordinates = [curr_location]

                n_resets = 0

                # continue until goal or limit is reached
                while curr_location != goal and n_resets < MAX_RESETS:
                    n_resets += 1

                    # possible moves
                    moves = [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1)]

                    # continue until no possible moves left
                    while moves:
                        # choose a move
                        move = random.choice(moves)
                        moves.remove(move)
                        
                        # create new location based on move
                        new_location = []
                        for i, value in enumerate(curr_location):
                            if i == move[0]:
                                new_location.append(value + move[1])
                            else:
                                new_location.append(value)
                        new_location = tuple(new_location)


                        # check if move is valid, continue to next wire if so
                        if self.valid_move(wire_coordinates, curr_location, new_location, goal, net_length, start_distance, current_deviation):
                            net_length += 1
                            wire_coordinates.append(new_location)
                            curr_location = new_location
                            break

                # if max resets is reached start over
                if n_resets == MAX_RESETS:
                    if net != 0:
                        self.board.reset_grid()
                    break
                
                # add all wire coordinates to the net's route
                net.route = wire_coordinates
                net.length = net_length

                # add all wire coordinates to board
                for xyz in wire_coordinates:
                    self.board.grid[xyz[0]][xyz[1]][xyz[2]].append(net.net_id)

            if count == 100:
                count = 0
                print("100 additional tries")
            count += 1

            # solution found, so quit loop
            if n_resets != MAX_RESETS:
                self.board.calc_cost()
                no_solution = False


    def manhattan(self, curr_location, new_location):
        """calculate manhattan distance"""
        dist = 0
        for i in range(3):
            dist += abs(curr_location[i] - new_location[i])
        return dist

    def valid_move(self, wire_coordinates, curr_location, new_location, goal, net_length, dist_init, bound_curr):
        """determine if move is valid"""
        # move is outside of grid
        for i, j in zip(new_location, (self.board.width, self.board.length, self.board.height)):
            if i > j or i < 0:
                return False

        check_a = not self.board.is_collision(curr_location, new_location, goal)
        check_b = self.manhattan(goal, new_location) + net_length <= dist_init + bound_curr
        check_c = not new_location in wire_coordinates

        return check_a & check_b & check_c