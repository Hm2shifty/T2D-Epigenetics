import pandas as pd
import gzip
import os

# 1. Define paths
file_path = "../data/GSE270223_series_matrix.txt.gz"
output_path = "../data/metadata_GSE270223.csv"

if not os.path.exists(file_path):
    print(f"Error: {file_path} not found.")
else:
    print(f"Directly parsing metadata from {file_path}...")
    
    metadata_dict = {}
    
    # We open the gzipped text file and look for the !Sample_ lines
    with gzip.open(file_path, 'rt') as f:
        for line in f:
            # Stop if we hit the data table
            if line.startswith('!series_matrix_table_begin'):
                break
            
            # Extract sample metadata lines
            if line.startswith('!Sample_'):
                parts = line.strip().split('\t')
                key = parts[0].replace('!Sample_', '')
                values = parts[1:]
                metadata_dict[key] = values

    # Convert to DataFrame
    df = pd.DataFrame(metadata_dict)

    # 2. Identify the columns we need
    # Map the typical GEO keys to our clean names
    # Note: 'characteristics_ch1' is often a list of columns in these matrices
    
    # Let's find all characteristics columns
    char_cols = [c for c in df.columns if 'characteristics_ch1' in c]
    
    # Create a mapping for our desired columns
    # We'll search through the characteristics columns to find T2D and Ethnicity
    final_data = pd.DataFrame()
    final_data['sample_id'] = df['title']
    final_data['geo_id'] = df['geo_accession']

    for col in char_cols:
        # Check the first row to see what this column contains
        first_val = str(df[col].iloc[0]).lower()
        if 't2d status' in first_val or 'diabetes' in first_val:
            final_data['group'] = df[col]
        elif 'ethnicity' in first_val:
            final_data['ethnicity'] = df[col]
        elif 'age' in first_val:
            final_data['age'] = df[col]
        elif 'sex' in first_val:
            final_data['sex'] = df[col]

    # 3. Clean the text (Strip the "prefix: " part)
    for col in final_data.columns:
        if col not in ['sample_id', 'geo_id']:
            final_data[col] = final_data[col].apply(
                lambda x: str(x).split(':')[-1].strip() if ':' in str(x) else str(x)
            )

    # 4. Final Binary Target for ML
    if 'group' in final_data.columns:
        final_data['target'] = final_data['group'].apply(
            lambda x: 1 if 't2d' in x.lower() or 'yes' in x.lower() or 'diabetes' in x.lower() else 0
        )

    # 5. Save
    final_data.to_csv(output_path, index=False)

    print("-" * 30)
    print("Success!")
    print(f"File saved to: {output_path}")
    print(f"Samples processed: {len(final_data)}")
    print("-" * 30)
    print(final_data.head())