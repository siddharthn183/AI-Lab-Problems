import math
import random
import matplotlib.pyplot as plt

cities = [
    "Jaipur", "Udaipur", "Jodhpur", "Jaisalmer", "Pushkar", "Ranthambore", "Ajmer",
    "Mount Abu", "Bikaner", "Chittorgarh", "Bundi", "Sawai Madhopur", "Kumbhalgarh",
    "Ranakpur", "Bharatpur", "Shekhawati", "Sariska", "Alwar", "Mandawa", "Nathdwara"
]


random.seed(42) 
city_coords = {city: (random.uniform(0, 100), random.uniform(0, 100)) for city in cities}

def distance(city1, city2):
    """Calculate Euclidean distance between two cities."""
    x1, y1 = city_coords[city1]
    x2, y2 = city_coords[city2]
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def total_distance(tour):
    """Calculate the total distance of a tour."""
    return sum(distance(tour[i], tour[i+1]) for i in range(len(tour)-1)) + distance(tour[-1], tour[0])

def swap_cities(tour):
    """Create a new tour by swapping two cities."""
    new_tour = tour.copy()
    i, j = random.sample(range(len(tour)), 2)
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    return new_tour

def simulated_annealing(initial_tour, initial_temp, cooling_rate, num_iterations):
    current_tour = initial_tour
    current_distance = total_distance(current_tour)
    best_tour = current_tour
    best_distance = current_distance
    temperature = initial_temp
    
    distance_history = [current_distance]

    for _ in range(num_iterations):
        new_tour = swap_cities(current_tour)
        new_distance = total_distance(new_tour)
        
        if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / temperature):
            current_tour = new_tour
            current_distance = new_distance
            
            if current_distance < best_distance:
                best_tour = current_tour
                best_distance = current_distance
        
        temperature *= cooling_rate
        distance_history.append(current_distance)

    return best_tour, best_distance, distance_history

def plot_tour(tour, title):
    """Plot the tour on a 2D plane."""
    x = [city_coords[city][0] for city in tour]
    y = [city_coords[city][1] for city in tour]
    x.append(x[0])
    y.append(y[0])
    
    plt.figure(figsize=(10, 10))
    plt.plot(x, y, 'bo-')
    plt.title(title)
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    for i, city in enumerate(tour):
        plt.annotate(city, (x[i], y[i]))
    plt.grid(True)
    plt.show()

initial_tour = random.sample(cities, len(cities))
initial_temp = 1000
cooling_rate = 0.995
num_iterations = 10000

best_tour, best_distance, distance_history = simulated_annealing(initial_tour, initial_temp, cooling_rate, num_iterations)

plot_tour(initial_tour, "Initial Tour")

plot_tour(best_tour, f"Best Tour (Distance: {best_distance:.2f})")

plt.figure(figsize=(10, 5))
plt.plot(distance_history)
plt.title('Tour Distance vs. Iteration')
plt.xlabel('Iteration')
plt.ylabel('Tour Distance')
plt.grid(True)
plt.show()

print("Best tour found:")
for city in best_tour:
    print(city)
print(f"\nTotal distance: {best_distance:.2f}")