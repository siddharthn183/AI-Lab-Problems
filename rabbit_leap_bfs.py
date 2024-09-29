from collections import deque

def is_valid(state):
    return True

def get_successors(state):
    successors = []
    index = state.index("_")
    moves = [-1, -2, 1, 2] 
    
    for move in moves:
        new_index = index + move
        if 0 <= new_index < len(state):
            new_state = list(state)
            new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
            new_state_str = "".join(new_state)
            if is_valid(new_state_str):
                successors.append(new_state_str)
    
    return successors

def bfs(start_state, goal_state):
    queue = deque([(start_state, [])])
    visited = set()
    while queue:
        (state, path) = queue.popleft()
        if state in visited:
            continue
        visited.add(state)
        path = path + [state]
        if state == goal_state:
            return path
        for successor in get_successors(state):
            queue.append((successor, path))
    return None

start_state = "EEE_WWW"
goal_state = "WWW_EEE"

solution = bfs(start_state, goal_state)
if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found.")
