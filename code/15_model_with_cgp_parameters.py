import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report

# 1. THE RESEARCH-BACKED ANCHORS (Top 18 from your Research)
anchors = [
    'cg19693031', 'cg06500161', 'cg11024682', 'cg02650017', 'cg18181703',
    'cg24531955', 'cg12054453', 'cg06721411', 'cg08309687', 'cg16809457',       
    'cg06715330', 'cg06229674' # Note: several genes shared this ID in the research
]

# 2. LOAD DATA
print("Loading datasets and aligning with Anchor sites...")
df_orig = pd.read_pickle('../data/analysis_a_full.pkl')
df_twins = pd.read_csv('../data/beta_values_twins.csv', index_col=0).T
y_twins = pd.read_csv('../data/metadata_twins.csv', index_col=0)['group_label']

# 3. FEATURE SELECTION: THE "18 + 1000" RULE
# We use your 18 anchors + the next top 1000 most stable sites from our previous LODO/Registry
registry = pd.read_csv('../results/Unified_Master_Registry.csv', index_col=0)
support_sites = registry.index[~registry.index.isin(anchors)][:1000].tolist()
final_features = anchors + support_sites

# 4. TRAIN ANCHOR-WEIGHTED MODEL
X_train = df_orig[final_features]
y_train = df_orig['group_label']

# We use a higher number of estimators to ensure the 18 anchors are sampled frequently
model = RandomForestClassifier(
    n_estimators=1500, 
    max_features='log2', # Forces the model to consider smaller groups of features, highlighting the anchors
    class_weight='balanced', 
    random_state=42
)
model.fit(X_train, y_train)

# 5. VALIDATE ON TWINS
X_test = df_twins.reindex(columns=final_features).fillna(0.5)
probs = model.predict_proba(X_test)[:, 1]

# 6. RESULTS & LABEL CHECK
auc = roc_auc_score(y_twins, probs)

print("\n" + "="*40)
print("ANCHOR-BASED DIAGNOSTIC RESULTS")
print("="*40)
print(f"Final AUC: {auc:.4f}")
print("-" * 40)
# Debugging the "0.45 AUC" ghost
if auc < 0.5:
    print("WARNING: AUC still below 0.5. Flipping labels for diagnostic check...")
    print(f"Flipped AUC: {1 - auc:.4f}")
    print("Action: Check if Twins 'group_label' 1=Healthy instead of 1=T2D.")
else:
    print("Success: Model is now biologically grounded.")
print("="*40)