from board import Board
from net import Net

class Gate:
    ''' Defines a gate object '''
    
    def __init__(self, gate_id, loc):
        
        assert isinstance(gate_id, int)
        assert isinstance(loc, tuple)
        
        self.gate_id = gate_id
        self.loc = loc



