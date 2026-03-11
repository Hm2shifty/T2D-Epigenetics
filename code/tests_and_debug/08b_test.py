'''

import pandas as pd
gold_list = pd.read_csv('../data/gold_list_biomarkers.csv')
print("--- YOUR 5 MASTER BIOMARKERS ---")
print(gold_list)
'''
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import roc_auc_score

def run_honest_ml(df, target):
    cpg_cols = [c for c in df.columns if str(c).startswith('cg')]
    X_all = df[cpg_cols]
    y = df[target]
    
    loo = LeaveOneOut()
    y_true, y_probs = [], []

    print(f"Starting Honest LOOCV for {target}...")

    for train_idx, test_idx in loo.split(X_all):
        # 1. SPLIT FIRST - isolate the test sample completely
        X_train_raw, X_test_raw = X_all.iloc[train_idx], X_all.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        # 2. FEATURE SELECTION INSIDE THE LOOP
        # Pick top 10k probes using ONLY the 51 training samples
        train_vars = X_train_raw.var().sort_values(ascending=False)
        top_10k = train_vars.head(10000).index.tolist()
        
        X_train = X_train_raw[top_10k]
        X_test = X_test_raw[top_10k]

        # 3. TRAIN & PREDICT
        model = RandomForestClassifier(n_estimators=500, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        
        prob = model.predict_proba(X_test)[:, 1]
        y_true.append(y_test.iloc[0])
        y_probs.append(prob[0])

    return roc_auc_score(y_true, y_probs)

# Run the Truth Test
df_females = pd.read_pickle('../data/analysis_b_females.pkl')
honest_auc = run_honest_ml(df_females, 'group_label')

print(f"\n==============================")
print(f"HONEST AUC: {honest_auc:.4f}")
print(f"==============================")