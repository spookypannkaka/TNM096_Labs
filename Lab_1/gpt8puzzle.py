import heapq

class PuzzleNode:
    def __init__(self, state, parent=None, action=None, depth=0):
        self.state = state
        self.parent = parent
        self.action = action  # The move made to get to this state from the parent state
        self.depth = depth
        self.h = self.misplaced_tiles()
        self.f = self.depth + self.h

    def misplaced_tiles(self):
        """Count the number of misplaced tiles, excluding the empty space."""
        misplaced = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0 and self.state[i][j] != goal_state[i][j]:
                    misplaced += 1
        return misplaced

    def __lt__(self, other):
        return self.f < other.f

def get_successors(node):
    """Generate all possible successors of a given node."""
    successors = []
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    zero_pos = [(i, j) for i in range(3) for j in range(3) if node.state[i][j] == 0][0]

    for move in moves:
        new_zero_pos = (zero_pos[0] + move[0], zero_pos[1] + move[1])
        if 0 <= new_zero_pos[0] < 3 and 0 <= new_zero_pos[1] < 3:
            new_state = [list(row) for row in node.state]  # Make a deep copy
            # Swap the zero with the adjacent tile
            new_state[zero_pos[0]][zero_pos[1]], new_state[new_zero_pos[0]][new_zero_pos[1]] = new_state[new_zero_pos[0]][new_zero_pos[1]], new_state[zero_pos[0]][zero_pos[1]]
            successors.append(PuzzleNode(new_state, node, new_zero_pos, node.depth + 1))

    return successors

def a_star_search(start_state, goal_state):
    """Perform A* search."""
    open_list = []
    heapq.heappush(open_list, PuzzleNode(start_state))
    explored = set()

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.state == goal_state:
            return current_node  # Goal reached

        explored.add(tuple(map(tuple, current_node.state)))

        for successor in get_successors(current_node):
            if tuple(map(tuple, successor.state)) not in explored:
                heapq.heappush(open_list, successor)

    return None  # No solution found

# Initial state and goal state
initial_state = [[2, 5, 0], [1, 4, 8], [7, 3, 6]]
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Perform A* search
result = a_star_search(initial_state, goal_state)

# Print the solution path
if result:
    path = []
    while result:
        path.append(result.state)
        result = result.parent
    path.reverse()
    for state in path:
        for row in state:
            print(row)
        print('---')
else:
    print("No solution found.")
