import heapq

initial_state = [[8, 6, 7], [2, 5, 4], [3, 0, 1]]
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

class Node:
    def __init__(self, state, parent=None, action=None, depth=0):
        self.state = state
        self.parent = parent
        self.action = action  # The move made to get to this state from the parent state
        self.g = depth
        self.h = self.h2()
        self.f = self.g + self.h

    # h1 is a function that returns the current number of misplaced tiles
    def h1(self):
        misplaced_tiles = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != goal_state[i][j] and self.state[i][j] != 0:
                    misplaced_tiles += 1
        return misplaced_tiles
    
    def h2(self):
        manhattan_distance = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0:  # Skip the empty tile
                    # Find the value of the current tile
                    tile_value = self.state[i][j]
                    # Find the expected position of the tile_value in the goal state
                    expected_position = [(row_idx, col_idx) for row_idx, row in enumerate(goal_state) for col_idx, val in enumerate(row) if val == tile_value][0]
                    # Calculate the Manhattan distance and add it to the total
                    manhattan_distance += abs(i - expected_position[0]) + abs(j - expected_position[1])
        return manhattan_distance
    
    # Heapq needs to compare elements to keep them in the correct order
    def __lt__(self, other):
        return self.f < other.f

# From an input state, get all possible moves from that state
# 0 is the empty space
# Expand the current state: Move the empty space in all possible directions and calculate f for each state
def get_children(node):
    children = []
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    # Find the position of the empty space (the number 0)
    zero_pos = [(i, j) for i in range(3) for j in range(3) if node.state[i][j] == 0][0]

    for move in moves:
        # [x,y], so 0 is x and 1 is y
        new_zero_pos = (zero_pos[0] + move[0], zero_pos[1] + move[1])

        # The new zero position must be inside the 3x3 grid
        if 0 <= new_zero_pos[0] < 3 and 0 <= new_zero_pos[1] < 3:
            # Save the current state
            new_state = [list(row) for row in node.state]

            new_state[zero_pos[0]][zero_pos[1]], new_state[new_zero_pos[0]][new_zero_pos[1]] = new_state[new_zero_pos[0]][new_zero_pos[1]], new_state[zero_pos[0]][zero_pos[1]]

            # Save the new state to the list of children, which also calculates its g and h value when the node is created
            children.append(Node(new_state, node, new_zero_pos, node.g + 1))

    return children

# Printe the path from a current node from the initial state
def print_path(node):
    path = []
    while node is not None:
        path.append(node.state)
        node = node.parent
    path.reverse()
    for state in path:
        for row in state:
            print(row)
        print("----------")

def astar_search(initial_state, goal_state):
    open_list = []  # Priority queue of nodes to be evaluated
    closed_list = set()  # Set of nodes already evaluated

    # Put the initial state into the open list
    heapq.heappush(open_list, Node(state=initial_state))

    # Check states in open list
    while open_list:
        current_node = heapq.heappop(open_list)

        # Check if the current state matches the goal state - in that case, the goal is reached
        if current_node.state == goal_state:
            print("You reached the goal!")
            print_path(current_node)
            print("Number of moves: ")
            print(current_node.g)
            return current_node
        
        # If current state is not the goal, add it to the closed list (to avoid repeats)
        closed_list.add(tuple(map(tuple, current_node.state)))

        # Check child states of this node. If is the state is unexplored, add to open list
        for children in get_children(current_node):
            if tuple(map(tuple, children.state)) not in closed_list:
                heapq.heappush(open_list, children)

    # The search has failed
    print("Too bad")
    return None

astar_search(initial_state, goal_state)