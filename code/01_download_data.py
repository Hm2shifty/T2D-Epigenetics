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

import urllib.request
import os

# GSE114763 - Muscle Memory EPIC Dataset
#url_mem = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE114nnn/GSE114763/matrix/GSE114763_series_matrix.txt.gz"
# dest_mem = "../data/GSE114763_series_matrix.txt.gz"

url_mem = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE270nnn/GSE270223/matrix/GSE270223_series_matrix.txt.gz"
dest_mem = "../data/GSE270223_series_matrix.txt.gz"


print("--- DOWNLOADING MONOCYTE VALIDATION DATA (GSE270223) ---")
urllib.request.urlretrieve(url_mem, dest_mem)
print("Download complete!")
    '''
import os
import urllib.request

# The actual verified filename for GSE270223 processed data
url_data = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE270nnn/GSE270223/suppl/GSE270223_Non-normalized_signal_intensities.txt.gz"
dest_data = "../data/GSE270223_data.txt.gz"

if not os.path.exists("../data"):
    os.makedirs("../data")

print("--- DOWNLOADING MONOCYTE SIGNAL DATA (This may take a while...) ---")
try:
    # This file is large, so we use a more robust download helper
    urllib.request.urlretrieve(url_data, dest_data)
    print(f"Download complete! File saved as {dest_data}")
except Exception as e:
    print(f"Error downloading: {e}")