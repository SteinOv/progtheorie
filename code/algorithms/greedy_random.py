import random
from copy import copy

# max deviation from ideal route
BOUNDS = 50
BOUND_INCR = 50

def greedy_random(board):
    '''combines greedy and random'''
    # random.seed(500)
    
    # determine route for each net individually
    for net in board.nets:
        print(net)

        curr_location = net.connect[0].loc
        goal = net.connect[1].loc
        start_distance = manhattan(curr_location, goal)
        net_length = 0

        # count number of iterations
        k = 0
        
        while curr_location != goal:
            
            bound_curr = BOUNDS
            
            # if k > 100:
            #     raise SystemExit
            
            if k % BOUND_INCR == 0:
                bound_curr += 1

            # continue until valid move is found 
            # TODO change to max iterations
            while True:
                k += 1
                # if k > 1000:
                #     raise SystemExit

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
                if valid_move(board, net, curr_location, new_location, goal, net_length, start_distance, bound_curr) or curr_location == goal:
                    net_length += 1
                    net.route.append(new_location)
                    board.grid[new_location[0]][new_location[1]][new_location[2]].append(net.net_id)
                    curr_location = new_location
                    # print(f"valid: {new_location} len: {net_length}")
                    break
                # else:
                #     print(f"invalid: {new_location} len: {net_length}")

        print(f"Net {net} is af!!!!!")


       


def manhattan(coord_1, coord_2):
    '''calculate manhattan distance'''
    dist = 0
    for i in range(3):
        dist += abs(coord_1[i] - coord_2[i])
    return dist

def valid_move(board, net, coord_1, coord_2, goal, net_length, dist_init, bound_curr):
    '''determine if move is valid'''
    # if len(coord_2) != 3:
    #     print(coord_2)

    # move is outside of grid
    for i, j in zip(coord_2, (board.width, board.length, board.height)):
        if i > j or i < 0:
            # print("req_0")
            return False

    # print(f"distance: {manhattan(goal, coord_2)}, net_len: {net_length}, dist_init: {dist_init}, bound_curr: {bound_curr}")

    req_a = not board.is_collision(coord_1, coord_2)
    req_b = manhattan(goal, coord_2) + net_length <= dist_init + bound_curr
    req_c = not coord_2 in net.route
    # print(req_a, req_b, req_c)

    return req_a & req_b & req_c