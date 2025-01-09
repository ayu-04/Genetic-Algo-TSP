import random

dist_dict = {}
fitness_dict = {}
##HYPERPARAMS
POP_SIZE = 1000
NUM_NEAREST = 10
GENERATIONS = 50
POOL_SIZE = 100
ELITE_SIZE = 100
MUTATION_RATE = 0.1
TOURNAMENT_SIZE = 10
NUM_CHILDREN = 1000

def dist(city1, city2):
    key = tuple(sorted((city1, city2)))
    if key in dist_dict:
        return dist_dict[key]
    d = ((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2 + (city1[2] - city2[2])**2)**0.5 
    dist_dict[key] = d
    return d

def fitness_fun(path):
    """returns the total dist of a path"""
    key = tuple(path)
    if key in fitness_dict:
        return fitness_dict[key]
    tot = 0
    n = len(path)
    for i in range(n):
        tot += dist(cities[path[i]], cities[path[(i+1)%n]])
    fitness_dict[key] = tot
    return tot

def brute_force(cities):
    """
    Solves TSP using brute force recursion to find the optimal path for n <= 10.
    """
    n = len(cities)
    min_cost = float('inf')
    best_path = []

    def visit_city(curr_city, visited, total_cost, path):
        nonlocal min_cost, best_path

        if len(visited) == n:  # If all cities are visited, return to the start
            total_cost += dist(cities[curr_city], cities[0])  
            if total_cost < min_cost:
                min_cost = total_cost
                best_path = path + [0]  
            return

        for next_city in range(n):
            if next_city not in visited:  
                visit_city(next_city, visited + [next_city], total_cost + dist(cities[curr_city], cities[next_city]), path + [next_city])

    visit_city(0, [0], 0, [0])  
    return min_cost, best_path[:-1]

def CreateInitialPopulation(size, cities, num_nearest):
    """Size: An integer representing the size of the list (initial_population) that
    needs to be returned.
    Cities: A list of cities/locations where a location is represented in 3D
    coordinates (x,y,z)
    Return Value: returns a list of paths where each path is generated using 
    nearest neighbors."""

    n = len(cities)
    population = []
    # Precompute nearest neighbors for each city
    nearest_neighbors = {}
    for i in range(n):
        distances = [(j, dist(cities[i], cities[j])) for j in range(n) if i != j]
        distances.sort(key=lambda x: x[1])  # Sort by distance
        nearest_neighbors[i] = [city for city, _ in distances[:num_nearest]]
    # Generate each individual
    for _ in range(size):
        path = []
        available_cities = set(range(n))
        current_city = random.choice(list(available_cities))
        path.append(current_city)
        available_cities.remove(current_city)
        # Build path by selecting from nearest neighbors
        while available_cities:
            next_city = None
            for neighbor in nearest_neighbors[current_city]:
                if neighbor in available_cities:
                    next_city = neighbor
                    break
            if next_city is None:  # If no nearest neighbor is available, choose randomly
                next_city = random.choice(list(available_cities))
            path.append(next_city)
            available_cities.remove(next_city)
            current_city = next_city
        population.append(path) 
    return population

def CreateElitePool(population, fitness_scores, size=5):
    """Population: A list of paths from which the elite pool is to be created
    fitness_scores: A list of fitness scores for the population.
    Return Value: A list of elite individuals who are preserved and 
    directly carried over to the next generation."""
    idx = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse = True)[:size] # identifies the indices of the elite individuals
    elitePool = [population[i] for i in idx]
    return elitePool

def CreateMatingPool(population, fitness_scores, pool_size, tournament_size = 5):
    """Population: A list of paths from which the mating pool is to be created
    fitness_scores: A list of fitness scores for the population.
    Return Value: A list of populations selected for mating (List contains
    paths)
    Function Definition: In each round, a subset (the "tournament") of the population is randomly selected. 
    The individual with the highest fitness in that subset is selected.
    Scales better w/ population size, balanced exploration & exploitation"""
    matingPool = []
    if len(population)>tournament_size:
        for _ in range(pool_size):
            tournament = random.sample(list(zip(population, fitness_scores)), tournament_size) # randomly select individuals from population
            matingPool.append(max(tournament, key = lambda i: i[1])[0]) # choose the one w/ the highest fitness score to be a parent
    return matingPool

def resolve_conflicts(child, parent2):
    """Performs conflict resolution to make sure child is a valid path."""
    missing = [city for city in parent2 if city not in child]
    new_child = []
    for city in child:
        if city is None:
            new_child.append(missing.pop(0))
        else:
            new_child.append(city)    
    return new_child

def Crossover(parent1, parent2, start_index, end_index):
    """Parent1: First argument of the function: A list containing the random
    sequence of cities for the salesman to follow
    Parent2: Second argument of the function: A list containing the random
    sequence of cities for the salesman to follow
    Start_index: Start index of the SUBARRAY to be chosen from parent 1
    End_index: End index of the SUBARRAY to be chosen from parent 1
    Return Value: Return child after performing the crossover (also a list
    containing a valid sequence of cities)
    Function Definition: In this function, students are asked to implement a
    two-point crossover. Choose the subarray from Parent1 starting at
    start_index and ending at end_index. Choose the rest of the sequence
    from Parent 2."""
    child = [None] * len(parent1)
    child[start_index:end_index] = parent1[start_index:end_index]
    child = resolve_conflicts(child, parent2)
    return child

def Mutate(path, mutation_rate):
    """randomly swaps any two cities in path if a random no. is less than mutation rate"""
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(path)), 2)
        path[i], path[j] = path[j], path[i]

def GeneticAlgorithm(cities_list):
    global cities
    cities = cities_list
    n = len(cities)
    # generate intial populaiton
    population = CreateInitialPopulation(POP_SIZE, cities, NUM_NEAREST)
    best_fitness = 0
    # start genetic algorithm loop
    for generation in range(GENERATIONS):
        print(f"gen {generation+1}/{GENERATIONS}")
        # cut population down if it grows too large
        if len(population) > POP_SIZE * 2:
            population = random.sample(population, POP_SIZE * 2)

        fitness_scores = []
        for individual in population:
            temp = fitness_fun(individual)
            if temp > 0:
                fitness_scores.append(1/temp)
            else:
                fitness_scores.append(0)
        
        #If % change in best fitness_score is < 0.01 then terminate
        curr_fitness = max(fitness_scores)
        if curr_fitness==0:
            break
        if best_fitness>0:
            percent_change = (curr_fitness - best_fitness)/best_fitness*100
            if abs(percent_change)<0.01:
                break
        best_fitness = curr_fitness
        # select elites and non-elites from population
        elite_population = CreateElitePool(population, fitness_scores, ELITE_SIZE)
        non_elites = [path for path in population if path not in elite_population]  
        # create mating pool
        parents = CreateMatingPool(non_elites, fitness_scores, POOL_SIZE, TOURNAMENT_SIZE)
        parents += elite_population
        # generate children from mating pool
        children = []
        number_children = NUM_CHILDREN  
        while len(children) < number_children:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)        
            if parent1 != parent2:
                start_index = random.randint(0, len(parent1)-1)
                end_index = random.randint(start_index, len(parent1)-1)                
                child = Crossover(parent1, parent2, start_index, end_index)
                children.append(child)   
        # mutate children
        for child in children:
            Mutate(child, MUTATION_RATE)    
        population += children
    best_indivdual = min(population, key = lambda individual: fitness_fun(individual))
    return best_indivdual, fitness_fun(best_indivdual)

def main():
    with open('input.txt', 'r') as file:
        n = int(file.readline().strip())
        cities = [tuple(map(int, file.readline().split())) for _ in range(n)]   
    if n<= 10:
        best_fitness_score, best_indivdual  = brute_force(cities)
    else:
        best_indivdual, best_fitness_score = GeneticAlgorithm(cities)
    with open('output.txt', 'w') as file:
        file.write(f"{best_fitness_score}\n")
        for i in best_indivdual:
            city = cities[i]
            file.write(f"{city[0]} {city[1]} {city[2]}\n")
        city = cities[best_indivdual[0]]
        file.write(f"{city[0]} {city[1]} {city[2]}\n")

if __name__ == "__main__":
    main()
