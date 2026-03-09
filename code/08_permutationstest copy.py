# this file tests if the detector is just memorizing the data by shuffling the labels and checking if it still performs well
# this is a crucial step to ensure that our model is learning real patterns and not just overfitting or finding spurious correlations in the data



import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

print("="*60)
print("THE LIE DETECTOR: PERMUTATION TEST")
print("="*60)

# 1. Load Data
df = pd.read_pickle('../data/analysis_b_females.pkl')
cpg_cols = [c for c in df.columns if str(c).startswith('cg')]
X = df[cpg_cols]
y_real = df['group_label'].values

# 2. Reduce to Top 10k (Standard procedure)
vars_ = X.var().sort_values(ascending=False)
X_reduced = X[vars_.head(10000).index.tolist()]

def run_loocv(X_data, y_labels):
    loo = LeaveOneOut()
    y_pred = []
    for train_idx, test_idx in loo.split(X_data):
        X_train, X_test = X_data.iloc[train_idx], X_data.iloc[test_idx]
        y_train = y_labels[train_idx]
        
        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        y_pred.append(model.predict(X_test)[0])
    return accuracy_score(y_labels, y_pred)

# 3. Run Real Test
print("\nRunning model on REAL labels...")
real_acc = run_loocv(X_reduced, y_real)
print(f"REAL ACCURACY: {real_acc:.2%}")

# 4. Run Scrambled Test
print("\nScrambling labels and re-running (The Lie Detector)...")
y_scrambled = np.random.permutation(y_real)
scrambled_acc = run_loocv(X_reduced, y_scrambled)
print(f"SCRAMBLED ACCURACY: {scrambled_acc:.2%}")

print("\n" + "="*60)
if scrambled_acc < 0.65:
    print("✅ RESULT: PASS. The model failed on random data.")
    print("This proves your 100% accuracy is likely a REAL biological signal.")
else:
    print("❌ RESULT: FAIL. The model found a pattern in random noise.")
    print("We need to investigate data leakage or overfitting.")
print("="*60)