import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import roc_auc_score
import warnings

warnings.filterwarnings('ignore')

def evaluate_n_features(df, target, n_features):
    """Runs Honest LOOCV using exactly n_features selected within the loop."""
    cpg_cols = [c for c in df.columns if str(c).startswith('cg')]
    X_all = df[cpg_cols]
    y = df[target]
    
    loo = LeaveOneOut()
    y_true, y_probs = [], []

    for train_idx, test_idx in loo.split(X_all):
        X_train_raw, X_test_raw = X_all.iloc[train_idx], X_all.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        # Feature Selection INSIDE the loop
        train_vars = X_train_raw.var().sort_values(ascending=False)
        top_n_names = train_vars.head(n_features).index.tolist()
        
        X_train = X_train_raw[top_n_names]
        X_test = X_test_raw[top_n_names]

        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)

        prob = model.predict_proba(X_test)[:, 1]
        y_true.append(y_test.iloc[0])
        y_probs.append(prob[0])

    return roc_auc_score(y_true, y_probs)

# --- EXECUTION ---
df = pd.read_pickle('../data/analysis_a_full.pkl')
feature_counts = [2, 5, 10, 25, 50, 100, 500, 1000, 5000, 10000]
results = []

print("Starting Feature Optimization Scan...")
for n in feature_counts:
    auc = evaluate_n_features(df, 'group_label', n)
    print(f"Tested Top {n:>5} sites | AUC: {auc:.4f}")
    results.append(auc)

# --- PLOTTING THE ELBOW CURVE ---
plt.figure(figsize=(10, 6))
plt.plot(feature_counts, results, marker='o', linestyle='-', color='#2c3e50', linewidth=2)
plt.xscale('log') # Use log scale to see the small numbers clearly
plt.title('Diagnostic Optimization: AUC vs. Number of CpG Sites', fontsize=14)
plt.xlabel('Number of Targeted CpG Sites (Log Scale)', fontsize=12)
plt.ylabel('Model Accuracy (AUC-ROC)', fontsize=12)
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.axvline(x=50, color='r', linestyle='--', label='Proposed 50-Site Panel')
plt.legend()
plt.savefig('../results/optimization_elbow_plot.png')
print("\nOptimization plot saved to ../results/optimization_elbow_plot.png")

# --- SAVE THE FINAL TOP 50 LIST ---
# We use the full dataset variance for the final export list
final_vars = df[[c for c in df.columns if str(c).startswith('cg')]].var().sort_values(ascending=False)
top_50_list = final_vars.head(50).index.tolist()
pd.DataFrame({'CpG_ID': top_50_list}).to_csv('../data/top_50_diagnostic_panel.csv', index=False)
print("Top 50 Diagnostic Panel saved to ../data/top_50_diagnostic_panel.csv")