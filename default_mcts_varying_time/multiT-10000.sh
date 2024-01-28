
params="165.33927464485168 188.1658320426941 229.6973955631256 333.88902831077576 533.9138493537903 880.459016084671 1566.231909751892 3017.553611755371 5684.314223051071"

output_file="T_results_10000.txt"
> "$output_file"

for Param_T in $params; do
    echo "Running solve-10000.sh with Param_T = $Param_T"

    Param_T_Divided=$(echo "$Param_T / 10000" | bc -l)
    
    bash solve-10000.sh "$Param_T_Divided"

    echo "Running summarize.py for results"
    
    {
        echo "Param_T: $Param_T"
        python summarize.py 10000
    } >> "$output_file"
    
done

echo "All tests completed."
