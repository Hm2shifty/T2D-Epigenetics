import pandas as pd
import os
import urllib.request
import gzip

# 1. Configuration
url_betas = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE270nnn/GSE270223/suppl/GSE270223%5Fbetas%5Fprocessed%5FGEO.txt.gz"
raw_dest = "../data/GSE270223_betas.txt.gz"
output_parquet = "../data/GSE270223_full_matrix.parquet"

# Ensure data directory exists
if not os.path.exists("../data"):
    os.makedirs("../data")

# 2. Download Section
if not os.path.exists(raw_dest):
    print(f"--- DOWNLOADING PROCESSED BETA VALUES (2.2 GB) ---")
    
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    
    try:
        urllib.request.urlretrieve(url_betas, raw_dest)
        print(f"Download Successful: {raw_dest}")
    except Exception as e:
        print(f"Download Failed: {e}")
        exit()
else:
    print("File already exists. Skipping download...")

# 3. Conversion Section (Text.gz -> Parquet)
print("--- CONVERTING TO PARQUET FORMAT ---")
print("Reading in chunks to save RAM...")

try:
    chunk_size = 50000 
    # Use 'fastparquet' or 'pyarrow'. 
    # If you get an error here, run: pip install pyarrow fastparquet
    
    reader = pd.read_csv(raw_dest, sep='\t', compression='gzip', chunksize=chunk_size)

    for i, chunk in enumerate(reader):
        # Set the first column (ID_REF / CpG ID) as index
        chunk.set_index(chunk.columns[0], inplace=True)
        
        # On the first chunk, create the file. On others, append.
        if i == 0:
            chunk.to_parquet(output_parquet, engine='fastparquet', index=True)
        else:
            chunk.to_parquet(output_parquet, engine='fastparquet', append=True, index=True)
            
        print(f"Processed { (i+1)*chunk_size } rows...")

    print("-" * 30)
    print(f"CONVERSION COMPLETE!")
    print(f"Final File: {output_parquet}")
    print("-" * 30)

except Exception as e:
    print(f"An error occurred during conversion: {e}")