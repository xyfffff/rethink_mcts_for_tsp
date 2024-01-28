import numpy as np
import fire

def generate_tsp_instances(N, batch):
    """
    Generate TSP instances of size N for given batch size.
    Each instance is a 2D Euclidean TSP problem.
    """
    np.random.seed(1234)  # Set random seed for reproducibility
    tsp_instances = []

    for _ in range(batch):
        # Generate N points within a unit square (0,1)x(0,1)
        points = np.random.rand(N, 2)

        # Flatten the points into a single line
        flattened_points = points.flatten()
        flattened_points_str = ' '.join(map(str, flattened_points))

        # Create solution format as integers
        solution_format = list(range(1, N + 1)) + [1]
        solution_format_str = ' '.join(map(str, solution_format))

        # Combine the two string parts
        instance = flattened_points_str + ' output ' + solution_format_str

        tsp_instances.append(instance)

    return tsp_instances

def write_to_file(filename, tsp_instances):
    """
    Write TSP instances to a file.
    """
    with open(filename, "w") as file:
        for instance in tsp_instances:
            file.write(instance + "\n")

def main(N, batch):
    # Generate TSP instances
    tsp_instances = generate_tsp_instances(N, batch)

    # Write instances to a file
    filename = f"tsp{N}_test_concorde.txt"
    write_to_file(filename, tsp_instances)

    print(f"TSP instances written to {filename}")

if __name__ == "__main__":
    fire.Fire(main)