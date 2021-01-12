
class Net:
    ''' Defines a net between gates '''

    def __init__(self, board, net_id, connect):
        self.net_id = net_id
        self.connect = connect
        self.route = []
        self.length = 0

        self.create_route(board)
    
    def __repr__(self):
        return str(self.net_id)
    
    def create_route(self, board):
        
        # starting x and final x
        x_curr, x_goal = self.connect[0].loc[0], self.connect[1].loc[0]
        y = self.connect[0].loc[1]
        z = 0
        self.route.append((x_curr,y,z))

        # move wire along x axis
        while x_curr != x_goal:
            if x_curr < x_goal:
                x_curr += 1
            else:
                x_curr -= 1

            self.length += 1
            self.route.append((x_curr,y,z))
            board.add_to_grid(x_curr,y,z)

        
        y_curr, y_goal = self.connect[0].loc[1], self.connect[1].loc[1]
        x = x_curr
        z = 0

        while y_curr != y_goal:
            if y_curr < y_goal:
                y_curr += 1
            else:
                y_curr -= 1

            self.length += 1
            self.route.append((x,y_curr,z))
            board.add_to_grid(x,y_curr,z)
            

        


