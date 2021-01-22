from copy import deepcopy

class hill_climber:

    def __init__(self, board, filename="./data/output/output.csv"):
        self.board = deepcopy(board)
        self.board.read_output(filename)
        self.board.cost = self.board.calc_cost()

    def __repr__(self):
        return "hill_climber"
    
    def run(self):
        pass
        
        