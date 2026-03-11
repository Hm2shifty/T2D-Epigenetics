import pandas as pd
import os

'''
# 1. Define Paths
parquet_path = "../data/GSE270223_full_matrix.parquet"
metadata_path = "../data/metadata_GSE270223.csv"
output_final = "../data/final_monocyte_dataset.parquet"

print("--- ALIGNING DATA WITH GROUND TRUTH ---")

# Load Metadata
meta = pd.read_csv(metadata_path)
meta['geo_id'] = meta['geo_id'].str.strip(' "\'') # Clean potential quotes/spaces
meta = meta.set_index('geo_id')

# Load the Full Matrix
print("Loading 850k feature matrix...")
full_df = pd.read_parquet(parquet_path)

# CLEAN THE MATRIX COLUMN NAMES (Crucial Step!)
full_df.columns = [c.strip(' "\'') for c in full_df.columns]

# 2. Match the IDs
common_ids = meta.index.intersection(full_df.columns)
print(f"Found {len(common_ids)} matching samples.")

# 3. Filter and Reorganize
if len(common_ids) > 0:
    # Filter matrix to only include samples we have metadata for
    final_df = full_df[common_ids].T 
    
    # Create the target column (1 if T2D is in the string, 0 otherwise)
    # We use .loc to make sure we pull the right labels for the right rows
    final_df['target_t2d'] = meta.loc[common_ids, 'sample_id'].str.contains('T2D', case=False).astype(int)

    # 4. Save the "Ready-to-Train" Dataset
    final_df.to_parquet(output_final)

    print("-" * 30)
    print(f"SUCCESS! Final Dataset Ready: {output_final}")
    print(f"Dimensions: {final_df.shape} (Samples x Features+Target)")
else:
    print("-" * 30)
    print("ERROR: No matching IDs found. Check your geo_id formats in both files.")
'''


import pandas as pd
import os

input_file = "../data/GSE270223_betas.txt.gz"
output_parquet = "../data/GSE270223_full_matrix.parquet"

if not os.path.exists(input_file):
    print("Error: The .gz file is missing!")
else:
    print("--- CONVERTING FULL MATRIX (MEMORY-OPTIMIZED) ---")
    
    # We use engine='c' and low_memory=True to handle the 2.2GB efficiently
    # This might take 3-5 minutes depending on your Starbucks laptop's RAM
    df = pd.read_csv(
        input_file, 
        sep='\t', 
        compression='gzip', 
        low_memory=True
    )
    
    print("File loaded into RAM. Cleaning headers...")
    
    # 1. Strip quotes from column names (the GSM IDs)
    df.columns = [c.strip(' "\'') for c in df.columns]
    
    # 2. Set the CpG ID (the first column) as the index
    df.set_index(df.columns[0], inplace=True)
    
    print(f"Matrix shape: {df.shape}. Saving to Parquet...")
    
    # 3. Save as a single Parquet file (No append needed)
    df.to_parquet(output_parquet, engine='pyarrow')

    print("-" * 30)
    print(f"DONE! Full Matrix Saved: {output_parquet}")