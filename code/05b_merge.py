import pandas as pd
import os

base_dir = r"C:\Users\hethm\Project\epigenetics_project\data"
parquet_path = os.path.join(base_dir, "GSE270223_full_matrix.parquet")
mapping_path = os.path.join(base_dir, "concrete_id_map.csv")
metadata_path = os.path.join(base_dir, "metadata_GSE270223.csv")
output_final = os.path.join(base_dir, "final_monocyte_dataset.parquet")

print("1. Loading small metadata files...")
mapping = pd.read_csv(mapping_path)
id_dict = dict(zip(mapping['barcode'], mapping['geo_id']))
meta = pd.read_csv(metadata_path)
meta['geo_id'] = meta['geo_id'].str.replace(r'[^a-zA-Z0-9]', '', regex=True)
meta_idx = meta.set_index('geo_id')

print("2. Reading and Transposing in one step...")
# By reading only the columns we need and immediate transpose, we save RAM
df = pd.read_parquet(parquet_path)

# Filter columns to only those in our mapping
common = [b for b in df.columns if b in id_dict]
df = df[common]

print("3. Swapping Barcodes for GSM IDs...")
df.columns = [id_dict[b] for b in df.columns]

print("4. Transposing (Flipping the Matrix)...")
# We use .T and immediately convert to float32 to shrink the size
final_df = df.T.astype('float32')
del df # Clear the big vertical matrix from memory immediately

print("5. Aligning with Metadata...")
final_samples = final_df.index.intersection(meta_idx.index)
final_df = final_df.loc[final_samples].copy()

# Add target
final_df['target_t2d'] = meta_idx.loc[final_samples, 'sample_id'].str.contains('T2D', case=False).astype(int)

print("6. Saving to disk...")
final_df.to_parquet(output_final, engine='pyarrow')

print(f"SUCCESS! Final dataset saved with {len(final_df)} samples.")