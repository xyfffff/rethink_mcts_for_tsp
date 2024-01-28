import torch
import torch.nn.functional as F
import numpy as np
import os
import time
import fire
from multiprocessing import Pool

def is_power_of_two(n):
    return (n != 0) and (n & (n - 1) == 0)

def create_heatmap_matrix(batch_coords, t, device="cuda:0"):
    batch_coords = torch.tensor(batch_coords, device=device).float()

    start_time = time.time()

    coord_diff = batch_coords[:, :, None, :] - batch_coords[:, None, :, :]
    distance_matrix = torch.sqrt(torch.sum(coord_diff ** 2, dim=-1))
    eye = torch.eye(distance_matrix.size(1), device=device).unsqueeze(0)
    distance_matrix = torch.where(eye == 1, torch.tensor(float('inf'), dtype=torch.float, device=device), distance_matrix)
    heatmap = F.softmax(- distance_matrix / t, dim=2)

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Heatmap generation took {elapsed_time} seconds")

    return heatmap.cpu().numpy()


def read_tsp_file(file_path, N):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    data = []
    for line in lines:
        parts = line.strip().split(" output ")
        coords_flat = np.array(parts[0].split(), dtype=np.float32)
        data.append(coords_flat[:2*N])
    data = np.array(data).reshape(-1, N, 2)
    return data

def write_heatmap_to_file(args):
    heatmap_matrix, output_file, N = args
    with open(output_file, 'w') as out_file:
        out_file.write(f"{N}\n")
        for row in heatmap_matrix:
            out_file.write(' '.join(map(str, row)) + '\n')

def process_tsp_data(N, temperature, device="cuda:0"):
    file_path = f"./tsp{N}_test_concorde.txt"
    batch_coords = read_tsp_file(file_path, N)
    
    os.makedirs(f"./heatmap/tsp{N}", exist_ok=True)

    try:
        heatmap_matrices = create_heatmap_matrix(batch_coords, temperature, device)
        args = [(heatmap_matrix, f"./heatmap/tsp{N}/heatmaptsp{N}_{i}.txt", N) 
                for i, heatmap_matrix in enumerate(heatmap_matrices)]
        with Pool() as pool:
            pool.map(write_heatmap_to_file, args)
        print("Processed in a single batch.")

    except RuntimeError as e:
        print(f"Error occurred: {e}. Please enter a valid batch size (must be a power of two and less than or equal to {len(batch_coords)}):")

        while True:
            try:
                batch_size = int(input("Enter batch size: "))
                if not is_power_of_two(batch_size) or batch_size > len(batch_coords):
                    raise ValueError
                break
            except ValueError:
                print("Invalid batch size. It must be a power of two and less than or equal to the total number of batches.")

        for i in range(0, len(batch_coords), batch_size):
            batch = batch_coords[i:i+batch_size]
            heatmap_matrices = create_heatmap_matrix(batch, temperature, device)
            
            args = [(heatmap_matrix, f"./heatmap/tsp{N}/heatmaptsp{N}_{i+j}.txt", N) 
                    for j, heatmap_matrix in enumerate(heatmap_matrices)]
            
            with Pool() as pool:
                pool.map(write_heatmap_to_file, args)


def process_batch(batch_coords, temperature, N, batch_size, device):
    for i in range(0, len(batch_coords), batch_size):
        batch = batch_coords[i:i+batch_size]
        heatmap_matrices = create_heatmap_matrix(batch, temperature, device)
        
        args = [(heatmap_matrix, f"./heatmap/tsp{N}/heatmaptsp{N}_{i+j}.txt", N) 
                for j, heatmap_matrix in enumerate(heatmap_matrices)]
        
        with Pool() as pool:
            pool.map(write_heatmap_to_file, args)

def process_tsp_data(N, temperature, device="cuda:0"):
    file_path = f"./tsp{N}_test_concorde.txt"
    batch_coords = read_tsp_file(file_path, N)
    
    os.makedirs(f"./heatmap/tsp{N}", exist_ok=True)
    
    try:
        process_batch(batch_coords, temperature, N, len(batch_coords), device)
        print("Processed in a single batch.")

    except RuntimeError as e:
        print(f"Error occurred: {e}. Please enter a valid batch size (must be a power of two and less than or equal to {len(batch_coords)}):")
        
        while True:
            try:
                batch_size = int(input("Enter batch size: "))
                if not is_power_of_two(batch_size) or batch_size > len(batch_coords):
                    raise ValueError
                
                process_batch(batch_coords, temperature, N, batch_size, device)
                break

            except ValueError:
                print("Invalid batch size. It must be a power of two and less than or equal to the total number of batches.")
            except RuntimeError as e:
                print(f"Error occurred again: {e}. Please enter a smaller batch size:")


def main(N, temperature):
    process_tsp_data(N, temperature)

if __name__ == "__main__":
    fire.Fire(main)
