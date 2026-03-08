import gzip

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