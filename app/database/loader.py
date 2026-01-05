"""
Database Loader for PRAISA

This module handles database initialization and data loading from CSV files.
Loads mock patient and visit data for the POC demo.

Features:
- Database schema initialization
- CSV data import with duplicate detection
- Error handling and logging
- Summary statistics

Author: Mid Engineer
Date: 2026-01-04
"""

import pandas as pd  # For CSV file reading and data manipulation
import sqlite3  # SQLite database operations
import os  # File system operations

# Database file path (relative to project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "praisa_demo.db")


def get_db_connection():
    """
    Create and return a SQLite database connection.

    Configures the connection to return rows as dictionaries
    instead of tuples for easier data access.

    Returns:
        sqlite3.Connection: Database connection with Row factory
    """
    conn = sqlite3.connect(DB_PATH)
    # Row factory allows accessing columns by name (dict-like)
    conn.row_factory = sqlite3.Row
    return conn


def load_patients_from_csv(csv_path, hospital_id):
    """
    Load patient data from CSV file into database.

    Reads patient records from CSV and inserts them into the patients table.
    Skips duplicates to allow safe re-running of the script.

    Args:
        csv_path: Path to CSV file (e.g., "data/hospital_a_patients.csv")
        hospital_id: Hospital identifier (e.g., "hospital_a" or "hospital_b")

    Returns:
        int: Number of patients successfully loaded

    CSV Format Expected:
        patient_id, name, dob, mobile, gender, abha_number, address, state
    """
    # Validate CSV file exists
    if not os.path.exists(csv_path):
        print(f"Error: File {csv_path} not found.")
        return 0

    # Establish database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Read CSV file into pandas DataFrame
    df = pd.read_csv(csv_path)
    count = 0  # Track number of patients loaded

    print(f"Loading patients from {csv_path} for {hospital_id}...")

    # Iterate through each row in the CSV
    for _, row in df.iterrows():
        try:
            # Check if patient already exists (prevent duplicates)
            # This allows safe re-running of the loader script
            cursor.execute(
                "SELECT id FROM patients WHERE patient_id = ?", (row["patient_id"],)
            )
            if cursor.fetchone():
                print(f"Skipping duplicate patient {row['patient_id']}")
                continue

            # Insert new patient record
            # Using parameterized query to prevent SQL injection
            cursor.execute(
                """
                INSERT INTO patients (
                    patient_id, hospital_id, name, dob, mobile,
                    gender, abha_number, aadhaar_number, address, state
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["patient_id"],  # Unique patient ID (e.g., "HA001")
                    hospital_id,  # Hospital identifier
                    row["name"],  # Patient full name
                    row["dob"],  # Date of birth (YYYY-MM-DD)
                    row["mobile"],  # Mobile number
                    row["gender"],  # Gender (M/F)
                    row["abha_number"],  # ABHA health ID
                    row.get("aadhaar_number", None), # Aadhaar number (handled if missing in old CSVs)
                    row["address"],  # Full address
                    row["state"],  # State name
                ),
            )
            count += 1  # Increment success counter

        except Exception as e:
            # Log error but continue processing other records
            print(f"Error inserting patient {row['patient_id']}: {e}")

    # Commit all changes to database
    conn.commit()
    conn.close()

    return count


def load_visits_from_csv(csv_path):
    """
    Load visit data from CSV file into database.

    Reads medical visit records and inserts them into the visits table.
    Each visit is linked to a patient via patient_id foreign key.

    Args:
        csv_path: Path to CSV file (e.g., "data/hospital_a_visits.csv")

    Returns:
        int: Number of visits successfully loaded

    CSV Format Expected:
        visit_id, patient_id, admission_date, visit_type, diagnosis, doctor_name
    """
    # Validate CSV file exists
    if not os.path.exists(csv_path):
        print(f"Error: File {csv_path} not found.")
        return 0

    # Establish database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Read CSV file into pandas DataFrame
    df = pd.read_csv(csv_path)
    count = 0  # Track number of visits loaded

    print(f"Loading visits from {csv_path}...")

    # Iterate through each row in the CSV
    for _, row in df.iterrows():
        try:
            # Check if visit already exists (prevent duplicates)
            cursor.execute(
                "SELECT id FROM visits WHERE visit_id = ?", (row["visit_id"],)
            )
            if cursor.fetchone():
                print(f"Skipping duplicate visit {row['visit_id']}")
                continue

            # Insert new visit record
            # Foreign key patient_id links to patients table
            cursor.execute(
                """
                INSERT INTO visits (
                    visit_id, patient_id, admission_date,
                    visit_type, diagnosis, doctor_name
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    row["visit_id"],  # Unique visit ID (e.g., "VA001")
                    row["patient_id"],  # Links to patient (foreign key)
                    row["admission_date"],  # Date and time of admission
                    row["visit_type"],  # Type: OPD, IPD, Emergency
                    row["diagnosis"],  # Medical diagnosis
                    row["doctor_name"],  # Attending doctor
                ),
            )
            count += 1  # Increment success counter

        except Exception as e:
            # Log error but continue processing other records
            print(f"Error inserting visit {row['visit_id']}: {e}")

    # Commit all changes to database
    conn.commit()
    conn.close()

    return count


def init_db():
    """
    Initialize the database schema.

    Creates the database file and executes the SQL schema to create tables.
    Skips initialization if database already exists to prevent data loss.

    Schema includes:
    - patients table (patient records)
    - visits table (medical visit records)
    - Indexes for performance
    - Foreign key constraints
    """
    # Check if database already exists
    if os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} already exists.")
        return

    print("Initializing database...")
    try:
        # Create new database connection
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Read and execute SQL schema file
        # Schema creates tables, indexes, and constraints
        with open(os.path.join(BASE_DIR, "app", "database", "schema.sql"), "r") as f:
            schema = f.read()
            cursor.executescript(schema)  # Execute all SQL statements

        # Commit changes and close connection
        conn.commit()
        conn.close()
        print("Database initialized successfully.")

    except Exception as e:
        print(f"Error initializing database: {e}")


def load_all_data():
    """
    Main function to load all data into database.

    Orchestrates the complete data loading process:
    1. Initialize database (if needed)
    2. Load patients from both hospitals
    3. Load visits from both hospitals
    4. Display summary statistics

    This function is idempotent - safe to run multiple times.
    Duplicates are automatically skipped.
    """
    # Step 1: Initialize database schema
    init_db()

    print("Starting data load...")

    # Step 2 & 3: Dynamically load all hospital data
    import glob
    
    # Load all patients
    patient_files = glob.glob(os.path.join(BASE_DIR, "data", "hospital_*_patients.csv"))
    total_patients = 0
    for p_file in patient_files:
        # Extract hospital_id from filename (e.g., data/hospital_a_patients.csv -> hospital_a)
        hospital_id = os.path.basename(p_file).replace("_patients.csv", "")
        count = load_patients_from_csv(p_file, hospital_id)
        total_patients += count
        print(f"Loaded {count} patients for {hospital_id}")

    # Load all visits
    visit_files = glob.glob(os.path.join(BASE_DIR, "data", "hospital_*_visits.csv"))
    total_visits = 0
    for v_file in visit_files:
        count = load_visits_from_csv(v_file)
        total_visits += count
        print(f"Loaded {count} visits from {os.path.basename(v_file)}")

    # Step 4: Display summary statistics
    print("\nData Load Summary:")
    print(f"Total Patients: {total_patients}")
    print(f"Total Visits: {total_visits}")


# Script entry point
# Allows running this file directly: python app/database/loader.py
if __name__ == "__main__":
    load_all_data()
