"""
Generate Bad Data Script
Generates mock patient and visit data for 5 hospitals with various data quality issues.
Scenarios: Repetitive names, misspellings, invalid numbers, extreme dates.
"""

import csv
import random
import os
from datetime import datetime, timedelta

# Configuration
HOSPITALS = ['hospital_a', 'hospital_b', 'hospital_c', 'hospital_d', 'hospital_e']
OUTPUT_DIR = "data"
NUM_PATIENTS_PER_HOSPITAL = 20

# Mock Data Sources
FIRST_NAMES = [
    "Ramesh", "Suresh", "Mahesh", "Rajesh", "Dinesh", "Sita", "Gita", "Rita", "Nita", "Anita",
    "Amit", "Sumit", "Rohit", "Mohit", "Sobhit", "Priya", "Riya", "Diya", "Siya", "Jiya"
]
LAST_NAMES = [
    "Singh", "Kumar", "Sharma", "Verma", "Gupta", "Malhotra", "Banerjee", "Patel", "Shah", "Yadav"
]
GENDERS = ["M", "F", "Other"]
STATES = ["Delhi", "Maharashtra", "Karnataka", "Tamil Nadu", "Uttar Pradesh", "Bihar", "West Bengal"]
VISIT_TYPES = ["OPD", "IPD", "Emergency"]
DIAGNOSES = ["Fever", "Cough", "Cold", "Headache", "Stomach Ache", "Fracture", "Dengue", "Malaria", "Typhoid", "Diabetes"]
DOCTORS = ["Dr. Smith", "Dr. Jones", "Dr. Strange", "Dr. House", "Dr. Who"]

def generate_mobile():
    """Generates valid and invalid mobile numbers."""
    scenario = random.random()
    if scenario < 0.7:  # 70% valid
        return f"{random.randint(6000000000, 9999999999)}"
    elif scenario < 0.8:  # 10% short (< 10 digits)
        return f"{random.randint(600000000, 999999999)}"
    elif scenario < 0.9:  # 10% starts with 0
        return f"0{random.randint(600000000, 999999999)}"
    else:  # 10% alphanumeric/garbage
        return "98765ABCDE"

def generate_abha():
    """Generates valid and invalid ABHA numbers."""
    scenario = random.random()
    if scenario < 0.8:  # 80% valid (14 digits)
        return f"{random.randint(10000000000000, 99999999999999)}"
    else:  # 20% invalid (wrong length)
        return f"{random.randint(100000, 999999)}"

def generate_dob():
    """Generates valid and extreme DOBS."""
    scenario = random.random()
    if scenario < 0.9:  # 90% normal age (1-90 years old)
        start_date = datetime.now() - timedelta(days=90*365)
        end_date = datetime.now() - timedelta(days=365)
    elif scenario < 0.95:  # 5% very old (> 120 years)
        start_date = datetime.now() - timedelta(days=150*365)
        end_date = datetime.now() - timedelta(days=120*365)
    else:  # 5% future date
        start_date = datetime.now() + timedelta(days=1)
        end_date = datetime.now() + timedelta(days=365)
    
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime("%Y-%m-%d")

def introduce_typo(name):
    """Introduces a simple typo in a name."""
    if len(name) < 3 or random.random() > 0.3: # Only 30% chance of typo
        return name
    
    idx = random.randint(0, len(name) - 2)
    # Swap two characters
    name_list = list(name)
    name_list[idx], name_list[idx+1] = name_list[idx+1], name_list[idx]
    return "".join(name_list)

def generate_data():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for hospital_id in HOSPITALS:
        patients_file = os.path.join(OUTPUT_DIR, f"{hospital_id}_patients.csv")
        visits_file = os.path.join(OUTPUT_DIR, f"{hospital_id}_visits.csv")
        
        print(f"Generating data for {hospital_id}...")
        
        patients = []
        visits = []
        
        hospital_prefix = hospital_id.split('_')[1].upper() # A, B, C...

        for i in range(1, NUM_PATIENTS_PER_HOSPITAL + 1):
            # 1. Basic Details
            patient_id = f"H{hospital_prefix}{i:03d}"
            
            # 2. Name Generation (Repetitive & Typos)
            fname = random.choice(FIRST_NAMES)
            lname = random.choice(LAST_NAMES)
            
            # Introduce typo in 2nd half of patients to simulate data entry errors
            if i > NUM_PATIENTS_PER_HOSPITAL / 2:
                fname = introduce_typo(fname)
            
            name = f"{fname} {lname}"
            
            # 3. Other fields
            dob = generate_dob()
            mobile = generate_mobile()
            gender = random.choice(GENDERS)
            abha = generate_abha()
            address = f"House No {random.randint(1, 999)}, Street {random.randint(1, 20)}"
            state = random.choice(STATES)
            
            patients.append([patient_id, name, dob, mobile, gender, abha, address, state])
            
            # 4. Generate Visits for this patient
            num_visits = random.randint(1, 5)
            for v in range(1, num_visits + 1):
                visit_id = f"V{hospital_prefix}{i:03d}-{v}"
                admission_date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
                visit_type = random.choice(VISIT_TYPES)
                diagnosis = random.choice(DIAGNOSES)
                doctor = random.choice(DOCTORS)
                
                visits.append([visit_id, patient_id, admission_date, visit_type, diagnosis, doctor])

        # Write Patients CSV
        with open(patients_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["patient_id", "name", "dob", "mobile", "gender", "abha_number", "address", "state"])
            writer.writerows(patients)
            
        # Write Visits CSV
        with open(visits_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["visit_id", "patient_id", "admission_date", "visit_type", "diagnosis", "doctor_name"])
            writer.writerows(visits)

if __name__ == "__main__":
    generate_data()
    print("Data generation complete.")
