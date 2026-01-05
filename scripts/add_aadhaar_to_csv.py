
import pandas as pd
import glob
import random
import os

def generate_aadhaar():
    """Generate a random 12-digit Aadhaar number string."""
    return ''.join([str(random.randint(0, 9)) for _ in range(12)])

def add_aadhaar_to_csvs():
    files = glob.glob("data/hospital_*_patients.csv")
    print(f"Found {len(files)} patient CSV files.")

    for fpath in files:
        print(f"Processing {fpath}...")
        try:
            df = pd.read_csv(fpath)
            
            # Check if column already exists
            if "aadhaar_number" in df.columns:
                print(f"  - Aadhaar column already exists in {fpath}. Skipping.")
                continue

            # Generate fake Aadhaar numbers
            # Use deterministic seed based on patient_id if possible for consistency, 
            # but random is fine for this demo as long as unique
            aadhaars = []
            for _, row in df.iterrows():
                # For demo consistency, let's keep it static if needed, 
                # but simple random 12 digits is okay for now.
                # However, for matched patients (same name across hospitals), 
                # we ideally want SAME Aadhaar if they are the same person.
                # Since we don't have cross-file matching logic here easily, 
                # we will just assign random ones. 
                # LIMITATION: Cross-hospital search for SAME person via Aadhaar 
                # won't work automatically unless we manually sync them.
                # BUT: For single patient search it works.
                aadhaars.append(generate_aadhaar())
            
            # Insert after abha_number
            if "abha_number" in df.columns:
                loc_idx = df.columns.get_loc("abha_number") + 1
                df.insert(loc_idx, "aadhaar_number", aadhaars)
            else:
                df["aadhaar_number"] = aadhaars
            
            # Save back
            df.to_csv(fpath, index=False)
            print(f"  - Added Aadhaar numbers to {fpath}")

        except Exception as e:
            print(f"Error processing {fpath}: {e}")

    # Special handling for our 'Golden Pairs' (Ramesh/Ramehs)
    # Ideally we edit them manually or ensure they match. 
    # For now, let's just make sure the column exists.

if __name__ == "__main__":
    add_aadhaar_to_csvs()
