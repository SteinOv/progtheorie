
class Gate:
    ''' Defines a gate object '''
    
    def __init__(self, gate_id, loc):
        self.gate_id = gate_id
        self.loc = loc


    def __repr__(self):
        return str(self.gate_id)

