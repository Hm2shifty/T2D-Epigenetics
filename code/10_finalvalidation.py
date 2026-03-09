import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# 1. LOAD DATASETS
print("Loading datasets...")
# Original Data (52 samples)
df_orig = pd.read_pickle('../data/analysis_a_full.pkl') # Assumes this has CpG columns and 'group_label'
# Twin Data (22 samples)
df_twins_beta = pd.read_csv('../data/beta_values_twins.csv', index_col=0).T
df_twins_meta = pd.read_csv('../data/metadata_twins.csv')

# 2. FIND OVERLAP (The "Common Language")
original_cpgs = [c for c in df_orig.columns if c.startswith('cg')]
twin_cpgs = df_twins_beta.columns.tolist()
common_cpgs = list(set(original_cpgs).intersection(set(twin_cpgs)))

print(f"Original Sites: {len(original_cpgs)}")
print(f"Twin Sites (27k chip): {len(twin_cpgs)}")
print(f"Common Sites for testing: {len(common_cpgs)}")

# 3. FEATURE SELECTION (Top 50 from Common Sites)
# We calculate variance on the ORIGINAL data only to pick features
top_50_common = df_orig[common_cpgs].var().sort_values(ascending=False).head(50).index.tolist()

# 4. PREPARE TRAIN (Original) AND TEST (Twins)
X_train = df_orig[top_50_common]
y_train = df_orig['group_label']

# Align twin data with metadata
X_test = df_twins_beta[top_50_common]
y_test = df_twins_meta.set_index('geo_accession').loc[X_test.index]['group_label']

# 5. TRAIN AND EVALUATE
print(f"\nTraining on {len(X_train)} original samples...")
model = RandomForestClassifier(n_estimators=500, max_depth=5, random_state=42)
model.fit(X_train, y_train)

print(f"Testing on {len(X_test)} unseen twins...")
y_probs = model.predict_proba(X_test)[:, 1]
y_pred = model.predict(X_test)

# 6. RESULTS
auc = roc_auc_score(y_test, y_probs)
acc = accuracy_score(y_test, y_pred)

print("-" * 30)
print(f"EXTERNAL VALIDATION RESULTS")
print(f"AUC: {auc:.4f}")
print(f"Accuracy: {acc:.4f}")
print("-" * 30)

# 7. VISUALIZE CONFUSION MATRIX
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Healthy', 'Diabetic'], 
            yticklabels=['Healthy', 'Diabetic'])
plt.title('Confusion Matrix: External Twin Validation')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.savefig('../results/external_validation_matrix.png')
print("Matrix saved to ../results/external_validation_matrix.png")