import pandas as pd
import urllib.request
import os
import gzip

'''
# 1. Define paths
url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE272nnn/GSE272137/matrix/GSE272137_series_matrix.txt.gz"
dest = "../data/GSE272137_series_matrix.txt.gz"
output_pickle = "../data/methylation_matrix.pkl"

if not os.path.exists(dest):
    print("Downloading...")
    urllib.request.urlretrieve(url, dest)

# 2. Improved Loading Logic
print("Loading the matrix... searching for data start...")

# We need to skip the metadata lines at the top. 
# We'll open the file briefly to find which line the table starts on.
skip_rows = 0
with gzip.open(dest, 'rt') as f:
    for i, line in enumerate(f):
        if line.startswith('!series_matrix_table_begin'):
            skip_rows = i + 1
            break

print(f"Skipping {skip_rows} metadata rows...")

# 3. Load the data table
# We skip the metadata, but the first row after 'table_begin' is our header
df = pd.read_csv(dest, 
                 sep='\t', 
                 compression='gzip', 
                 skiprows=skip_rows,
                 index_col=0)

# 4. Cleanup
# GEO matrices often have a '!series_matrix_table_end' row at the bottom
if "!series_matrix_table_end" in df.index:
    df = df.drop("!series_matrix_table_end")

print("-" * 30)
print(f"Success! Matrix Loaded.")
print(f"Features (Probes): {df.shape[0]}")
print(f"Samples (Patients): {df.shape[1]}")
print("-" * 30)

# 5. Save
df.to_pickle(output_pickle)
print(f"Saved to {output_pickle}")
'''

import pandas as pd
import os
import gzip

# 1. Define paths
file_path = "../data/GSE38291_series_matrix.txt.gz"
output_meta_path = "../data/metadata_twins.csv"
output_beta_path = "../data/beta_values_twins.csv"

if not os.path.exists(file_path):
    print(f"Error: {file_path} not found.")
else:
    print(f"Parsing Twin Dataset: {file_path}...")

    # 2. Extract Metadata from the header section
    metadata_dict = {}
    characteristics_count = 0
    
    with gzip.open(file_path, 'rt') as f:
        for line in f:
            if line.startswith("!series_matrix_table_begin"):
                break 
            if line.startswith("!Sample_"):
                parts = line.strip().split("\t")
                key = parts[0].replace("!Sample_", "")
                
                # Handle multiple 'characteristics_ch1' entries
                if key == "characteristics_ch1":
                    if characteristics_count == 0:
                        key = "status"
                    elif characteristics_count == 1:
                        key = "sex"
                    elif characteristics_count == 2:
                        key = "age"
                    characteristics_count += 1
                
                values = [p.replace('"', '') for p in parts[1:]]
                metadata_dict[key] = values

    # 3. Create DataFrame and Clean
    df_meta = pd.DataFrame(metadata_dict)
    
    # Selecting the specific columns based on your inspection
    keep_cols = ['title', 'geo_accession', 'status', 'sex', 'age']
    df_meta_clean = df_meta[keep_cols].copy()
    
    # Clean text (e.g., "type 2 diabetes status: type 2 diabetic" -> "type 2 diabetic")
    df_meta_clean['status'] = df_meta_clean['status'].apply(lambda x: x.split(':')[-1].strip())
    df_meta_clean['sex'] = df_meta_clean['sex'].apply(lambda x: x.split(':')[-1].strip())
    df_meta_clean['age'] = df_meta_clean['age'].apply(lambda x: x.split(':')[-1].strip())

    # IMPORTANT: The Twin dataset has both Muscle and Fat. 
    # Let's filter for MUSCLE samples only to match your training data.
    df_meta_clean = df_meta_clean[df_meta_clean['title'].str.contains('muscle', case=False)].copy()
    
    # Standardize 'group' names for your ML model
    # Convert 'type 2 diabetic' -> 1 and 'non-diabetic' -> 0 (matching your previous labels)
    df_meta_clean['group_label'] = df_meta_clean['status'].map({
        'type 2 diabetic': 1,
        'non-diabetic': 0
    })

    df_meta_clean.to_csv(output_meta_path, index=False)
    print(f"Success: Metadata saved with {len(df_meta_clean)} muscle samples.")

    # 4. Extract Methylation Data (Beta Values)
    print("Loading Beta Values (This takes ~1 min)...")
    # comment='!' skips all lines starting with ! including the header junk
    df_beta = pd.read_csv(file_path, sep="\t", compression='gzip', comment='!', index_col=0)
    
    # Filter columns to only include the muscle samples we just kept in metadata
    muscle_geo_ids = df_meta_clean['geo_accession'].tolist()
    df_beta_muscle = df_beta[muscle_geo_ids]

    df_beta_muscle.to_csv(output_beta_path)
    print(f"Success: Beta values saved to {output_beta_path}")
    print("-" * 30)
    print(f"Twin pairs found: {len(df_meta_clean) // 2}")