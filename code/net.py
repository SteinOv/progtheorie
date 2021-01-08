
class Net:
    ''' Defines a net between gates '''

    def __init__(self, net_id, connect):
        self.net_id = net_id
        self.connect = connect
        self.route = []
        self.length = None 
    
    def __repr__(self):
        return str(self.net_id)
    
    def create_route(self):
        pass

'''

(1,2) -> (4,3)


'''


