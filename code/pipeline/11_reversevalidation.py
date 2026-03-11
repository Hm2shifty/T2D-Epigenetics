import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score

# 1. LOAD DATA
print("Loading Twin Data (Train) and Original Data (Test)...")
df_twins_beta = pd.read_csv('../data/beta_values_twins.csv', index_col=0).T
df_twins_meta = pd.read_csv('../data/metadata_twins.csv')

df_orig = pd.read_pickle('../data/analysis_a_full.pkl')

# 2. ALIGNMENT
# Get the common sites (all 22,757 sites from the twins are in the 850k)
common_sites = list(set(df_twins_beta.columns).intersection(set(df_orig.columns)))

# Pick the Top 50 most variable sites FROM THE TWIN DATA
top_50_twins = df_twins_beta[common_sites].var().sort_values(ascending=False).head(50).index.tolist()

# 3. PREPARE TRAIN (Twins)
X_train = df_twins_beta[top_50_twins]
y_train = df_twins_meta.set_index('geo_accession').loc[X_train.index]['group_label']

# 4. PREPARE TEST (Original 52)
X_test = df_orig[top_50_twins]
y_test = df_orig['group_label']

# 5. TRAIN & EVALUATE
print(f"Training on {len(X_train)} Twin samples...")
model = RandomForestClassifier(n_estimators=500, random_state=42)
model.fit(X_train, y_train)

print(f"Testing on {len(X_test)} Original samples...")
y_probs = model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, y_probs)

print("-" * 30)
print(f"REVERSE VALIDATION RESULTS")
print(f"AUC: {auc:.4f}")
print("-" * 30)