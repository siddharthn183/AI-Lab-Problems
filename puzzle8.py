import heapq
import numpy as np
import random


class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g  
        self.h = h 
        self.f = g + h 

    def __lt__(self, other):
        return self.f < other.f 


def heuristic(state, goal_state):
    """Calculate the Manhattan distance heuristic."""
    h = 0
    for i in range(9):
        if state[i] != 0: 
            goal_index = goal_state.index(state[i])
            h += abs(i // 3 - goal_index // 3) + abs(i % 3 - goal_index % 3)
    return h


def get_successors(node):
    """Generate successor nodes by moving the empty space (0)."""
    successors = []
    index = node.state.index(0) 
    row, col = index // 3, index % 3

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:  
            new_index = new_row * 3 + new_col
            new_state = list(node.state)
            new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
            h = heuristic(new_state, goal_state)  
            successor = Node(new_state, node, node.g + 1, h)  
            successors.append(successor)
    
    return successors


def search_agent(start_state, goal_state):
    """A* search algorithm for the 8-puzzle problem."""
    start_node = Node(start_state, g=0, h=heuristic(start_state, goal_state))
    frontier = []
    heapq.heappush(frontier, start_node)
    visited = set()
    nodes_explored = 0

    while frontier:
        node = heapq.heappop(frontier) 
        if tuple(node.state) in visited: 
            continue
        visited.add(tuple(node.state))
        nodes_explored += 1

        if node.state == goal_state: 
            path = []
            while node:
                path.append(node.state)
                node = node.parent
            print('Total nodes explored:', nodes_explored)
            return path[::-1]

        for successor in get_successors(node):
            heapq.heappush(frontier, successor)

    print('Total nodes explored:', nodes_explored)
    return None

start_state = [1, 2, 3, 4, 5, 0, 7, 8, 6]
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]


solution = search_agent(start_state, goal_state)
if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found.")
