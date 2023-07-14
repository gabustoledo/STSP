import random
import math

class Individual:
    def __init__(self, cities):
        self.cities = cities
        self.fitness = self.calculate_fitness()
        self.distance = self.calculate_distance()
    
    def calculate_distance(self):
        total_distance = 0
        for i in range(len(self.cities)):
            city = self.cities[i]
            next_city = self.cities[(i + 1) % len(self.cities)]  # Circular tour
            total_distance += distance(city, next_city)  # Replace with your distance calculation function
        return total_distance  # Fitness is inversely proportional to the total distance

    def calculate_fitness(self):
        total_distance = 0
        for i in range(len(self.cities)):
            city = self.cities[i]
            next_city = self.cities[(i + 1) % len(self.cities)]  # Circular tour
            total_distance += distance(city, next_city)  # Replace with your distance calculation function
        return 1 / total_distance  # Fitness is inversely proportional to the total distance

def distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def initialize_population(population_size, city_list):
    population = []
    for _ in range(population_size):
        cities = city_list.copy()
        random.shuffle(cities)  # Randomly shuffle the city list for each individual
        individual = Individual(cities)
        population.append(individual)
    return population

def tournament_selection(population, tournament_size):
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda x: x.fitness, reverse=True)  # Higher fitness is better
    return tournament[0]

def crossover(parent1, parent2):
    child = [None] * len(parent1.cities)
    start_index = random.randint(0, len(parent1.cities) - 1)
    end_index = random.randint(start_index, len(parent1.cities) - 1)

    for i in range(start_index, end_index + 1):
        child[i] = parent1.cities[i]
    
    remaining_cities = [x for x in parent2.cities if x not in child]
    child_index = 0
    for i in range(len(child)):
        if child[i] is None:
            child[i] = remaining_cities[child_index]
            child_index += 1
    
    return Individual(child)

def mutate(individual, mutation_rate):
    if random.random() < mutation_rate:
        index1 = random.randint(0, len(individual.cities) - 1)
        index2 = random.randint(0, len(individual.cities) - 1)
        individual.cities[index1], individual.cities[index2] = individual.cities[index2], individual.cities[index1]
        individual.fitness = individual.calculate_fitness()

def genetic_algorithm(city_list, population_size, tournament_size, mutation_rate, generations):
    population = initialize_population(population_size, city_list)
    
    for _ in range(generations):
        new_population = []
        
        for _ in range(population_size):
            parent1 = tournament_selection(population, tournament_size)
            parent2 = tournament_selection(population, tournament_size)
            child = crossover(parent1, parent2)
            mutate(child, mutation_rate)
            new_population.append(child)
        
        population = new_population
    
    population.sort(key=lambda x: x.fitness, reverse=True)  # Sort population by fitness
    best_individual = population[0]
    
    return best_individual

def read_cities_file(filename):
    cities = []
    with open(filename, 'r') as file:
        for line in file:
            city_info = line.strip().split()
            city_id = int(city_info[0])
            x = float(city_info[1])
            y = float(city_info[2])
            city = (x, y)
            cities.append(city)
    return cities

# Example usage
filename = '../djibouti.txt'  # Nombre del archivo de texto
cities = read_cities_file(filename)

population_size = 100
tournament_size = 10
mutation_rate = 0.3
generations = 300

best_solution = genetic_algorithm(cities, population_size, tournament_size, mutation_rate, generations)
# print("Best solution:", best_solution.cities)
print("Fitness:", best_solution.fitness)
print("Distance:", best_solution.distance)