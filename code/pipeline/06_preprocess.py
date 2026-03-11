import pandas as pd
import numpy as np
import os

print("="*60)
print("PHASE 2: FINAL PREPROCESSING")
print("="*60)

# 1. Load data
input_path = '../data/final_dataset_for_ml.pkl'
print(f"\nLoading dataset from {input_path}...")
df = pd.read_pickle(input_path)

meta_cols = ['sample_id', 'geo_id', 'tissue', 'sex', 'timepoint', 'group']
cpg_cols = [c for c in df.columns if str(c).startswith('cg')]

# 2. Step 1: Remove constant probes (Zero Variance)
print("\nStep 1: Removing constant probes...")
variances = df[cpg_cols].var()
constant_probes = variances[variances == 0].index.tolist()
print(f"  Found {len(constant_probes)} constant probes. Removing them...")
df = df.drop(columns=constant_probes)

# 3. Step 2: Encode labels for the Model
print("\nStep 2: Encoding labels...")
# group_label: Diabetic = 1, Non-diabetic = 0
df['group_label'] = (df['group'] == 'Obese diabetic').astype(int)
# timepoint_label: Post-surgery = 1, Pre-surgery = 0
df['timepoint_label'] = (df['timepoint'] == '52 weeks post metabolic surgery').astype(int)
# sex_label: Male = 1, Female = 0
df['sex_label'] = (df['sex'] == 'male').astype(int)

# 4. Step 3: Create Analysis A (Full Cohort, n=52)
print("\nStep 3: Saving Analysis A (Full Cohort)...")
df.to_pickle('../data/analysis_a_full.pkl')

# 5. Step 4: Create Analysis B (Females Only, n=42)
print("\nStep 4: Saving Analysis B (Females Only)...")
analysis_b = df[df['sex'] == 'female'].copy()
analysis_b.to_pickle('../data/analysis_b_females.pkl')

print("PREPROCESSING COMPLETE")
print(f"Analysis A: {df.shape[0]} samples")
print(f"Analysis B: {analysis_b.shape[0]} samples")