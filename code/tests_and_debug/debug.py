import os
import GEOparse
'''

file_path = "../data/GSE272137_family.soft.gz"

if not os.path.exists(file_path):
    print("File not found! Check your paths.")
else:
    print(f"Opening {file_path}...")
    gse = GEOparse.get_GEO(filepath=file_path, silent=True)
    
    # 1. Check the first Sample (GSM)
    first_gsm_id = list(gse.gsms.keys())[0]
    gsm = gse.gsms[first_gsm_id]
    
    print(f"\n--- Testing Sample: {first_gsm_id} ---")
    print(f"Table columns: {gsm.table.columns.tolist()}")
    print(f"Table shape: {gsm.table.shape}")
    
    # 2. Check the Platform (GPL) - sometimes data is linked here
    first_gpl_id = list(gse.gpls.keys())[0]
    gpl = gse.gpls[first_gpl_id]
    
    print(f"\n--- Testing Platform: {first_gpl_id} ---")
    print(f"Platform Table columns (first 5): {gpl.table.columns.tolist()[:5]}")
    print(f"Platform Table shape: {gpl.table.shape}")

    # 3. Check for "Columns" metadata
    if not gsm.table.empty:
        print("\nSuccess: Data found in GSM table.")
    else:
        print("\nNotice: GSM table is empty. The SOFT file likely contains metadata only.")
        print("We should proceed with the Series Matrix download.")



gse = GEOparse.get_GEO(filepath="../data/GSE272137_family.soft.gz", silent=True)
first_gsm = list(gse.gsms.keys())[0]
print(f"The columns for {first_gsm} are:")
print(gse.gsms[first_gsm].table.columns.tolist())





file_path = "./data/GSE221660_series_matrix.txt"

if not os.path.exists(file_path):
    print("File not found! Make sure you extracted it.")
else:
    print("--- FIRST 100 LINES PREVIEW ---")
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for i in range(100):
            line = f.readline()
            if not line:
                break
            # We use repr() to see hidden characters like \t (tabs) or \n (newlines)
            print(f"Line {i}: {repr(line[:100])}")


import pandas as pd

# Load just the beginning to verify
path = "../data/final_monocyte_dataset.parquet"
df_check = pd.read_parquet(path)

print("--- DATASET VERIFICATION ---")
print(f"Rows (People): {df_check.shape[0]}")
print(f"Columns (DNA Sites): {df_check.shape[1]}")
print("\nFirst 5 Rows and 5 Columns:")
print(df_check.iloc[:5, :5])


import pandas as pd

parquet_path = "../data/GSE270223_full_matrix.parquet"
metadata_path = "../data/metadata_GSE270223.csv"

# 1. Check Metadata IDs
meta = pd.read_csv(metadata_path)
print("--- METADATA ID CHECK ---")
print(f"Column names: {list(meta.columns)}")
print("First 5 IDs in 'geo_id' column:")
print(meta['geo_id'].head().values)

# 2. Check Parquet IDs
print("\n--- PARQUET ID CHECK ---")
# We only load the header (columns) to save time/RAM
df_cols = pd.read_parquet(parquet_path, columns=[]) 
print(f"Total columns in Parquet: {len(df_cols.columns)}")
print("First 5 column names in Parquet:")
print(list(df_cols.columns[:5]))

# 3. Check for obvious mismatches
sample_meta = str(meta['geo_id'].iloc[0])
sample_para = str(df_cols.columns[0])

if sample_meta in sample_para or sample_para in sample_meta:
    print("\n[!] The IDs look similar but might have extra characters (like quotes or spaces).")
else:
    print("\n[!] The IDs look totally different. We might be using 'GSM123' in one and 'Sample_1' in the other.")
    
import pandas as pd
parquet_path = "../data/GSE270223_full_matrix.parquet"

try:
    # Load just the header
    df_cols = pd.read_parquet(parquet_path, columns=[])
    cols = list(df_cols.columns)
    print(f"Total Columns found: {len(cols)}")
    if len(cols) > 0:
        print("First 5 column names in your data:")
        print(cols[:5])
    else:
        print("The Parquet file is EMPTY. We need to re-run the converter.")
except Exception as e:
    print(f"Error reading Parquet: {e}")

'''
import gzip
import pandas as pd

soft_path = "../data/GSE270223_family.soft.gz"
mapping = {} # {GSM: Barcode}

print("--- SCANNING FOR CONCRETE ID LINKS ---")

with gzip.open(soft_path, 'rt', encoding='utf-8') as f:
    current_gsm = None
    for line in f:
        # Detect the start of a new Sample block
        if line.startswith("^SAMPLE"):
            current_gsm = line.split('=')[1].strip()
        
        # Look for the barcode pattern (XXXXXXXXXXXX_RXXCXX)
        # We look in every line related to this sample
        if current_gsm:
            # Common tags for barcodes: Supplementary_file, Description, or Title
            import re
            match = re.search(r'(\d{10,}_R\d{2}C\d{2})', line)
            if match:
                mapping[current_gsm] = match.group(1)
                # Reset current_gsm so we don't pick up duplicate IDs for one sample
                current_gsm = None 

print(f"Concrete evidence found for {len(mapping)} samples.")

if len(mapping) > 0:
    # Convert to a DataFrame for proof
    evidence_df = pd.DataFrame(list(mapping.items()), columns=['geo_id', 'barcode'])
    evidence_df.to_csv("../data/concrete_id_map.csv", index=False)
    print("\nSample of Proof:")
    print(evidence_df.head())
else:
    print("Barcode not found in SOFT file. We may need to check the 'IDAT' file headers.")