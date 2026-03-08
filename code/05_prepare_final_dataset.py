import pandas as pd
import sys

# 1. Load the data
print("--- LOADING DATA ---")
try:
    metadata = pd.read_csv("../data/metadata_final.csv")
    matrix = pd.read_pickle("../data/methylation_matrix.pkl")
except FileNotFoundError as e:
    print(f"Error: Could not find files. {e}")
    sys.exit()

# 2. Transpose the matrix so patients are rows
X = matrix.T 

# 3. INSPECTION (The "No-Guess" Part)
print("\n--- METADATA INSPECTION ---")
print(f"Metadata Columns: {metadata.columns.tolist()}")
print(f"Metadata Index:   {metadata.index.name}")
print(f"First 3 IDs in Metadata ['sample_id']:\n{metadata['sample_id'].head(3).tolist()}")

print("\n--- MATRIX INSPECTION ---")
print(f"Matrix Index Name: {X.index.name}")
print(f"First 3 IDs in Matrix Index:\n{X.index[:3].tolist()}")

# 4. PRECISE MATCHING LOGIC
# We are checking if the strings actually match or if there is hidden whitespace
sample_meta = str(metadata['sample_id'].iloc[0]).strip()
sample_matrix = str(X.index[0]).strip()

if sample_meta == sample_matrix:
    print(f"\n✅ Match confirmed: '{sample_meta}' matches '{sample_matrix}'")
else:
    print(f"\n❌ MISMATCH: '{sample_meta}' does not equal '{sample_matrix}'")
    sys.exit("Stopping: Identifiers do not match. Check for prefixes or suffixes.")

# 5. THE MERGE
# We use 'inner' to ensure we only keep rows where IDs exist in both files
final_df = metadata.merge(X, left_on='sample_id', right_index=True, how='inner')

# 6. VERIFICATION
print("\n--- FINAL DATASET VERIFICATION ---")
if final_df.empty:
    print("Error: The merge resulted in an empty DataFrame. The IDs might look similar but aren't identical.")
else:
    print(f"Success! Final Shape: {final_df.shape}")
    print(f"Confirming target 'group' column exists: {'group' in final_df.columns}")
    
    # Save the result
    final_df.to_pickle("../data/final_dataset_for_ml.pkl")
    print("Saved: ../data/final_dataset_for_ml.pkl")