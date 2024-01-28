import os
import numpy as np
import fire

path = "../../default_mcts"

def calculate_tour_length(coords, tour):
    coords_array = np.array([coords[i-1] for i in tour] + [coords[tour[0]-1]])
    distances = np.linalg.norm(coords_array[:-1] - coords_array[1:], axis=1)
    return np.sum(distances)

def read_tsp_instances(path, N):
    with open(f"{path}/tsp{N}_test_concorde.txt", "r") as file:
        instances = []
        for line in file:
            parts = line.split(" output ")
            coords = list(map(float, parts[0].split())) 
            coords = [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]
            tour = list(map(int, parts[1].split()))    
            instances.append((coords, tour))
        return instances

def process_results(N):
    results_path = f"./results/{N}"
    total_length = 0
    total_time = 0
    count = 0

    instances = read_tsp_instances(path, N)

    for filename in os.listdir(results_path):
        if filename.startswith("result_") and filename.endswith(".txt"):
            with open(f"{results_path}/{filename}", "r") as file:
                next(file)
                for line in file:
                    if line.startswith("Inst_Index"):
                        parts = line.split("\t")
                        index = int(parts[0].split(":")[1]) - 1
                        solution = list(map(int, file.readline().split()[1:]))
                        length = calculate_tour_length(instances[index][0], solution)
                        total_length += length
                        time = float(parts[4].split(":")[1].split()[0])
                        total_time += time
                        count += 1

    average_length = total_length / count if count > 0 else 0
    average_time = total_time / count if count > 0 else 0

    return f"Average Solution Length: {average_length}\nAverage Time: {average_time} Seconds"

def main(N):
    print(process_results(N))

if __name__ == "__main__":
    fire.Fire(main)
