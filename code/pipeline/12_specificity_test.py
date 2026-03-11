import pandas as pd
import os
import pickle

# --- Paths (Running from 'code' folder) ---
DATA_DIR = os.path.join("..", "data")
BETA_FILE = os.path.join(DATA_DIR, "GSE114763_beta_values.csv")
GOLD_LIST_FILE = os.path.join(DATA_DIR, "top_50_diagnostic_panel.csv")
# Assuming your trained model is saved as a .pkl file
MODEL_FILE = os.path.join(DATA_DIR, "final_trained_model.pkl") 

def run_specificity_check():
    # 1. Load the 50 CpG names we care about
    print("📋 Loading the Gold List...")
    gold_list_df = pd.read_csv(GOLD_LIST_FILE)
    # Adjust 'CpG_ID' to whatever your column name is in the csv
    target_cpgs = gold_list_df.iloc[:, 0].tolist() 

    # 2. Extract only these sites from the massive Exercise file
    print("🔪 Slicing Exercise dataset (Targeting 50 sites)...")
    # We use 'chunksize' to stay memory-efficient
    filtered_chunks = []
    for chunk in pd.read_csv(BETA_FILE, chunksize=50000):
        subset = chunk[chunk['ID_REF'].isin(target_cpgs)]
        filtered_chunks.append(subset)
    
    exercise_subset = pd.concat(filtered_chunks)
    
    # 3. Format for the Model
    # Pivot so rows = samples, columns = CpG sites
    exercise_subset.set_index('ID_REF', inplace=True)
    test_data = exercise_subset.transpose()
    
    # Ensure column order matches the model's training order
    test_data = test_data[target_cpgs]
    
    print(f"✅ Data ready. Shape: {test_data.shape} (Samples x Sites)")

    # 4. Run the Algorithm
    print("🧠 Running T2D Model Predictions...")
    try:
        with open(MODEL_FILE, 'rb') as f:
            model = pickle.load(f)
        
        predictions = model.predict(test_data)
        probabilities = model.predict_proba(test_data)[:, 1]
        
        results = pd.DataFrame({
            'Sample_ID': test_data.index,
            'Predicted_as_T2D': predictions,
            'T2D_Probability': probabilities
        })
        
        print("\n--- SPECIFICITY RESULTS ---")
        print(results.head())
        
        # Calculate 'False Positive Rate'
        # Since these are all non-diabetics, any '1' (T2D) is a False Positive
        fp_count = results['Predicted_as_T2D'].sum()
        print(f"\nSummary: {fp_count} out of {len(results)} samples flagged as T2D.")
        if fp_count == 0:
            print("🏆 PERFECT SPECIFICITY: The model knows exercise isn't diabetes.")
        else:
            print(f"⚠️ Note: {fp_count} samples showed T2D-like noise.")

    except FileNotFoundError:
        print(f"❌ Error: Model file '{MODEL_FILE}' not found. Did you save your ML model yet?")

if __name__ == "__main__":
    run_specificity_check()