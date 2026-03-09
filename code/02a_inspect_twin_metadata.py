import gzip
import os

file_path = "../data/GSE38291_series_matrix.txt.gz"

if not os.path.exists(file_path):
    print("Error: File not found. Run the download script first.")
else:
    print(f"--- INSPECTING METADATA FOR: {file_path} ---\n")
    
    with gzip.open(file_path, 'rt') as f:
        # We only need to look at the first 100 lines to find the headers
        for i, line in enumerate(f):
            if i > 100: 
                break
            
            # These lines tell us what the columns actually mean
            if line.startswith("!Sample_title"):
                print(f"TITLES: {line[:200]}...") # e.g., Twin 13A muscle
            
            if line.startswith("!Sample_characteristics_ch1"):
                print(f"CHARACTERISTICS: {line[:200]}...") # e.g., disease state: T2D
                
            if line.startswith("!Sample_geo_accession"):
                print(f"GEO IDs: {line[:200]}...") # e.g., GSM938065
    
    print("\n--- END OF INSPECTION ---")