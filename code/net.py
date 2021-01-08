
class Net:
    ''' Defines a net between gates '''

    def __init__(self, net_id, connect):
        self.net_id = net_id
        self.connect = connect
        self.route = []
        self.length = 0

        self.create_route()
    
    def __repr__(self):
        return str(self.net_id)
    
    def create_route(self):
        
        # starting x and final x
        x_curr, x_goal = self.connect[0].loc[0], self.connect[1].loc[0]
        y = self.connect[0].loc[1]
        self.route.append((x_curr, y))

        # move wire along x axis
        while x_curr != x_goal:
            if x_curr < x_goal:
                x_curr += 1
            else:
                x_curr -= 1

            self.length += 1
            self.route.append((x_curr,y))

        
        y_curr, y_goal = self.connect[0].loc[1], self.connect[1].loc[1]
        x = x_curr

        while y_curr != y_goal:
            if y_curr < y_goal:
                y_curr += 1
            else:
                y_curr -= 1

            self.length += 1
            self.route.append((x,y_curr))

        


