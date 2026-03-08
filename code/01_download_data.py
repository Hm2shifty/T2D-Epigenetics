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
'''

url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE272nnn/GSE272137/suppl/GSE272137_processed_data_methylation.tsv.gz"
dest = "../data/GSE272137_processed_data_methylation.tsv.gz"

print("Starting download... this might take a few minutes.")
urllib.request.urlretrieve(url, dest)
print("Download complete! Now you can run the extraction script.")