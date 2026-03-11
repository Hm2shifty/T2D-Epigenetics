import os
import pandas as pd

# 1. Get current working directory
cwd = os.getcwd()
print(f"Current Directory: {cwd}")

# 2. Check if the 'data' folder exists in the project root
possible_data_path = os.path.join(os.path.dirname(cwd), "data")
print(f"Looking for data folder at: {possible_data_path}")

if os.path.exists(possible_data_path):
    print("Contents of data folder:")
    print(os.listdir(possible_data_path))
    
    # Try to load the file using the absolute path
    final_file = os.path.join(possible_data_path, "final_monocyte_dataset.parquet")
    if os.path.exists(final_file):
        print(f"\nSUCCESS: Found {final_file}")
        df = pd.read_parquet(final_file)
        print(f"Dataset Shape: {df.shape}")
        print(f"T2D Label Count:\n{df['target_t2d'].value_counts()}")
    else:
        print(f"\nFAILURE: 'final_monocyte_dataset.parquet' not found in {possible_data_path}")
else:
    print("\nFAILURE: Could not find 'data' folder at all.")