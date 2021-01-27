def is_collision(board, curr_loc, new_loc, goal):
    """
    checks if nets are in collision
    returns number of intersections
    returns true if net in collision else false
    """
    # nets on curr_loc and new_loc
    nets_1 = set(board.grid[curr_loc[0]][curr_loc[1]][curr_loc[2]])
    nets_2 = set(board.grid[new_loc[0]][new_loc[1]][new_loc[2]])
    
    # check for colliding nets
    net_collision = nets_1 & nets_2

    # check for intersection
    intersection = 1 if nets_2 and new_loc != goal else 0

    # check if net collides with gate
    gate_collision = new_loc in board.gate_locations and not new_loc == goal

    return net_collision or gate_collision, intersection


def calc_cost(board):
    """calculates and returns total cost of solution"""
    # combined length of all nets
    length = 0
    for net in board.nets:
        length += net.length

    # convert grid to 2D list
    list_2D = sum(sum(board.grid, []), [])

    # list of grid points with intersections
    intersection_nets = [li for li in list_2D if len(li) > 1 and not li.count(-1)]

    # total number of intersections
    total_intersections = 0
    for grid_point in intersection_nets:
        if len(grid_point) == 2:
            total_intersections += 1
        else:
            total_intersections += 2

    print(f"total intersections: {total_intersections}")

    # total cost
    return length + 300 * total_intersections


def manhattan(board, current_loc, new_loc):
    """calculates and returns manhattan distance"""
    distance = 0
    for i in range(3):
        distance += abs(current_loc[i] - new_loc[i])
    return distance


def find_new_loc(board, current_loc, move):
    """returns new location based on move"""
    new_loc = []
    for i, value in enumerate(current_loc):
        if i == move[0]:
            new_loc.append(value + move[1])
        else:
            new_loc.append(value)
    return tuple(new_loc)