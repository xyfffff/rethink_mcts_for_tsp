# LKH-3 Runtime
params="14.110521078109741 21.70449709892273 36.79493761062622 66.38069152832031 125.64403963088989 241.49699783325195 476.9617409706116 932.0746085643768 1861.1837575435638"

output_file="T_results_1000.txt"
> "$output_file"

for Param_T in $params; do
    echo "Running solve-1000.sh with Param_T = $Param_T"

    Param_T_Divided=$(echo "$Param_T / 1000 / 2" | bc -l)
    
    bash solve-1000.sh "$Param_T_Divided"

    echo "Running summarize.py for results"
    
    {
        echo "Param_T: $Param_T"
        python summarize.py 1000
    } >> "$output_file"
    
done

echo "All tests completed."
