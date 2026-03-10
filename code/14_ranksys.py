import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, average_precision_score

'''
# 1. LOAD ALL DATA (Universal Intersection)
df_orig = pd.read_pickle('../data/analysis_a_full.pkl')
df_twins = pd.read_csv('../data/beta_values_twins.csv', index_col=0).T
df_exercise = pd.read_csv('../data/GSE114763_beta_values.csv', index_col=0).T

common_sites = list(set(df_orig.columns) & set(df_twins.columns) & set(df_exercise.columns))

# 2. CALCULATE IMPORTANCE WEIGHTS
def get_importance(X, y):
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X, y)
    return model.feature_importances_

print("Ranking sites across all biological conditions...")
# Discovery Weight (T2D vs Obese)
w_discovery = get_importance(df_orig[common_sites], df_orig['group_label'])

# Twin Weight (Genetic Stability)
y_twins = pd.read_csv('../data/metadata_twins.csv', index_col=0)['group_label']
w_twins = get_importance(df_twins[common_sites], y_twins)

# Exercise "Noise" Penalty (Higher variance in exercise = Lower Score)
# We want sites that DON'T change much during exercise
exercise_variance = df_exercise[common_sites].var()
w_noise_penalty = 1 / (exercise_variance + 0.01) # Inverse of variance

# 3. CREATE MASTER RANKING
master_rank = pd.DataFrame(index=common_sites)
master_rank['discovery_score'] = w_discovery
master_rank['twin_score'] = w_twins
master_rank['stability_score'] = w_noise_penalty

# Normalize scores 0-1
master_rank = (master_rank - master_rank.min()) / (master_rank.max() - master_rank.min())

# Calculate Final Universal Rank (Weighted Average)
master_rank['final_score'] = (master_rank['discovery_score'] * 0.5) + \
                             (master_rank['twin_score'] * 0.3) + \
                             (master_rank['stability_score'] * 0.2)

master_rank = master_rank.sort_values('final_score', ascending=False)
master_rank.to_csv('../results/Master_Ranked_Registry.csv')
print("Master Registry Created. Top 5 sites:", master_rank.index[:5].tolist())




'''


import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, average_precision_score
import os

# 1. LOAD ALL DATA
print("Loading Discovery (850k), Exercise (850k), and Twins (27k)...")
df_orig = pd.read_pickle('../data/analysis_a_full.pkl')
df_exercise = pd.read_csv('../data/GSE114763_beta_values.csv', index_col=0).T
df_twins = pd.read_csv('../data/beta_values_twins.csv', index_col=0).T

# 2. FEATURE TIERING & CLEANING
# Filter: Only keep columns that start with 'cg' (removes metadata like 'sex', 'age', etc.)
all_sites = [col for col in df_orig.columns if col.startswith('cg')]
print(f"Cleaned Feature List: Found {len(all_sites)} CpG sites in Discovery data.")

# Intersection for the Twin Robustness Bonus (The 27k anchor)
universal_27k = list(set(all_sites) & set(df_twins.columns))
print(f"Universal Anchor: {len(universal_27k)} sites match the Twin study.")

# 3. COMPUTE THE "STABILITY SCORE" (EXERCISE FILTER)
print("Calculating Stability Scores using Exercise Data...")
# We reindex to ensure we only look at sites present in both, filling missing with high variance (penalty)
ex_subset = df_exercise.reindex(columns=all_sites).fillna(df_exercise.var().mean())
ex_variance = ex_subset.var()
stability_score = 1 / (ex_variance + 0.001) 
stability_norm = (stability_score - stability_score.min()) / (stability_score.max() - stability_score.min())

# 4. COMPUTE THE "SENSITIVITY SCORE" (DISCOVERY IMPORTANCE)
print("Calculating Sensitivity Scores using Discovery Data...")
rf_discovery = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
rf_discovery.fit(df_orig[all_sites], df_orig['group_label'])
sensitivity_score = rf_discovery.feature_importances_
sensitivity_norm = sensitivity_score / sensitivity_score.max()

# 5. CREATE THE MASTER RANKED REGISTRY
registry = pd.DataFrame(index=all_sites)
registry['sensitivity'] = sensitivity_norm
registry['stability'] = stability_norm.values
registry['is_universal'] = 0
registry.loc[universal_27k, 'is_universal'] = 1

# FINAL FORMULA: 50% Sensitivity, 30% Stability, 20% Universal/Twin Proof
registry['final_rank_score'] = (registry['sensitivity'] * 0.5) + \
                               (registry['stability'] * 0.3) + \
                               (registry['is_universal'] * 0.2)

registry = registry.sort_values('final_rank_score', ascending=False)

# Ensure results folder exists
if not os.path.exists('../results'):
    os.makedirs('../results')
registry.to_csv('../results/Unified_Master_Registry.csv')

# 6. VALIDATION: TEST ON THE "LEFT OUT" TWINS
print("Running Validation on Twin Cohort using Top Universal Sites...")
top_50_universal = registry[registry['is_universal'] == 1].head(50).index.tolist()

X_train = df_orig[top_50_universal]
y_train = df_orig['group_label']

# Match columns for Twins
X_test = df_twins.reindex(columns=top_50_universal).fillna(0)
y_test = pd.read_csv('../data/metadata_twins.csv', index_col=0)['group_label']

final_val_model = RandomForestClassifier(n_estimators=1000, random_state=42)
final_val_model.fit(X_train, y_train)
probs = final_val_model.predict_proba(X_test)[:, 1]

print("\n" + "="*40)
print("UNIFIED VALIDATION RESULTS")
print("="*40)
print(f"Top 50 Universal Sites AUC: {roc_auc_score(y_test, probs):.4f}")
print(f"Precision-Recall Score:   {average_precision_score(y_test, probs):.4f}")
print("="*40)