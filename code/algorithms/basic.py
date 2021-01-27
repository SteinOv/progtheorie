from copy import deepcopy


class basic:
    """finds shortest possible routes without constraints"""
    def __init__(self, board):
        self.board = deepcopy(board)
        

    def __repr__(self):
        return "basic"


    def run(self):
        """start algorithm"""
        for net in self.board.nets:
            # horizontal starting data
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

                # add x coordinates
                net.route.append((x_curr,y,z))
                self.board.grid[x_curr][y][z].append(net.net_id)

            # vertical starting data
            y_curr, y_goal = net.connect[0].loc[1], net.connect[1].loc[1]
            x = x_curr
            z = 0

            # move wire along y axis
            while y_curr != y_goal:
                if y_curr < y_goal:
                    y_curr += 1
                else:
                    y_curr -= 1

                net.length += 1

                # add x coordinates
                net.route.append((x,y_curr,z))
                self.board.grid[x][y_curr][z].append(net.net_id)
            
            self.board.cost += net.length