from copy import deepcopy
from code.helpers import helpers
from queue import PriorityQueue

INTERSECTION_COST = 300
DIRECTIONS = [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1)]


class Node:
    """grid point"""

    def __init__(self, loc, parent=None):
        self.parent = parent
        self.loc = loc
        self.cost_to_node = 0
        self.heuristic = 0
        self.sum = 0
    

    def __repr__(self):
        return str(f"{id(self)}, loc: {self.loc}, sum: {self.sum}")


    def __lt__(self, other):
        """highest priority for node with lowest sum and latest in open_list"""
        selfPriority = self.sum
        otherPriority = other.sum
        return selfPriority <= otherPriority


class a_star:
    """A* algorithm using manhattan distance heuristic"""

    def __init__(self, board):
        self.board = deepcopy(board)
    

    def __repr__(self):
        return "a_star"


    def run(self):
        """starts algorithm"""
        # sort nets by priority
        self.board.nets.sort(key=lambda net: net.priority_num, reverse=True)

        i = 0
        
        # for every net
        while i < len(self.board.nets):
            net = self.board.nets[i]

            # add wire coordinates to grid
            solution = self.a_star_search(net)
            if solution:
                net.route = solution
                self.board.add_net(net)
                
                i += 1

            # if no solution restart with unsolved net first
            else:
                self.board.reset_grid()
                self.board.nets.remove(net)
                self.board.nets.insert(0, net)
                i = 0
                print("Restarting...")

        # total cost
        self.board.cost = helpers.calc_cost(self.board)


    def a_star_search(self, net):
        """
        tries to find ideal solution for net
        returns list of coordinates if solution found else false
        """
        # start and end nodes
        start_loc, end_loc = net.connect[0].loc, net.connect[1].loc
        start_node, end_node = Node(start_loc), Node(end_loc)

        # nodes open to visit
        open_list = PriorityQueue()
        open_list.put(start_node)

        # already visited nodes
        closed_list = set()
        
        current_node = start_node
        while not open_list.empty():
            # check if goal reached
            if current_node.loc == end_node.loc:
                path = []
                current = current_node

                # backtrack to start
                while current is not start_node:
                    path.append(current.loc)
                    current = current.parent
                path.append(current.loc)
                
                # return reversed list
                path.reverse()
                return path

            # choose node with lowest sum and add to closed list
            current_node = open_list.get()
            closed_list.add(current_node.loc)

            # add valid moves to open_list
            for move in DIRECTIONS:
                self.move(move, current_node, end_node, open_list, closed_list)

        print(f"no solution found for net: {net.net_id}")
        return False
            

    def valid_move(self, current_loc, new_loc, goal):
        """determines if move is valid"""
        # return false if move outside of grid
        grid_dimensions = (self.board.width, self.board.length, self.board.height)
        for i, j in zip(new_loc, grid_dimensions):
            if i > j or i < 0:
                return False, 0

        # return: true if not in collision and 1 if intersection
        collision_intersection = helpers.is_collision(self.board, current_loc, new_loc, goal)
        return not collision_intersection[0], collision_intersection[1]


    def move(self, move, current_node, end_node, open_list, closed_list):
        """if move valid, add to open_list or update existing node"""
        # try move, skip if invalid
        new_loc = helpers.find_new_loc(self.board, current_node.loc, move)
        move_valid, n_intersections = self.valid_move(current_node.loc,
                                                    new_loc, end_node.loc)
        if move_valid:
            # skip move if in closed_list
            if new_loc in closed_list:
                return

            # calculate cost_to_node
            cost_to_node = current_node.cost_to_node + 1 + \
                        INTERSECTION_COST * n_intersections

            # check if node already in open_list
            in_open_list = [node for node in open_list.queue if new_loc == node.loc]
            if in_open_list:
                return
                
            new_node = Node(new_loc, current_node)

            # calculate heuristic and sum
            new_node.cost_to_node = cost_to_node
            node_heuristic = new_node.heuristic = helpers.manhattan(self.board, current_node.loc, new_node.loc)
            new_node.sum = cost_to_node + node_heuristic

            # add new node to open_list
            open_list.put(new_node)
