import pandas as pd
import sqlite3
import os

DB_PATH = "praisa_demo.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def load_patients_from_csv(csv_path, hospital_id):
    if not os.path.exists(csv_path):
        print(f"Error: File {csv_path} not found.")
        return 0

    conn = get_db_connection()
    cursor = conn.cursor()
    
    df = pd.read_csv(csv_path)
    count = 0
    
    print(f"Loading patients from {csv_path} for {hospital_id}...")
    
    for _, row in df.iterrows():
        try:
            # Check if patient already exists
            cursor.execute("SELECT id FROM patients WHERE patient_id = ?", (row['patient_id'],))
            if cursor.fetchone():
                print(f"Skipping duplicate patient {row['patient_id']}")
                continue
                
            cursor.execute(
                """
                INSERT INTO patients (patient_id, hospital_id, name, dob, mobile, gender, abha_number, address, state)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row['patient_id'],
                    hospital_id,
                    row['name'],
                    row['dob'],
                    row['mobile'],
                    row['gender'],
                    row['abha_number'],
                    row['address'],
                    row['state']
                )
            )
            count += 1
        except Exception as e:
            print(f"Error inserting patient {row['patient_id']}: {e}")
            
    conn.commit()
    conn.close()
    return count

def load_visits_from_csv(csv_path):
    if not os.path.exists(csv_path):
        print(f"Error: File {csv_path} not found.")
        return 0
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    df = pd.read_csv(csv_path)
    count = 0
    
    print(f"Loading visits from {csv_path}...")
    
    for _, row in df.iterrows():
        try:
            # Check if visit already exists
            cursor.execute("SELECT id FROM visits WHERE visit_id = ?", (row['visit_id'],))
            if cursor.fetchone():
                print(f"Skipping duplicate visit {row['visit_id']}")
                continue
                
            cursor.execute(
                """
                INSERT INTO visits (visit_id, patient_id, admission_date, visit_type, diagnosis, doctor_name)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    row['visit_id'],
                    row['patient_id'],
                    row['admission_date'],
                    row['visit_type'],
                    row['diagnosis'],
                    row['doctor_name']
                )
            )
            count += 1
        except Exception as e:
            print(f"Error inserting visit {row['visit_id']}: {e}")

    conn.commit()
    conn.close()
    return count

def init_db():
    if os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} already exists.")
        return

    print("Initializing database...")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        with open('app/database/schema.sql', 'r') as f:
            schema = f.read()
            cursor.executescript(schema)
            
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

def load_all_data():
    # Initialize DB if needed
    init_db()

    print("Starting data load...")
    
    p_a = load_patients_from_csv("data/hospital_a_patients.csv", "hospital_a")
    p_b = load_patients_from_csv("data/hospital_b_patients.csv", "hospital_b")
    
    v_a = load_visits_from_csv("data/hospital_a_visits.csv")
    v_b = load_visits_from_csv("data/hospital_b_visits.csv")
    
    print("\nData Load Summary:")
    print(f"Hospital A Patients: {p_a}")
    print(f"Hospital B Patients: {p_b}")
    print(f"Hospital A Visits: {v_a}")
    print(f"Hospital B Visits: {v_b}")
    print(f"Total Patients: {p_a + p_b}")
    print(f"Total Visits: {v_a + v_b}")

if __name__ == "__main__":
    load_all_data()
