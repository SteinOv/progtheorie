class Gate:
    
    def __init__(self, gate_id, loc):
        self.gate_id = gate_id
        self.loc = loc
        self.n_connections = 0

    def __repr__(self):
        return str(self.gate_id)


