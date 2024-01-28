import numpy as np
import lkh
from concurrent.futures import ProcessPoolExecutor
import functools
from lkh import LKHProblem
import time
import fire

import random
random.seed(1234)


class MyLKHProblem(LKHProblem):
    def __init__(self, coords):
        super().__init__()
        self.name = 'TSP'
        self.type = 'TSP'
        self.dimension = len(coords)
        self.edge_weight_type = 'EUC_2D'
        self.node_coords = {n + 1: (coords[n, 0], coords[n, 1]) for n in range(self.dimension)}

def solve_single_instance(coords, lkh_path, max_trials, runs, seed):
    scale = 1e6
    coords_scaled = coords * scale
    problem = MyLKHProblem(coords_scaled)

    start_time = time.time()
    solution = lkh.solve(lkh_path, problem=problem, max_trials=max_trials, runs=runs, seed=seed)
    end_time = time.time()

    tour = [n for n in solution[0]]
    length = calculate_path_length(coords, tour)
    elapsed_time = end_time - start_time
    
    return tour, length, elapsed_time

def solve_tsp_lkh(instances, lkh_path, max_trials=1000, runs=10, seed=1234, num_workers=None):
    """
    Solve TSP instances using the LKH algorithm in parallel using multiprocessing.

    :param instances: List of TSP instances, each instance is a NumPy array of coordinates.
    :param lkh_path: Path to the LKH executable.
    :param max_trials: Maximum number of trials for each LKH run.
    :param runs: Number of LKH runs for each instance.
    :param seed: Random seed for each LKH run.
    :param num_workers: Number of parallel workers (processes) to use. If None, it uses as many as the machine's CPU cores.
    :return: List of tours (1-based index) and corresponding lengths.
    """
    lkh_solutions = []
    lkh_lengths = []
    lkh_times = []

    partial_solve = functools.partial(solve_single_instance, lkh_path=lkh_path, 
                                      max_trials=max_trials, runs=runs, seed=seed)

    total_start_time = time.time()

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(partial_solve, instances))

    total_end_time = time.time()
    total_elapsed_time = total_end_time - total_start_time
    print("TOTAL TIME IS: ", total_elapsed_time)


    for tour, length, elapsed_time in results:
        lkh_solutions.append(tour)
        lkh_lengths.append(length)
        lkh_times.append(elapsed_time)

    return lkh_solutions, lkh_lengths, lkh_times


def read_tsp_instances(file_path):
    with open(file_path, 'r') as file:
        instances = []
        optimal_solutions = []

        for line in file:
            parts = line.strip().split(" output ")
            coordinates_part = parts[0]
            solution_part = parts[1]

            coords = [float(x) for x in coordinates_part.split()]
            coords = np.array(coords).reshape(-1, 2)
            instances.append(coords)

            solution = [int(x) for x in solution_part.split()]
            optimal_solutions.append(solution[:-1])

        return instances, optimal_solutions

def calculate_path_length(coords, tour):
    """
    Calculate the total length of the TSP tour.

    :param coords: NumPy array of shape (N, 2) containing coordinates of the nodes.
    :param tour: List of node indices (starting from 1) representing the tour.
    :return: Total length of the path.
    """
    adjusted_tour = np.array(tour) - 1
    rolled_tour = np.roll(adjusted_tour, -1)
    distances = np.linalg.norm(coords[adjusted_tour] - coords[rolled_tour], axis=1)
    return np.sum(distances)


def main(N=1000, max_trials=10000, runs=10, seed=1234, num_workers=None):
    file_path = f"./tsp{N}_test_concorde.txt"
    lkh_path = '/home/v-yifanxia/experiment/LKH-3.0.9/LKH'

    instances, optimal_solutions = read_tsp_instances(file_path)

    optimal_lengths = [calculate_path_length(inst, sol) for inst, sol in zip(instances, optimal_solutions)]
    avg_optimal_length = sum(optimal_lengths) / len(optimal_lengths)
    print("Average Optimal Path Length:", avg_optimal_length)

    lkh_solutions, lkh_lengths, lkh_times = solve_tsp_lkh(instances, lkh_path, 
                                                        max_trials=max_trials, 
                                                        runs=runs, 
                                                        seed=seed, 
                                                        num_workers=num_workers)
    avg_lkh_length = sum(lkh_lengths) / len(lkh_lengths)
    avg_time = sum(lkh_times) / len(lkh_times)
    print("Average LKH Path Length:", avg_lkh_length)
    print("Average LKH Time:", avg_time)
        

if __name__ == '__main__':
    fire.Fire(main)