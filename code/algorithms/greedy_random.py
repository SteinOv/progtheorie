import random
from copy import copy

# max deviation from ideal route
DEVIATION = 20
DEVIATION_INCREASE = 5
MAX_RESETS = 5000
INVALID_LIMIT = 50


def greedy_random(board):
    """combines greedy and random"""
    random.seed(500)
    current_deviation = DEVIATION
    #board.width * board.length

    # determine route for each net individually
    for net in board.nets:
        current_deviation += 1
        print(net)

        curr_location = net.connect[0].loc
        goal = net.connect[1].loc
        start_distance = manhattan(curr_location, goal)
        net_length = 0
        
        # coordinates of the wire, start at gate
        wire_coordinates = [curr_location]

        n_resets = 0

        # continue until goal or limit is reached
        while curr_location != goal and n_resets < MAX_RESETS:
            n_resets += 1

            # number of consecutive invalids
            n_invalid = 0

            # continue until valid move or limit is reached
            while n_invalid < INVALID_LIMIT:
                # choose if x, y or z is moved and choose to move -1 or +1
                move = [random.choice((0, 1, 2)), random.choice((-1, 1))]

                # create new location based on move
                new_location = []
                for i, value in enumerate(curr_location):
                    if i == move[0]:
                        new_location.append(value + move[1])
                    else:
                        new_location.append(value)
                new_location = tuple(new_location)


                # check if move is valid
                if valid_move(board, wire_coordinates, curr_location, new_location, goal, net_length, start_distance, current_deviation):
                    net_length += 1
                    wire_coordinates.append(new_location)
                    curr_location = new_location
                    # print(f"valid: {new_location} len: {net_length}")
                    break
                else:
                    n_invalid += 1
                    # print(f"invalid: {new_location} len: {net_length}")

        print(f"Net {net} is af!!!!!")
        print(n_resets)

        # add all wire coordinates to the net's route
        net.route = wire_coordinates

        # add all wire coordinates to board
        for xyz in wire_coordinates:
            board.grid[xyz[0]][xyz[1]][xyz[2]].append(net.net_id)


       


def manhattan(coord_1, coord_2):
    """calculate manhattan distance"""
    dist = 0
    for i in range(3):
        dist += abs(coord_1[i] - coord_2[i])
    return dist

def valid_move(board, wire_coordinates, curr_location, new_location, goal, net_length, dist_init, bound_curr):
    """determine if move is valid"""
    # move is outside of grid
    for i, j in zip(new_location, (board.width, board.length, board.height)):
        if i > j or i < 0:
            # print("req_0")
            return False

    # print(f"distance: {manhattan(goal, coord_2)}, net_len: {net_length}, dist_init: {dist_init}, bound_curr: {bound_curr}")

    req_a = not board.is_collision(curr_location, new_location, goal)
    req_b = manhattan(goal, new_location) + net_length <= dist_init + bound_curr
    req_c = not new_location in wire_coordinates
    # print(req_a, req_b, req_c)

    return req_a & req_b & req_c