import random
import math

RAAG_BHAIRAV = ['S', 'r', 'G', 'm', 'P', 'd', 'N']

PAKADS = [
    ['S', 'r', 'G', 'm', 'd', 'N', 'S'],
    ['S', 'N', 'd', 'P', 'm', 'G', 'r', 'S'],
    ['G', 'm', 'd', 'N', 'S'], 
    ['r', 'G', 'm', 'P', 'd', 'm', 'G', 'r', 'S'] 
]


def generate_initial_melody(length):
    """Generate a random initial melody of the specified length."""
    return [random.choice(RAAG_BHAIRAV) for _ in range(length)]

def calculate_energy(melody):
    """Calculate the energy of the melody based on specific criteria."""
    energy = 0
    if melody[0] != 'S' or melody[-1] != 'S':
        energy += 10

    for pakad in PAKADS:
        if ''.join(pakad) in ''.join(melody):
            energy -= 5

    for i in range(1, len(melody)):
        if melody[i] == melody[i - 1]:
            energy += 1

    if len(set(melody)) < len(RAAG_BHAIRAV):
        energy += 5

    return energy

def get_neighbor(melody):
    """Generate a neighboring melody by randomly changing one or more notes."""
    new_melody = melody.copy()
    index = random.randint(0, len(melody) - 1)
    new_melody[index] = random.choice(RAAG_BHAIRAV)
    if random.random() < 0.5:
        index2 = random.randint(0, len(melody) - 1)
        new_melody[index2] = random.choice(RAAG_BHAIRAV)
    return new_melody

def simulated_annealing(length, initial_temp, cooling_rate, num_iterations):
    """Perform simulated annealing to find an optimal melody."""
    current_melody = generate_initial_melody(length)
    current_energy = calculate_energy(current_melody)
    best_melody = current_melody
    best_energy = current_energy
    temperature = initial_temp

    for _ in range(num_iterations):
        neighbor = get_neighbor(current_melody)
        neighbor_energy = calculate_energy(neighbor)

        if neighbor_energy < current_energy or random.random() < math.exp((current_energy - neighbor_energy) / temperature):
            current_melody = neighbor
            current_energy = neighbor_energy

        if current_energy < best_energy:
            best_melody = current_melody
            best_energy = current_energy

        temperature *= cooling_rate

    return best_melody


melody_length = 32
initial_temperature = 100.0
cooling_rate = 0.995
iterations = 10000

generated_melody = simulated_annealing(melody_length, initial_temperature, cooling_rate, iterations)
print("Generated Raag Bhairav Melody:", ' '.join(generated_melody))
