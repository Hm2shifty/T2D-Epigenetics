import os
import shutil

# Using forward slashes prevents the \U unicode error
base_data = "C:/Users/hethm/Project/epigenetics_project/data"

# 1. First, define the Monocyte sub-structure
monocyte_dir = os.path.join(base_data, "GSE270223_monocytes")
subfolders = ["raw", "mapping", "processed"]
for sub in subfolders:
    os.makedirs(os.path.join(monocyte_dir, sub), exist_ok=True)

# 2. Define the Global Mapping
# Format: { "destination_folder": ["file1", "file2"] }
organize_plan = {
    "GSE270223_monocytes/raw": [
        "GSE270223_betas.txt.gz", "GSE270223_family.soft.gz", 
        "GSE270223_series_matrix.txt.gz", "metadata_GSE270223.csv"
    ],
    "GSE270223_monocytes/mapping": ["concrete_id_map.csv"],
    "GSE270223_monocytes/processed": ["GSE270223_full_matrix.parquet"],
    
    "GSE114763_twins": [
        "GSE114763_beta_values.csv", "GSE114763_metadata.csv", 
        "GSE114763_series_matrix.txt.gz", "beta_values_twins.csv", "metadata_twins.csv"
    ],
    "GSE272137_blood": [
        "GSE272137_family.soft.gz", "GSE272137_processed_data_methylation.tsv.gz", 
        "GSE272137_series_matrix.txt.gz"
    ],
    "GSE38291_old": ["GSE38291_series_matrix.txt.gz"],
    "archive_v1": [
        "analysis_a_full.pkl", "analysis_b_females.pkl", 
        "final_dataset_for_ml.pkl", "methylation_matrix.pkl", 
        "metadata_final.csv", "metadata.csv"
    ],
    "results": ["gold_list_biomarkers.csv", "top_50_diagnostic_panel.csv"]
}

print("--- STARTING GLOBAL CLEANUP ---")

for folder_rel, files in organize_plan.items():
    target_dir = os.path.join(base_data, folder_rel)
    os.makedirs(target_dir, exist_ok=True)
    
    for file_name in files:
        src = os.path.join(base_data, file_name)
        dst = os.path.join(target_dir, file_name)
        
        if os.path.exists(src):
            try:
                shutil.move(src, dst)
                print(f"MOVED: {file_name} -> {folder_rel}/")
            except Exception as e:
                print(f"FAILED: {file_name} | {e}")

print("\n--- CLEANUP COMPLETE ---")