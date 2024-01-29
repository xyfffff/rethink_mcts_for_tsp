## Installation

1. **Environment Setup**:
   The project relies on the `fire`, `lkh`, `numpy`, and `torch` libraries. Install them using the following commands:

   ```bash
   pip install fire
   pip install lkh
   pip install numpy
   ```

   Install torch according to your CUDA version. For CUDA 11.4, use:
   ```bash
   pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
   ```

## Heatmap Loading

2. **About Heatmaps**:
   The `all_heatmap` folder contains all heatmaps for heatmap-guided MCTS. The heatmaps for `attgcn`, `dimes`, and `utsp` are directly downloaded from their official GitHub repositories. As `difusco` did not provide heatmaps for download, we replicated their experiments to generate these heatmaps. First, you need to unzip all the heatmaps:

   ```bash
   cd all_heatmap/attgcn
   unzip heatmap.zip
   cd ../difusco
   unzip heatmap.zip
   cd ../dimes
   unzip heatmap.zip
   cd ../utsp
   unzip TSP500_Input.zip
   unzip TSP1000_Input.zip
   ```

   Note: The heatmap format used in `utsp` is inconsistent with the other methods, so some format conversion is needed:
   ```bash
   python reformat_to_default.py 500
   python reformat_to_default.py 1000
   ```

   Then generate heatmaps using our proposed SoftDist method:
   First, unzip the input files:
   ```bash
   cd ../../default_mcts
   unzip tsp500_test_concorde.zip
   unzip tsp1000_test_concorde.zip
   unzip tsp10000_test_concorde.zip
   ```

   Start generating heatmaps using SoftDist:
   ```bash
   cd ../all_heatmap/softdist
   python batch_generate_heatmap.py 500 0.0066
   python batch_generate_heatmap.py 1000 0.0051
   python batch_generate_heatmap.py 10000 0.0018
   cd ../..
   ```

## Testing with Default MCTS Parameters

3. **Test with default MCTS parameters**. Assuming the method name to be tested is `name`, which can be one of `attgcn`, `difusco`, `dimes`, `softdist`, `utsp`. Here is an example of testing `softdist` on TSP-500:

   ```bash
   cd default_mcts
   cp -r ../all_heatmap/softdist/heatmap .
   bash solve-500.sh
   python summarize.py 500
   cd ..
   ```

## Testing MCTS with Varying Time Budgets

4. **Test MCTS with different time budgets (Example for TSP-500)**:
   ```bash
   cd default_mcts_varying_time
   unzip tsp500_test_concorde.zip
   cp -r ../all_heatmap/softdist/heatmap .
   bash multiT-500.sh
   cd ..
   ```

## Testing with UTSP's MCTS Parameters

5. **Test with UTSP's MCTS parameters**. Here is an example of testing `softdist`:
   First, convert the `softdist` heatmap format to the input format required by UTSP’s MCTS:
   ```bash
   cd utsp
   python reformat_to_utsp.py softdist 500
   python reformat_to_utsp.py softdist 1000
   ```

   Start the MCTS, using parameters provided by UTSP:
   ```bash
   cd Search
   bash ./new-solve-500.sh 0 5 100 0 50 2 1 1
   python summarize.py 500
   bash ./new-solve-1000.sh 0 5 10 0 150 3 1
   python summarize.py 1000
   cd ../..
   ```

   Note: In UTSP's MCTS implementation, you need to update the specific value of `#define Max_City_Num` in `TSP_IO.h` according to the current size of the TSP problem.

## Testing UTSP's MCTS with Varying Time Budgets 

6. **Test UTSP version of MCTS with different time budgets (Example for TSP-500)**:
   ```bash
   cd utsp_varying_time
   python reformat_to_utsp.py softdist 500
   python reformat_to_utsp.py softdist 1000
   cd Search
   bash multiT-500.sh
   cd ../..
   ```

   Again, update `#define Max_City_Num` in `TSP_IO.h` according to the TSP problem size.

## Calculating Metric *Score*

7. **To calculate metric indicators**, you need to test the performance of LKH-3 (Example for TSP-500):
   ```bash
   cd calculate_score_metric
   unzip tsp500_test_concorde.zip

   # Ensure LKH-3 is installed and the path is set in lkh_solve.py
   # Adjust the 'runs' parameter to align with the running time of MCTS.
   python lkh_solve.py --N 500 --runs 5

   cd ..
   ```

## Grid Search for SoftDist Temperature Parameter

8. **Grid search for SoftDist's temperature parameter**:
   First, generate a training dataset for grid search, using TSP-500 as an example:
   ```bash
   cd grid_search
   python generate_training_data.py --N 500 --batch 1024
   bash grid_search-500.sh
   ```