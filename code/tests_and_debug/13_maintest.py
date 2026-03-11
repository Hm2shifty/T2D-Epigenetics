import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os

# 1. SETUP PATHS
DATA_DIR = "../data/"
ORIGINAL_DATA = os.path.join(DATA_DIR, "analysis_a_full.pkl")
GOLD_LIST = os.path.join(DATA_DIR, "top_50_diagnostic_panel.csv")
EXERCISE_BETA = os.path.join(DATA_DIR, "GSE114763_beta_values.csv")
EXERCISE_META = os.path.join(DATA_DIR, "GSE114763_metadata.csv")

print("--- STARTING SPECIFICITY VALIDATION ---")

# 2. LOAD DISCOVERY DATA & TRAIN MODEL
# We train on the original 52 samples using your validated Gold List
print("Step 1: Training model on original Discovery Cohort...")
df_orig = pd.read_pickle(ORIGINAL_DATA)
top_50_df = pd.read_csv(GOLD_LIST)
top_50 = top_50_df.iloc[:, 0].tolist() # Assumes CpG IDs are in the first column

X_train = df_orig[top_50]
y_train = df_orig['group_label']

model = RandomForestClassifier(n_estimators=1000, random_state=42)
model.fit(X_train, y_train)

# 3. LOAD EXERCISE DATA (The "Negative Control")
print("Step 2: Loading Exercise Validation Data (GSE114763)...")
# Transposing because GEO matrices usually have samples as columns
df_exercise_beta = pd.read_csv(EXERCISE_BETA, index_col=0).T

# Filter exercise data to only include your 50 sites
# We use .reindex to ensure we don't crash if a site is somehow missing
X_test_exercise = df_exercise_beta.reindex(columns=top_50).fillna(0)

# 4. PREDICT
print("Step 3: Running predictions on healthy muscle samples...")
preds = model.predict(X_test_exercise)
probs = model.predict_proba(X_test_exercise)[:, 1]

# 5. FINAL REPORT
print("\n" + "="*30)
print(f"SPECIFICITY TEST RESULTS")
print("="*30)
print(f"Total Healthy Exercise Samples: {len(preds)}")
print(f"Mistakenly flagged as T2D:      {sum(preds)}")
print(f"Correctly identified as Healthy: {len(preds) - sum(preds)}")
print(f"Mean 'Diabetic Risk' Probability: {probs.mean():.4f}")
print("="*30)

if sum(preds) == 0:
    print("\nVERDICT: SUCCESS. The model has 100% Specificity.")
    print("It correctly distinguished T2D biology from exercise-induced muscle changes.")
else:
    print(f"\nVERDICT: PARTIAL. {sum(preds)} samples were flagged.")
    print("Note: Check if flagged samples are 'reloading' phase (intense muscle growth).")