
import pandas as pd
import glob
import os

def find_matches():
    # Load data
    df_a = pd.read_csv("data/hospital_a_patients.csv")
    df_b = pd.read_csv("data/hospital_b_patients.csv")
    
    print(f"Hospital A: {len(df_a)} records")
    print(f"Hospital B: {len(df_b)} records")
    
    # Normalize columns for comparison
    common_cols = ['name', 'mobile', 'abha_number', 'aadhaar_number']
    
    # Ensure ID columns are strings to avoid int/object mismatches
    for col in ['mobile', 'abha_number', 'aadhaar_number']:
        df_a[col] = df_a[col].astype(str)
        df_b[col] = df_b[col].astype(str)
    
    # Find exact matches across both
    # We want to find a row in A that matches a row in B on significant fields
    
    print("\n--- EXACT MATCHES (Name + Mobile) ---")
    merged = pd.merge(df_a, df_b, on=['name', 'mobile'], suffixes=('_A', '_B'))
    if not merged.empty:
        print(merged[['patient_id_A', 'patient_id_B', 'name', 'mobile']])
    else:
        print("No exact Name+Mobile matches found.")

    print("\n--- ABHA MATCHES ---")
    merged_abha = pd.merge(df_a, df_b, on=['abha_number'], suffixes=('_A', '_B'))
    if not merged_abha.empty:
        print(merged_abha[['patient_id_A', 'patient_id_B', 'name_A', 'name_B', 'abha_number']])
    else:
        print("No ABHA matches found.")

    print("\n--- AADHAAR MATCHES ---")
    merged_aadhaar = pd.merge(df_a, df_b, on=['aadhaar_number'], suffixes=('_A', '_B'))
    if not merged_aadhaar.empty:
        print(merged_aadhaar[['patient_id_A', 'patient_id_B', 'name_A', 'name_B', 'aadhaar_number']])
    else:
        print("No Aadhaar matches found.")

    print("\n--- NAME ONLY MATCHES ---")
    merged_name = pd.merge(df_a, df_b, on=['name'], suffixes=('_A', '_B'))
    if not merged_name.empty:
        print(merged_name[['patient_id_A', 'patient_id_B', 'name', 'mobile_A', 'mobile_B']])
    else:
        print("No Name matches found.")

if __name__ == "__main__":
    find_matches()
