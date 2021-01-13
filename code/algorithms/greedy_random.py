import random
from copy import copy

# starting bound and increase bound every N iterations
BOUNDS = 50
BOUND_INCR = 50

def greedy_random(board):
    '''combines greedy and random'''

    
    # determine route for each net individually
    for net in board.nets:
        print(net)
        
        curr_loc = net.connect[0].loc
        goal = net.connect[1].loc
        dist_init = manhattan(curr_loc, goal)
        net_len = 0

        # count number of iterations
        i = 0
        
        while curr_loc != goal:
            
            bound_curr = BOUNDS
            
            if i > 100:
                raise SystemExit
            
            if i % BOUND_INCR == 0:
                bound_curr += 1

            # continue until valid move is found 
            # TODO change to max iterations
            while True:
                i += 1

                if i > 1000:
                    raise SystemExit
                # choose if x, y or z is moved and choose to move -1 or +1
                move = [random.choice((0, 1, 2)), random.choice((-1, 1))]

                # create new location, moving based on move
                new_loc = tuple(j + move[1] if i == move[0] else j for i, j in enumerate(curr_loc))

                # check if move is valid
                if valid_move(board, net, curr_loc, new_loc, net_len, dist_init, bound_curr) or curr_loc == goal:
                    net_len += 1
                    net.route.append(new_loc)
                    board.grid[new_loc[0]][new_loc[1]][new_loc[2]].append(net.net_id)
                    curr_loc = new_loc
                    print(f"valid: {new_loc} len: {net_len}")
                    break
                else:
                    print(f"invalid: {new_loc} len: {net_len}")


       


def manhattan(coord_1, coord_2):
    '''calculate manhattan distance'''
    dist = 0
    for i in range(3):
        dist += abs(coord_1[i] - coord_2[i])
    return dist

def valid_move(board, net, coord_1, coord_2, net_len, dist_init, bound_curr):
    '''determine if move is valid'''
    # if len(coord_2) != 3:
    #     print(coord_2)

    # move is outside of grid
    for i, j in zip(coord_2, (board.width, board.length, board.height)):
        if i > j or i < 0:
            return False

    req_a = not board.is_collision(coord_1, coord_2)
    req_b = manhattan(coord_1, coord_2) + net_len <= dist_init + bound_curr
    req_c = not coord_2 in net.route

    return req_a & req_b & req_c