initial_state = [[2, 5, 0], [1, 4, 8], [7, 3, 6]]
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# h1 is a function that returns the current number of misplaced tiles
def h1(current_state, goal_state):
    misplaced_tiles = 0

    for i in range(len(current_state)):
        for j in range(len(current_state[i])):
            if current_state[i][j] != goal_state[i][j] and current_state[i][j] != 0:
                misplaced_tiles += 1
    return misplaced_tiles