#!/bin/bash

params=$(seq 0.0010 0.0001 0.0020)

for param in $params
do
    echo "Processing with parameter: $param"

    python batch_generate_heatmap.py 10000 $param

    bash solve-10000.sh

    python summarize.py 10000

    echo "Result for param $param" >> grid_search_results_10000.txt
    python summarize.py 10000 >> grid_search_results_10000.txt
    echo "--------" >> grid_search_results_10000.txt
done

echo "Grid search completed."
