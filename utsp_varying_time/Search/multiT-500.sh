# LKH-3 Runtime
params="6.319660663604736 10.520916223526001 19.312680959701538 37.055044412612915 72.2369282245636 139.80984783172607 275.4425036907196 544.4691386222839 1095.5841400623322"

output_file="T_results_500.txt"
> "$output_file"

for Param_T in $params; do
    echo "Running solve-500.sh with Param_T = $Param_T"

    Param_T_Divided=$(echo "$Param_T / 500 / 2" | bc -l)
    
    bash ./new-solve-500.sh 0 5 100 0 50 2 1 1 "$Param_T_Divided"

    echo "Running summarize.py for results"

    {
        echo "Param_T: $Param_T"
        python summarize.py 500
    } >> "$output_file"
    
done

echo "All tests completed."
