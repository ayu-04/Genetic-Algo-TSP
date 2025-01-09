# Genetic-Algo-TSP

# **Genetic Algorithm for Solving the Traveling Salesman Problem (TSP)**

## **Overview**
This project implements a Genetic Algorithm (GA) to solve the **Traveling Salesman Problem (TSP)**, a classic combinatorial optimization problem. The algorithm is optimized to handle 3D coordinates and includes features such as brute force solving for small datasets, elite selection, mutation, and crossover.

Additionally, it integrates testing using:
- Randomly generated cities (`test_random.py`).
- TSPLIB datasets (`test_tsplib.py`).

---

## **Contents**

### 1. **`GA.py`**
The core implementation of the Genetic Algorithm and brute force solver. Key features include:
- **Brute Force Solver**: Solves TSP for small datasets (≤10 cities).
- **Genetic Algorithm**:
  - Nearest neighbor initialization.
  - Elite and mating pool creation.
  - Two-point crossover and mutation.
  - Fitness evaluation and conflict resolution.
- **Input/Output**:
  - Reads cities from `input.txt`.
  - Outputs the best path and fitness score to `output.txt`.

#### **How to Run**:
```bash
python GA.py
```

#### **Key Functions**:
- `CreateInitialPopulation`: Generates initial solutions using nearest neighbor heuristics.
- `GeneticAlgorithm`: Executes the main GA loop.
- `Mutate`: Randomly swaps two cities in a path.
- `Crossover`: Combines two parents to produce offspring.

---

### 2. **`test_random.py`**
Generates random test cases to validate the algorithm's performance. It compares the GA's solutions to approximations provided by Google OR-Tools.

#### **Features**:
- **Random City Generation**: Creates cities in 3D space.
- **OR-Tools Integration**: Uses OR-Tools for baseline comparison.
- **Time Constraints**: Ensures the algorithm adheres to time limits for different problem sizes.

#### **How to Run**:
```bash
python test_random.py
```

---

### 3. **`test_tsplib.py`**
Tests the Genetic Algorithm on standard TSPLIB problems, which are well-known benchmarks for TSP solutions.

#### **Features**:
- **TSPLIB Dataset Parsing**: Fetches and parses TSPLIB `.tsp` files.
- **Optimal Solution Comparison**: Compares GA solutions with known optimal results.
- **Score Calculation**: Evaluates the quality of GA's solutions relative to optimal values.

#### **How to Run**:
```bash
python test_tsplib.py
```

---

## **How It Works**
1. **Input**:
   - Input is read from `input.txt`. Each city is specified as a 3D coordinate.

   Example:
   ```
   4
   0 0 0
   1 1 1
   2 2 2
   3 3 3
   ```

2. **Execution**:
   - For ≤10 cities: Uses brute force to find the optimal solution.
   - For >10 cities: Runs the Genetic Algorithm.

3. **Output**:
   - Best fitness score (total path length) and the sequence of cities in the path are written to `output.txt`.

   Example:
   ```
   20.1234
   0 0 0
   1 1 1
   2 2 2
   3 3 3
   ```

---

## **Dependencies**
Install the required dependencies before running the project:
```bash
pip install numpy scipy ortools
```

---

## **Highlights**
- Efficient handling of large datasets with Genetic Algorithms.
- Integration with OR-Tools and TSPLIB for validation and benchmarking.
- Modular design for easy testing and customization.

---

## **Future Enhancements**
- Add visualization for the generated paths.
- Experiment with additional crossover and mutation strategies.
- Optimize runtime for larger datasets.
