
class Net:
    ''' Defines a net between gates '''

    def __init__(self, net_id, connect):

        assert isinstance(net_id, int)
        assert isinstance(connect, tuple)

        self.net_id = net_id
        self.connect = connect
        self.route = []
        self.length = None 

        

