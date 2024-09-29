import random
import math

def evaluate_cost(layout):
    overall_cost = 0
    for row in range(512):
        for col in range(512):
            if col + 1 < 512 and (col + 1) % 128 == 0:
                overall_cost += abs(int(layout[(512 * row) + col]) - int(layout[(512 * row) + col + 1]))
            if row + 1 < 512 and (row + 1) % 128 == 0:
                overall_cost += abs(int(layout[(512 * row) + col]) - int(layout[(512 * (row + 1)) + col]))
    return overall_cost

def swap_puzzle_blocks(layout):
    idx1, idx2 = random.sample(range(16), 2)
    row1 = idx1 // 4
    row2 = idx2 // 4
    col1 = idx1 % 4
    col2 = idx2 % 4
    row_shift1 = 128 * row1
    row_shift2 = 128 * row2
    col_shift1 = 128 * col1
    col_shift2 = 128 * col2
    
    section_1 = [layout[(512 * (row_shift1 + i)) + (col_shift1 + j)] for i in range(128) for j in range(128)]
    section_2 = [layout[(512 * (row_shift2 + i)) + (col_shift2 + j)] for i in range(128) for j in range(128)]

    for i in range(128):
        for j in range(128):
            layout[(512 * (row_shift1 + i)) + (col_shift1 + j)] = section_2[(i * 128) + j]
            layout[(512 * (row_shift2 + i)) + (col_shift2 + j)] = section_1[(i * 128) + j]

    return layout

def apply_simulated_annealing(initial_layout, starting_temp, cooling_factor, target_temp):
    min_cost = float('inf')
    optimal_layout = None
    current_temp = starting_temp
    current_layout = initial_layout
    current_cost = evaluate_cost(current_layout)
    
    while current_temp > target_temp:
        candidate_layout = swap_puzzle_blocks(current_layout.copy())
        candidate_cost = evaluate_cost(candidate_layout)

        if candidate_cost < current_cost:
            current_layout = candidate_layout
            current_cost = candidate_cost
            if current_cost < min_cost:
                min_cost = current_cost
                optimal_layout = current_layout.copy()
        else:
            if random.uniform(0, 1) < math.exp((current_cost - candidate_cost) / current_temp):
                current_layout = candidate_layout
                current_cost = candidate_cost
        
        current_temp *= cooling_factor 
    
    return optimal_layout, min_cost

puzzle_info = []
with open('scrambled_lena.mat', 'r') as file:
    for _ in range(5): 
        next(file)
    
    for line in file:
        puzzle_info.append(line.strip().split()) 


flat_layout = [int(item) for sublist in puzzle_info for item in sublist]

best_solution = []
lowest_cost = float('inf')

for attempt in range(5):
    temp_start = 1000
    temp_decay = 0.99
    final_temp = 0.1
    solved_layout, cost = apply_simulated_annealing(flat_layout, temp_start, temp_decay, final_temp)
    
    if cost < lowest_cost:
        lowest_cost = cost
        flat_layout = solved_layout.copy()
        best_solution = flat_layout
    
    print(cost)

with open('solution.mat', 'w') as output_file:
    for value in best_solution:
        output_file.write(f"{value}\n")
