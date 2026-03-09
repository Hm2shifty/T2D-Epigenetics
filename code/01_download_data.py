import GEOparse
import urllib.request
import os

'''
geo_id = "GSE272137"
data_folder = "../data"

# We add 'how="full"' to tell it to get the whole family of data
# And we use a try/except block just in case it fails again
try:
    gse = GEOparse.get_GEO(geo=geo_id, destdir=data_folder, how="full")
    print("Success! Title:", gse.metadata['title'][0])
except Exception as e:
    print("It failed again. Check your internet or delete the files in ./data and restart.")


url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE272nnn/GSE272137/suppl/GSE272137_processed_data_methylation.tsv.gz"
dest = "../data/GSE272137_processed_data_methylation.tsv.gz"

print("Starting download... this might take a few minutes.")
urllib.request.urlretrieve(url, dest)
print("Download complete! Now you can run the extraction script.")



# --- NEW TWIN DATASET (GSE38291) - ADDED ---
# This is the Series Matrix file which contains the processed Beta values for the twins
url_twins = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE38nnn/GSE38291/matrix/GSE38291_series_matrix.txt.gz"
dest_twins = "../data/GSE38291_series_matrix.txt.gz"

if not os.path.exists("../data"):
    os.makedirs("../data")

print("--- STARTING DOWNLOAD: Twin Dataset (GSE38291) ---")
try:
    urllib.request.urlretrieve(url_twins, dest_twins)
    print(f"Download complete! File saved to: {dest_twins}")
    print("\nNext Step: We need to extract this and check if your Top 50 sites are inside.")
except Exception as e:
    print(f"Download failed. Error: {e}")
    '''

import urllib.request
import os

# GSE114763 - Muscle Memory EPIC Dataset
url_mem = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE114nnn/GSE114763/matrix/GSE114763_series_matrix.txt.gz"
dest_mem = "../data/GSE114763_series_matrix.txt.gz"

if not os.path.exists("../data"):
    os.makedirs("../data")

print("--- DOWNLOADING EXERCISE VALIDATION DATA (EPIC) ---")
urllib.request.urlretrieve(url_mem, dest_mem)
print("Download complete!")