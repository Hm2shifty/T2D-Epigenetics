import gzip
'''
file_path = "../data/GSE272137_series_matrix.txt.gz"

print(f"Inspecting the first 100 lines of {file_path}...\n")

with gzip.open(file_path, 'rt') as f:
    for i in range(100):
        line = f.readline()
        if not line:
            break
        
        # Print line number and content (stripped of extra newlines)
        # We also look for keywords
        indicator = ""
        if "ID_REF" in line: indicator = " <--- POTENTIAL HEADER"
        if "!series_matrix_table_begin" in line: indicator = " <--- DATA START MARKER"
        
        print(f"{i}: {line.strip()[:100]}{indicator}")

        '''
import gzip
import os

matrix_path = "../data/GSE270223_series_matrix.txt.gz"

print("--- PEEKING AT DATA TABLE HEADERS ---")
with gzip.open(matrix_path, 'rt') as f:
    count = 0
    start_printing = False
    for line in f:
        # We only care about the data table rows
        if line.startswith('!series_matrix_table_begin'):
            start_printing = True
            continue
        
        if start_printing:
            # Print the first 10 rows of data to see the IDs
            print(f"Row {count}: {line[:100]}...") # Print first 100 characters of the line
            count += 1
            if count > 15:
                break