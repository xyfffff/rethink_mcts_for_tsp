#!/bin/bash

params=$(seq 0.0050 0.0001 0.0060)

for param in $params
do
    echo "Processing with parameter: $param"

    python batch_generate_heatmap.py 1000 $param

    bash solve-1000.sh

    python summarize.py 1000

    echo "Result for param $param" >> grid_search_results_1000.txt
    python summarize.py 1000 >> grid_search_results_1000.txt
    echo "--------" >> grid_search_results_1000.txt 
done

echo "Grid search completed."
