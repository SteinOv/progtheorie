class Node:

    def __init__(self, parent=None, loc):
        self.parent = parent
        self.location = loc
        self.cost_to_node = 0
        self.heuristic = 0
        self.sum = 0



class a_star(greedy_random):

    def __init__(self, board):
        self.board = deepcopy(board)
        


    def run(self):

        for net in self.board.nets:
            pass
            # run a star search

    


    def a_star_search(self, net):

        start_loc = net.connect[0]
        start_node = Node(None, start_loc)
        end_loc = net.connect[1]
        end_node = Node(None, end_loc)

        open_list = [start_node]
        closed_list = []
        current_node = start_node
        while open_list:

            # end reached
            if current_node is end_node:
                # backtrack to start



            # move to closed_list
            open_list.remove(current_node)
            closed_list.append(current_node)

            for move in [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1)]:
                if self.valid_move(current_loc, new_loc, goal):
                    new_node = Node(current_node, self.find_new_loc(current_loc, move))

                # node already in closed_list, skip
                for node in closed_list:
                    if node.loc == new_node.loc:
                        in_closed = True


                    # TODO calculate cost_to_node, heuristic and sum

                    # add node to open list
                    open_list.append(node)
                else:
                    continue
            
            # sort open_list on lowest sum
            open_list.sort(key=lambda node: node.sum)

            # choose node with lowest sum
            current_node = open_list[0]






    def valid_move(self, current_loc, new_loc, goal):
        """determine if move is valid"""
        # move is outside of grid
        for i, j in zip(new_loc, (self.board.width, self.board.length, self.board.height)):
            if i > j or i < 0:
                return False

        return not self.board.is_collision(current_loc, new_loc, goal)
