import pandas as pd
import urllib.request
import os
import gzip

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