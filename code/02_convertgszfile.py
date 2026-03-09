import GEOparse
import pandas as pd
import os


'''
# 1. Define paths
file_path = "../data/GSE272137_family.soft.gz"
output_path = "../data/metadata_final.csv"

# 2. Load the GSE object from the local file
if not os.path.exists(file_path):
    print(f"Error: {file_path} not found. Run the download script first!")
else:
    print(f"Loading and parsing {file_path}...")
    # Silence the mixed-type warning for a cleaner terminal
    gse = GEOparse.get_GEO(filepath=file_path, silent=True)

    # 3. Extract the phenotype (sample) data
    pheno_data = gse.phenotype_data

    # 4. Define the columns we want to keep
    keep_cols = [ 
        'title', 
        'geo_accession', 
        'characteristics_ch1.0.tissue', 
        'characteristics_ch1.1.Sex', 
        'characteristics_ch1.2.timepoint', 
        'characteristics_ch1.3.group'
    ]

    # 5. Create a clean copy with only our selected columns
    metadata_clean = pheno_data[keep_cols].copy() 

    # 6. Rename headers to short, easy names
    metadata_clean.columns = ['sample_id', 'geo_id', 'tissue', 'sex', 'timepoint', 'group']

    # 7. Clean the text inside the columns
    # We use .apply(lambda) because it is much more robust against mixed data types
    cols_to_strip = ['tissue', 'sex', 'timepoint', 'group']
    
    for col in cols_to_strip:
        # Step-by-step logic: Convert to string -> check for colon -> split and take right side -> strip whitespace
        metadata_clean[col] = metadata_clean[col].apply(
            lambda x: str(x).split(':')[-1].strip() if ':' in str(x) else str(x)
        )

    # 8. Save the final clinical table to CSV
    metadata_clean.to_csv(output_path, index=False)

    print("-" * 30)
    print("Transformation Complete!")
    print(f"File saved to: {output_path}")
    print("-" * 30)
    # Show a preview of the clean data
    print(metadata_clean.head())

'''

import pandas as pd
import gzip
import os

# 1. Setup Paths (Relative to the 'code' folder)
# '..' tells Python to go up one level to the project root, then into 'data'
DATA_DIR = os.path.join("..", "data")
RAW_FILE = os.path.join(DATA_DIR, "GSE114763_series_matrix.txt.gz")
OUT_BETA = os.path.join(DATA_DIR, "GSE114763_beta_values.csv")
OUT_META = os.path.join(DATA_DIR, "GSE114763_metadata.csv")

def process_geo_matrix(file_path):
    if not os.path.exists(file_path):
        print(f"Error: Could not find {file_path}")
        print("Make sure you are running this script from the 'code' directory.")
        return

    print(f"Processing {file_path}...")
    
    metadata_lines = []
    data_start_line = 0
    
    # Scan for the data table start and collect metadata labels
    with gzip.open(file_path, 'rt') as f:
        for i, line in enumerate(f):
            # We specifically want the title and characteristics for Exercise vs Control
            if line.startswith("!Sample_title") or line.startswith("!Sample_characteristics_ch1"):
                metadata_lines.append(line.strip().split('\t'))
            if "!series_matrix_table_begin" in line:
                data_start_line = i + 1
                break

    # --- PART 1: METHYLATION DATA ---
    print("Reading methylation matrix (this may take a minute)...")
    df = pd.read_csv(file_path, sep='\t', compression='gzip', skiprows=data_start_line)
    
    # Clean up GEO footer
    df = df[df.iloc[:, 0] != "!series_matrix_table_end"]
    df.rename(columns={df.columns[0]: 'ID_REF'}, inplace=True)
    
    print(f"Saving Beta values to {OUT_BETA}...")
    df.to_csv(OUT_BETA, index=False)
    
    # --- PART 2: METADATA EXTRACTION ---
    print("Extracting Exercise/Control labels...")
    meta_df = pd.DataFrame(metadata_lines).transpose()
    # Set headers and drop the descriptor row
    meta_df.columns = meta_df.iloc[0]
    meta_df = meta_df.drop(meta_df.index[0])
    
    meta_df.to_csv(OUT_META, index=False)
    print(f"✅ Success! Data and Metadata are ready in the /data folder.")

if __name__ == "__main__":
    process_geo_matrix(RAW_FILE)