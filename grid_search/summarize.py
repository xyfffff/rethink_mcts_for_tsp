import os
import re
import fire

def analyze(N):
    folder_name = f'./results/{N}'

    total_concorde = 0.0
    total_mcts = 0.0
    total_time = 0.0
    total_gap = 0.0
    inst_index_count = 0

    pattern = re.compile(r'Concorde:(\d+\.\d+)\s+MCTS:(\d+\.\d+)\s+Improve:.*?\s+Time:(\d+\.\d+)')

    for filename in os.listdir(folder_name):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_name, filename), 'r') as file:
                content = file.read()
                matches = pattern.finditer(content)
                for match in matches:
                    inst_index_count += 1
                    total_concorde += float(match.group(1))
                    total_mcts += float(match.group(2))
                    total_time += float(match.group(3))
                    total_gap += (total_mcts/total_concorde - 1) * 100

    average_concorde = total_concorde / inst_index_count if inst_index_count else 0
    average_mcts = total_mcts / inst_index_count if inst_index_count else 0
    average_time = total_time / inst_index_count if inst_index_count else 0
    average_gap = total_gap / inst_index_count if inst_index_count else 0

    result = f"Instance Count: {inst_index_count}, Average Concorde: {average_concorde:.5f}, Average MCTS: {average_mcts:.5f}, Average Gap: {average_gap:.5f}%, Average Time: {average_time:.5f}"
    return result

if __name__ == '__main__':
    fire.Fire(analyze)
