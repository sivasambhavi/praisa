-- Create patients table
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT UNIQUE NOT NULL,
    hospital_id TEXT NOT NULL,
    name TEXT NOT NULL,
    dob DATE,
    mobile TEXT,
    gender TEXT,
    abha_number TEXT,
    aadhaar_number TEXT,
    address TEXT,
    state TEXT
);

-- Create visits table
CREATE TABLE IF NOT EXISTS visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id TEXT UNIQUE NOT NULL,
    patient_id TEXT NOT NULL,
    admission_date DATETIME,
    visit_type TEXT,
    diagnosis TEXT,
    doctor_name TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
);

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_patients_patient_id ON patients(patient_id);
CREATE INDEX IF NOT EXISTS idx_patients_abha ON patients(abha_number);
CREATE INDEX IF NOT EXISTS idx_patients_aadhaar ON patients(aadhaar_number);
CREATE INDEX IF NOT EXISTS idx_visits_patient_id ON visits(patient_id);
