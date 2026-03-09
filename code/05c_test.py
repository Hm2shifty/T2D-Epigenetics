import pandas as pd
import numpy as np
import os


'''
def run_test():
    file_path = '../data/final_dataset_for_ml.pkl'
    
    if not os.path.exists(file_path):
        print(f"ERROR: Could not find {file_path}")
        return

    print("Reading dataset... (this may take a moment due to size)")
    df = pd.read_pickle(file_path)

    # Separate metadata from CpG columns
    meta_cols = ['sample_id', 'geo_id', 'tissue', 'sex', 'timepoint', 'group']
    cpg_cols = [c for c in df.columns if str(c).startswith('cg')]
    cpg_data = df[cpg_cols]

    print("\n" + "="*30)
    print("      DATASET OVERVIEW")
    print("="*30)
    print(f"Total Samples:  {df.shape[0]}")
    print(f"Total CpG Sites: {len(cpg_cols):,}")

    print("\n--- INTEGRITY CHECK ---")
    missing = cpg_data.isnull().sum().sum()
    print(f"Missing Values: {missing:,}")
    
    # Check data range (Beta values should be 0 to 1)
    b_min = cpg_data.min().min()
    b_max = cpg_data.max().max()
    print(f"Beta Range:     {b_min:.4f} to {b_max:.4f}")

    print("\n--- FEATURE VARIANCE ---")
    # Find probes that are identical across all patients (Zero Variance)
    # Using a small subset check for speed if needed, but here we do the whole thing
    zero_var = (cpg_data.var() == 0).sum()
    print(f"Constant Probes (Zero Var): {zero_var}")

    print("\n--- SAMPLE DISTRIBUTION ---")
    combo = df.groupby(['group', 'timepoint']).size().unstack(fill_value=0)
    print(combo)

    print("\n--- SEX DISTRIBUTION ---")
    sex_dist = df.groupby(['group', 'sex']).size().unstack(fill_value=0)
    print(sex_dist)
    print("="*30)
    
    if missing == 0 and 0 <= b_min <= 1 and 0 <= b_max <= 1:
        print("\n✅ TEST PASSED: Dataset is ready for Model Training.")
    else:
        print("\n⚠️  TEST WARNING: Check range or missing values before training.")

if __name__ == "__main__":
    run_test()
'''

import pandas as pd

# Load your top 50 panel from earlier
top_50_df = pd.read_csv('../data/top_50_diagnostic_panel.csv')
gold_list = top_50_df.iloc[:, 0].tolist() # Assumes CpG IDs are in the first column

# Load the twin data headers (the 27k sites)
twin_data_cols = pd.read_csv('../data/beta_values_twins.csv', nrows=0).columns.tolist()

# Check overlap
overlap = [site for site in gold_list if site in twin_data_cols]
missing = [site for site in gold_list if site not in twin_data_cols]

print(f"--- GOLD LIST SURVIVAL REPORT ---")
print(f"Total Gold List Sites: {len(gold_list)}")
print(f"Present in Twin Data: {len(overlap)}")
print(f"Missing (Not on 27k Chip): {len(missing)}")
print(f"\nAvailable Sites: {overlap[:10]}...")