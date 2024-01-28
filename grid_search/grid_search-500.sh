#!/bin/bash

params=$(seq 0.0060 0.0001 0.0070)

for param in $params
do
    echo "Processing with parameter: $param"

    python batch_generate_heatmap.py 500 $param

    bash solve-500.sh

    python summarize.py 500

    echo "Result for param $param" >> grid_search_results_500.txt
    python summarize.py 500 >> grid_search_results_500.txt
    echo "--------" >> grid_search_results_500.txt
done

echo "Grid search completed."
