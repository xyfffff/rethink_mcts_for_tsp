import fire

def process_file(N):
    input_filename = f'TSP{N}_Input.txt'

    with open(input_filename, 'r') as file:
        for i, line in enumerate(file):
            # Extracting the numbers after the word 'value'
            numbers = line.split('value ')[1]
            # Converting the string of numbers to a list of floats
            float_numbers = list(map(float, numbers.split()))
            # Ensuring we have exactly N*N numbers
            if len(float_numbers) != N * N:
                raise ValueError(f"Line {i+1} does not contain {N*N} numbers.")
            
            # Writing the numbers to the output file
            output_filename = f'./heatmap/tsp{N}/heatmaptsp{N}_{i}.txt'
            with open(output_filename, 'w') as output_file:
                output_file.write(f'{N}\n')
                for j in range(N):
                    row = ' '.join(map(str, float_numbers[j*N:(j+1)*N]))
                    output_file.write(row + '\n')

    print("Processing complete.")

if __name__ == '__main__':
    fire.Fire(process_file)
