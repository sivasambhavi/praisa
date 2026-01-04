
import sys
import os
import sqlite3
import random

# Add project root to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.matching.ml_matcher import MLPatientMatcher

def get_patients_from_db():
    conn = sqlite3.connect('praisa_demo.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return patients

def main():
    print("Training Active ML Model on current Database...")
    
    patients = get_patients_from_db()
    if not patients:
        print("Error: No patients found in DB.")
        return

    # Create maps by hospital
    hospitals = ['hospital_a', 'hospital_b', 'hospital_c', 'hospital_d', 'hospital_e']
    h_maps = {h: {p['patient_id']: p for p in patients if p['hospital_id'] == h} for h in hospitals}
    
    training_pairs = []
    training_labels = []
    
    # 1. Positive Examples (Cross-hospital pairs)
    print("Step 1: Extracting positive matches across all hospitals...")
    match_count = 0
    # Patient IDs are HAxxx, HBxxx, HCxxx, HDxxx, HExxx where xxx matches for the same person
    for i in range(1, 101): # Check up to 100
        suffix = f"{i:03d}"
        relevant_patients = []
        for h in hospitals:
            prefix = h.split('_')[1].upper()
            pid = f"H{prefix}{suffix}"
            if pid in h_maps[h]:
                relevant_patients.append(h_maps[h][pid])
        
        # Create pairs from all matching records
        for j in range(len(relevant_patients)):
            for k in range(j + 1, len(relevant_patients)):
                training_pairs.append((relevant_patients[j], relevant_patients[k]))
                training_labels.append(1)
                match_count += 1
            
    # 2. Negative Examples (Random cross-hospital)
    print("Step 2: Generating negative examples...")
    pids_by_h = {h: list(h_maps[h].keys()) for h in hospitals}
    
    neg_count = 0
    while neg_count < max(200, match_count * 1.5):
        h1, h2 = random.sample(hospitals, 2)
        if not pids_by_h[h1] or not pids_by_h[h2]: continue
        
        pa_id = random.choice(pids_by_h[h1])
        pb_id = random.choice(pids_by_h[h2])
        
        if pa_id[-3:] != pb_id[-3:]:
            training_pairs.append((h_maps[h1][pa_id], h_maps[h2][pb_id]))
            training_labels.append(0)
            neg_count += 1
            
    print(f"Dataset summary: {match_count} matches, {neg_count} non-matches.")
    
    # 3. Train
    matcher = MLPatientMatcher()
    matcher.train(training_pairs, training_labels)
    
    # 4. Save
    matcher.save_model()
    print("Success: Model trained and saved to model_weights.json")

if __name__ == "__main__":
    main()
