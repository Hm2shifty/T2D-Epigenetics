import pandas as pd
import numpy as np

# 1. Load the dataset
print("Loading final_dataset_for_ml.pkl...")
df = pd.read_pickle("../data/final_dataset_for_ml.pkl")

# 2. Check for Missing Values (The #1 model killer)
n_null = df.isnull().sum().sum()
print(f"Total Missing Values: {n_null}")

# 3. Check Data Ranges (Should be between 0 and 1)
# We only check columns that start with 'cg'
probe_cols = [c for c in df.columns if str(c).startswith('cg')]
min_val = df[probe_cols].min().min()
max_val = df[probe_cols].max().max()
print(f"Data Range: {min_val:.4f} to {max_val:.4f}")

# 4. Check Group Balance (Target variable)
print("\n--- Class Distribution ---")
print(df['group'].value_counts())

# 5. Check Variance
# If a probe has 0 variance (every patient has the same number), it's useless for ML
variances = df[probe_cols].var()
zero_var = (variances == 0).sum()
print(f"\nProbes with Zero Variance: {zero_var}")

if n_null == 0 and 0 <= min_val and max_val <= 1:
    print("\n✅ SYSTEM HEALTHY: Data is clean and ready for Machine Learning.")
else:
    print("\n⚠️ WARNING: Data may need imputation or scaling.")