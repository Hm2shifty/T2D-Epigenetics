import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import roc_auc_score
import warnings

warnings.filterwarnings('ignore')

def run_experiment_honest(df, target_label, experiment_name):
    print(f"\n--- Running HONEST Experiment: {experiment_name} ---")
    
    cpg_cols = [c for c in df.columns if str(c).startswith('cg')]
    X_all = df[cpg_cols]
    y = df[target_label]
    
    loo = LeaveOneOut()
    y_true, y_probs = [], []

    # LOOCV Loop
    for train_idx, test_idx in loo.split(X_all):
        # 1. SPLIT FIRST (Total isolation of the test sample)
        X_train_raw, X_test_raw = X_all.iloc[train_idx], X_all.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        # 2. FEATURE SELECTION INSIDE THE LOOP 
        # (Picking top 10k using ONLY the training samples)
        train_vars = X_train_raw.var().sort_values(ascending=False)
        top_10k_names = train_vars.head(10000).index.tolist()
        
        X_train = X_train_raw[top_10k_names]
        X_test = X_test_raw[top_10k_names]

        # 3. TRAIN
        model = RandomForestClassifier(n_estimators=500, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)

        # 4. PREDICT
        prob = model.predict_proba(X_test)[:, 1]
        y_true.append(y_test.iloc[0])
        y_probs.append(prob[0])

    # Final Metric calculation
    auc = roc_auc_score(y_true, y_probs)
    
    # 5. Get Feature Importance from a final model run (for the Gold List)
    # This is done AFTER the cross-validation is finished
    final_vars = X_all.var().sort_values(ascending=False)
    final_top_10k = final_vars.head(10000).index.tolist()
    final_model = RandomForestClassifier(n_estimators=500, random_state=42, n_jobs=-1)
    final_model.fit(X_all[final_top_10k], y)
    
    importance_df = pd.DataFrame({
        'CpG': final_top_10k,
        'Weight': final_model.feature_importances_
    }).sort_values('Weight', ascending=False).head(100)

    return auc, importance_df

# --- EXECUTION ---
df_a = pd.read_pickle('../data/analysis_a_full.pkl')
df_b = pd.read_pickle('../data/analysis_b_females.pkl')

# Updated calls to the NEW function name
res1_auc, res1_feat = run_experiment_honest(df_a, 'group_label', "1. Diabetes (Everyone)")
res2_auc, res2_feat = run_experiment_honest(df_a, 'timepoint_label', "2. Surgery (Everyone)")
res3_auc, res3_feat = run_experiment_honest(df_b, 'group_label', "3. Diabetes (Females)")
res4_auc, res4_feat = run_experiment_honest(df_b, 'timepoint_label', "4. Surgery (Females)")

print("\n" + "="*45)
print(f"{'EXPERIMENT':<25} | {'AUC-ROC':<10}")
print("-" * 45)
print(f"{'1. Diabetes (Everyone)':<25} | {res1_auc:<10.4f}")
print(f"{'2. Surgery (Everyone)':<25} | {res2_auc:<10.4f}")
print(f"{'3. Diabetes (Females)':<25} | {res3_auc:<10.4f}")
print(f"{'4. Surgery (Females)':<25} | {res4_auc:<10.4f}")
print("="*45)

# Save Gold List
gold_set = set(res1_feat['CpG']).intersection(set(res3_feat['CpG']))
pd.Series(list(gold_set)).to_csv('../data/gold_list_biomarkers.csv', index=False)
print(f"\nGold List saved! {len(gold_set)} overlapping biomarkers found.")