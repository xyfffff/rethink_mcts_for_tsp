import fire

def replace_values(name, N):
    # Construct file paths using `name` and `N`
    input_file = f'../all_heatmap/utsp/TSP{N}_Input.txt'
    folder = f'../all_heatmap/{name}'

    # Read the content of the input file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Process each line
    for i, line in enumerate(lines):
        if 'value' in line:
            # Split the line at 'value' and keep the part before it
            parts = line.split('value')
            prefix = parts[0] + 'value'

            # Read the corresponding heatmap file
            heatmap_file = f'{folder}/heatmap/tsp{N}/heatmaptsp{N}_{i}.txt'
            with open(heatmap_file, 'r') as hf:
                heatmap_lines = hf.readlines()[1:]  # skip the first line

            # Extract the N*N numbers from the heatmap file
            new_values = ' '.join(''.join(heatmap_lines).split())

            # Replace the old values with the new ones
            lines[i] = prefix + ' ' + new_values + '\n'

    # Write the modified content to a new file
    new_file = f'./{N}.txt'
    with open(new_file, 'w') as nf:
        nf.writelines(lines)

    return new_file

if __name__ == '__main__':
    fire.Fire(replace_values)
