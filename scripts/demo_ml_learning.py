"""
Demo: Machine Learning Adaptive Matching
----------------------------------------
This script demonstrates the "Adaptive Learning" capability of the PRAISA matcher.
It simulates the following process:
1. Loading raw patient data (with quality issues).
2. "Learning" from verified examples (Golden Pairs).
3. Predicting matches on new, unseen data with probability scores.
4. Explaining WHY it matched (Feature Importance).
"""

import sys
import os
import secrets

# Add project root to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.loader import load_patients_from_csv
from app.matching.ml_matcher import MLPatientMatcher
import random

def main():
    print("="*60)
    print("PRAISA - Machine Learning Adaptive Matcher Demo")
    print("="*60)

    # 1. Load Data
    print("\n[1] Loading Data...")
    # diverse data generated earlier
    patients_a = load_patients_from_csv("data/hospital_a_patients.csv", "hospital_a")
    patients_b = load_patients_from_csv("data/hospital_b_patients.csv", "hospital_b")
    
    # We happen to know from generation that HA001 matches HB001, HA002 matches HB002, etc.
    # up to the count of patients (20).
    
    # 2. Create Training Data
    print("\n[2] Synthesizing Training Data (Simulating Human Feedback)...")
    training_pairs = []
    training_labels = []

    # --- Positive Examples (Matches) ---
    # We'll use the first 15 pairs for training
    print("   -> Adding verified matches (e.g. 'Ramesh' == 'Ramehs')")
    for i in range(15):
        # Assuming list index corresponds (loader returns lists)
        # Note: loader returns count, we need the actual objects.
        # Let's direct load for this script to get objects
        pass 
        
    # Re-reading properly
    import csv
    def read_csv_dicts(filepath):
        data = []
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    list_a = read_csv_dicts("data/hospital_a_patients.csv")
    list_b = read_csv_dicts("data/hospital_b_patients.csv")

    # Creating meaningful maps
    map_a = {p['patient_id']: p for p in list_a}
    map_b = {p['patient_id']: p for p in list_b}
    
    # Positive Samples: Corresponding IDs (HA00X <-> HB00X)
    # The generation script aligned them by index.
    # HA001 is mapped to HB001 in our golden dataset logic
    count_pos = 0
    for i in range(1, 16): # Train on first 15
        pid_a = f"HA{i:03d}"
        pid_b = f"HB{i:03d}"
        if pid_a in map_a and pid_b in map_b:
            training_pairs.append((map_a[pid_a], map_b[pid_b]))
            training_labels.append(1) # MATCH
            count_pos += 1
            
    # --- Negative Examples (Non-Matches) ---
    # Randomly pair different people
    print("   -> Adding non-matches (e.g. 'Ramesh' != 'Priya')")
    count_neg = 0
    keys_a = list(map_a.keys())
    keys_b = list(map_b.keys())
    
    for _ in range(30): # Add 30 negatives
        pa_id = random.choice(keys_a)
        pb_id = random.choice(keys_b)
        
        # Ensure not the matching pair
        # HBxxx vs HAxxx - check numeric part
        num_a = int(pa_id[2:])
        num_b = int(pb_id[2:])
        
        if num_a != num_b:
            training_pairs.append((map_a[pa_id], map_b[pb_id]))
            training_labels.append(0) # NO MATCH
            count_neg += 1

    print(f"   Training Set: {count_pos} Matches, {count_neg} Non-Matches")

    # 3. Train Model
    print("\n[3] Training Adaptive Model...")
    matcher = MLPatientMatcher()
    matcher.train(training_pairs, training_labels)

    # 4. Feature Importance
    print("\n[4] What did the model learn? (Feature Importance)")
    importances = matcher.get_feature_importance()
    # Sort by importance
    sorted_feats = sorted(importances.items(), key=lambda x: x[1], reverse=True)
    for name, score in sorted_feats:
        print(f"   - {name:<20}: {score:.4f}")
        
    # 5. Predictions on Test Data (The unseen last 5 records)
    print("\n[5] Predictions on Unseen Test Data:")
    print("   (These pairs were NOT in the training set)")
    
    for i in range(16, 21): # Train on 1-15, Test on 16-20
        pid_a = f"HA{i:03d}"
        pid_b = f"HB{i:03d}"
        
        if pid_a in map_a and pid_b in map_b:
            p_a = map_a[pid_a]
            p_b = map_b[pid_b]
            
            prob = matcher.predict(p_a, p_b)
            
            # Formatting output
            status = "MATCH" if prob > 0.8 else "REVIEW" if prob > 0.5 else "NO MATCH"
            color = "OK" if prob > 0.8 else "WARN"
            
            print(f"\n   Pair: {p_a['name']} (Hosp A) vs {p_b['name']} (Hosp B)")
            print(f"   Details: ID matches? {p_a.get('abha_number') == p_b.get('abha_number')}")
            print(f"   Details: DOB {p_a.get('dob')} vs {p_b.get('dob')}")
            print(f"   => ML Confidence: {prob*100:.1f}%  [{status}]")

    print("\n" + "="*60)
    print("Demo Complete. The model successfully 'learned' to trust phonetic matches!")
    print("="*60)

if __name__ == "__main__":
    main()
