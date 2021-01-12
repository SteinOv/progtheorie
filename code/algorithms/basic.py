

def basic(board):
    '''basic algorithm, does not take intersections into account'''

    # for each net
    for net in board.nets:

        # starting x and final x
        x_curr, x_goal = net.connect[0].loc[0], net.connect[1].loc[0]
        y = net.connect[0].loc[1]
        z = 0
        net.route.append((x_curr,y,z))

        # move wire along x axis
        while x_curr != x_goal:
            if x_curr < x_goal:
                x_curr += 1
            else:
                x_curr -= 1

            net.length += 1
            net.route.append((x_curr,y,z))
            board.grid[x_curr][y][z].append(net.net_id)


        y_curr, y_goal = net.connect[0].loc[1], net.connect[1].loc[1]
        x = x_curr
        z = 0

        while y_curr != y_goal:
            if y_curr < y_goal:
                y_curr += 1
            else:
                y_curr -= 1

            net.length += 1
            net.route.append((x,y_curr,z))
            # print(f"x:{x}, y:{y}, z:{z}")
            board.grid[x][y_curr][z].append(net.net_id)