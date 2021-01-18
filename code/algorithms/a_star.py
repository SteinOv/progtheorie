from algorithms.greedy_random import greedy_random
from copy import deepcopy


class Node:

    def __init__(self, loc, parent=None):
        self.parent = parent
        self.loc = loc
        self.cost_to_node = 0
        self.heuristic = 0
        self.sum = 0

class a_star(greedy_random):

    def __init__(self, board):
        self.board = deepcopy(board)
    
    def __repr__(self):
        return "a_star"

    def run(self):
        # sort netlist by amount of connections
        self.board.nets.sort(key=lambda net: net.priority_num, reverse=True)

        i = 0
        # run a star search
        while i < len(self.board.nets):
            net = self.board.nets[i]
            # add all wire coordinates to board
            result = self.a_star_search(net)
            if result[0]:
                net.route = result
                net.length = len(result) - 1

                for xyz in result:
                    self.board.grid[xyz[0]][xyz[1]][xyz[2]].append(net.net_id)
                i += 1
            else:
                self.board.reset_grid()
                self.board.nets.remove(net)
                self.board.nets.insert(0, net)
                i = 0
                print("Restarting...")

        self.board.calc_cost()

    def a_star_search(self, net):

        start_loc = net.connect[0].loc
        start_node = Node(start_loc)
        end_loc = net.connect[1].loc
        end_node = Node(end_loc)

        open_list = [start_node]
        closed_list = []
        current_node = start_node

        while open_list:
            # end reached
            if current_node.loc == end_node.loc:

                # backtrack to start
                path = []
                current = current_node

                while current is not start_node:
                    path.append(current.loc)
                    current = current.parent
                path.append(current.loc)
                
                # backtracked, reverse list
                path.reverse()
                return path

            # sort open_list on lowest sum
            open_list.sort(key=lambda node: node.sum)

            # choose node with lowest sum
            current_node = open_list[0]

            # move to closed_list
            open_list.remove(current_node)
            closed_list.append(current_node)

            for move in [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1)]:
                
                new_loc = self.find_new_loc(current_node.loc, move)

                if self.valid_move(current_node.loc, new_loc, end_node.loc):

                    # skip move if in closed_list
                    in_closed_list = [True for node in closed_list if node.loc == new_loc]
                    if in_closed_list:
                        continue
                    
                    # calculate cost_to_node
                    cost_to_node = current_node.cost_to_node + 1

                    # check if new_loc already in open_list
                    in_open_list = [node for node in open_list if new_loc == node.loc]

                    # if not in open list or path to new node is shorter add to open list
                    if in_open_list:
                        # if cost is lower than existing route, update route
                        if cost_to_node < in_open_list[0].cost_to_node:
                            new_node = in_open_list[0]
                            new_node.parent = current_node
                        else:
                            continue
                    else:        
                        new_node = Node(new_loc, current_node)
                        open_list.append(new_node)

                    # calculate heuristic and sum
                    new_node.cost_to_node = cost_to_node
                    new_node.heuristic = self.manhattan(current_node.loc, new_node.loc)
                    new_node.sum = cost_to_node + new_node.heuristic


        print(f"No solution found, {net.net_id}")
        return False, net   
            



    def valid_move(self, current_loc, new_loc, goal):
        """determine if move is valid"""
        # move is outside of grid
        for i, j in zip(new_loc, (self.board.width, self.board.length, self.board.height)):
            if i > j or i < 0:
                return False

        return not self.board.is_collision(current_loc, new_loc, goal)
