import pandas as pd
import os

# 1. Setup paths
input_file = "../data/GSE272137_processed_data_methylation.tsv.gz"
output_pickle = "../data/methylation_matrix.pkl"

if not os.path.exists(input_file):
    print(f"Error: {input_file} not found. Please download it from GEO first.")
else:
    print("Loading the TSV matrix... this will take a moment (it's 850k rows!)...")
    
    # We use sep='\t' because it's a TSV
    # We use index_col=0 because the first column is the Probe ID (cg...)
    df = pd.read_csv(input_file, sep='\t', compression='gzip', index_col=0)
    
    print("-" * 30)
    print("SUCCESS!")
    print(f"Matrix Shape: {df.shape}")
    print(f"Sample IDs found: {list(df.columns[:5])}...")
    print("-" * 30)
    
    # Save to pickle for instant loading in the ML script
    print("Saving to pickle for fast access...")
    df.to_pickle(output_pickle)
    print("Done!")