import os
import GEOparse


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


'''
gse = GEOparse.get_GEO(filepath="../data/GSE272137_family.soft.gz", silent=True)
first_gsm = list(gse.gsms.keys())[0]
print(f"The columns for {first_gsm} are:")
print(gse.gsms[first_gsm].table.columns.tolist())
'''



'''
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
'''