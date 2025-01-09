import requests

def fetch_tsplib_case(url):
    """Fetch a TSPLIB case from a given URL and convert it to a list of cities in 3D coordinates."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    cities = []
    lines = response.text.splitlines()
    parsing_nodes = False
    for line in lines:
        # Skip metadata lines
        line = line.strip()  # Remove leading/trailing whitespace
        if line.startswith('NODE_COORD_SECTION'):
            parsing_nodes = True  # Start parsing after this line
            continue
        if line.startswith('EOF'):
            break
        if not parsing_nodes:  # Skip all lines before the node section
            continue

        # Parse the coordinate lines
        parts = list(map(float, line.split()))
        if len(parts) == 4:
            cities.append((parts[1], parts[2], parts[3]))  # (x, y, z)
        elif len(parts) == 3:
            cities.append((parts[1], parts[2], 0))  # Pad with z=0 if only x, y

    return cities

def write_to_input_file(cities):
    """Writes the city coordinates to the input file in the format required by the GA."""
    with open('input.txt', 'w') as file:
        file.write(f"{len(cities)}\n")
        for city in cities:
            file.write(f"{int(city[0])} {int(city[1])} {int(city[2])}\n")

def read_output_file():
    """Reads the best fitness score from the output file."""
    with open('output.txt', 'r') as file:
        best_fitness_score = float(file.readline().strip())
    return best_fitness_score

def run_test_on_tsplib_case(tsplib_url, optimal_solution):
    """Run GA using the main function on a TSPLIB problem fetched from the web and compare with the optimal solution."""
    cities = fetch_tsplib_case(tsplib_url)

    # Write the cities to the input file for GA
    write_to_input_file(cities)

    # Call your main function to run the GA (with hyperparameters passed)
    from GA import main as tsp_main
    tsp_main()  # Ensure your main function is set up to read from input.txt

    # Read the output file to get the best fitness score
    my_cost = read_output_file()

    # Compare cost to TSPLIB optimal solution
    score =  optimal_solution / my_cost
    return score

def main_script(tsplib_urls, optimal_solutions):
    total_score = 0
    test_cases = 0

    for url, optimal_solution in zip(tsplib_urls, optimal_solutions):
        print(f"Running test on {url}")

        # Run the test and accumulate the score
        score = run_test_on_tsplib_case(url, optimal_solution)
        print(f"Score for {url}: {score}")
        total_score += score
        test_cases += 1

    # Print the final score
    if test_cases > 0:
        print(f"Total score across {test_cases} test cases: {total_score}")
    else:
        print("No test cases found.")

if __name__ == "__main__":
    tsplib_urls = [
        "https://raw.githubusercontent.com/mastqe/tsplib/master/a280.tsp",
        "https://raw.githubusercontent.com/mastqe/tsplib/master/berlin52.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/bier127.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/ch130.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/ch150.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/eil51.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/eil76.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/eil101.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/kroA100.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/kroB100.tsp",  
        "https://raw.githubusercontent.com/mastqe/tsplib/master/kroC100.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/kroD100.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/kroE100.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/kroA150.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/kroB150.tsp",  
        "https://raw.githubusercontent.com/mastqe/tsplib/master/kroA200.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/kroB200.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/lin105.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/lin318.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/pr107.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/pr136.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/pr144.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/pr152.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/pr226.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/pr264.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/pr299.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/pr439.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/pr76.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/pcb442.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/st70.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/ts225.tsp", 
        "https://raw.githubusercontent.com/mastqe/tsplib/master/tsp225.tsp", 
    ]
    optimal_solutions = [2579, 7542, 118282, 6110, 6528, 426, 538, 629, 
                         21282, 22141, 20749, 21294, 22068, 26524, 26130, 
                         29368, 29437, 14379, 42029, 44303, 96772, 58537, 
                         73682, 80369, 49135, 48191, 107217, 108159, 50778, 
                         675, 126643, 3916]  # Optimal solutions for Berlin52, Euclidean 51, Lin318
    if len(tsplib_urls)!=len(optimal_solutions):
        print('error')
    else:
        main_script(tsplib_urls, optimal_solutions)
