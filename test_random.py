import numpy as np
from scipy.spatial import distance
import random
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import time

def generate_random_cities(n):
    """Generate n random 3D cities."""
    return [(random.randint(1, 10000), random.randint(1, 10000), random.randint(1, 10000)) for _ in range(n)]

def compute_distance_matrix(cities):
    """Compute the distance matrix for a list of cities."""
    return distance.cdist(cities, cities)

def tsp_solver_ortools(dist_matrix):
    """Solve TSP using Google OR-Tools."""
    manager = pywrapcp.RoutingIndexManager(len(dist_matrix), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return int(dist_matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)])
    
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        return solution.ObjectiveValue()
    else:
        return float('inf')

def write_test_case(filename, cities):
    """Write the generated cities to the input file."""
    with open(filename, 'w') as file:
        file.write(f"{len(cities)}\n")
        for city in cities:
            file.write(f"{city[0]} {city[1]} {city[2]}\n")

def read_cities_from_file(filename):
    """Read cities from the input file."""
    with open(filename, 'r') as file:
        n = int(file.readline().strip())
        cities = [tuple(map(float, file.readline().split())) for _ in range(n)]
    return cities

def read_output_file(filename):
    """Read the best path and its score from the output file."""
    with open(filename, 'r') as file:
        best_fitness_score = float(file.readline().strip())
        best_individual = []
        for line in file:
            best_individual.append(tuple(map(float, line.split())))
    return best_individual, best_fitness_score

def main():
    # Generate random test cases
    total_score = 0
    time_limits = [(100, 60), (300, 75), (500, 120), (1000, 300)]
    total_score = 0
    for num_cities, time_limit in time_limits:
        for _ in range(5):
            cities = generate_random_cities(num_cities)
            # Write test case to input file
            write_test_case('input.txt', cities)
            
            # Call the main function from your TSP script
            from GA  import main as tsp_main
            
            # Timing the function execution (using CPU time)
            start_time = time.process_time()
            try:
                tsp_main()
                execution_time = time.process_time() - start_time
                if execution_time > time_limit:
                    print(f"Time limit exceeded: {execution_time:.2f}s for {num_cities} cities.")
                    total_score += 0  # Add score as 0 for exceeding time limit
                    break
            except Exception as e:
                print(f"Error executing TSP: {e}")
                total_score += 0  # Add score as 0 for any error
                continue

            # Read the output file
            best_individual, best_fitness_score = read_output_file('output.txt')
            
            # Compute the OR-Tools TSP approximation for comparison
            dist_matrix = compute_distance_matrix(cities)
            tsp_approximation = tsp_solver_ortools(dist_matrix)
            
            # Calculate the score
            score = tsp_approximation / best_fitness_score if best_fitness_score > 0 else 0
            
            # Print the score and time
            print(f"Score: {score}, Time: {execution_time:.2f}s, Cities: {num_cities}")
            
            # Sum up the scores, cap at 1
            total_score += min(score, 1)

    # Print the final score
    print(f"Final Score: {total_score / (5 * len(time_limits))}")
    
if __name__ == "__main__":
    main()
