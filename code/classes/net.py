
class Net:
    ''' Defines a net between gates '''

    def __init__(self, board, net_id, connect):
        self.net_id = net_id
        self.connect = connect
        self.route = []
        self.length = 0

    
    def __repr__(self):
        return str(self.net_id)

        


