import GEOparse
import pandas as pd
import os

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