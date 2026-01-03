# PRAISA 2-Day POC - Mid Engineer
## Demo-Focused Implementation

**Role**: Mid Engineer (5 years)  
**Timeline**: 2 days (16 hours total)  
**Focus**: Simple database + mock data that makes demo work  
**AI Tools**: ChatGPT (data generation), Antigravity (code)  

---

## Mission

Create **realistic mock data** and **simple database** that makes the demo compelling. Focus on **quality over quantity** - 10 perfect patient pairs beats 100 mediocre ones.

---

## What You're Building (Simplified)

| Component | Time | Why It Matters |
|-----------|------|----------------|
| 1. Mock Patient Data | 3h | Realistic demo scenario |
| 2. SQLite Database | 1h | Simple, no Docker |
| 3. Data Loader | 1h | Load CSV to DB |
| 4. Patient APIs | 3h | CRUD operations |
| 5. Integration & Testing | 2h | Make it work |
| **TOTAL** | **10h** | Leaves 6h buffer |

---

## Day 1: Data + Database (8 hours)

### Hour 1-3: Mock Patient Data (3 hours)

**9:00 AM - 12:00 PM: Generate Demo Data**

**Use ChatGPT with this prompt**:

```
Generate realistic mock patient data for PRAISA healthcare demo.

Requirements:
1. hospital_a_patients.csv (10 patients):
   Columns: patient_id, name, dob, mobile, gender, abha_number, address, state

   Include realistic Indian names:
   - HA001, Ramesh Singh, 1985-03-15, 9876543210, M, 12-3456-7890-1234, "123 MG Road Mumbai", Maharashtra
   - HA002, Priya Sharma, 1990-07-22, 9123456789, F, 12-3456-7890-2345, "456 Park Street Delhi", Delhi
   - HA003, Vijay Kumar, 1978-11-30, 9234567890, M, 12-3456-7890-3456, "789 Anna Salai Chennai", Tamil Nadu
   - ... 7 more patients

2. hospital_b_patients.csv (10 patients):
   - 5 "golden pairs" (same patients with variations):
     * HB001, Ramehs Singh, 1985-03-15, +91-9876543210, M, 12-3456-7890-1234 (typo in name)
     * HB002, Prya Sharma, 1990-07-22, 9123456789, F, 12-3456-7890-2345 (typo in name)
     * HB003, Wijay Kumar, 1978-11-30, 9234567890, M, 12-3456-7890-3456 (v→w transliteration)
     * ... 2 more golden pairs
   
   - 5 completely different patients:
     * HB006, Amit Patel, 1992-05-10, 9345678901, M, 12-3456-7890-6789, ...
     * ... 4 more different patients

3. hospital_a_visits.csv (20 visits):
   Columns: visit_id, patient_id, admission_date, visit_type, diagnosis, doctor_name

   Examples:
   - VA001, HA001, 2025-10-15 09:00:00, OPD, Type 2 Diabetes Mellitus, Dr. Anjali Mehta
   - VA002, HA001, 2025-12-20 14:30:00, OPD, Diabetes Follow-up, Dr. Anjali Mehta
   - VA003, HA002, 2025-11-05 10:15:00, Emergency, Severe Headache, Dr. Rajesh Kumar
   - ... 17 more visits (2-3 per patient)

4. hospital_b_visits.csv (20 visits):
   - Include visits for the golden pairs (HB001-HB005)
   - Include visits for different patients (HB006-HB010)
   - Recent dates (last 3 months)

Generate all 4 CSV files with realistic Indian healthcare data.
```

**Save ChatGPT output to**:
- `data/hospital_a_patients.csv`
- `data/hospital_b_patients.csv`
- `data/hospital_a_visits.csv`
- `data/hospital_b_visits.csv`

**Verify**:
```bash
# Check files exist
ls data/*.csv

# Check line counts
wc -l data/*.csv
# Expected: 11, 11, 21, 21 (including headers)

# Check golden pairs manually
head -6 data/hospital_a_patients.csv
head -6 data/hospital_b_patients.csv
# Verify HA001 "Ramesh Singh" matches HB001 "Ramehs Singh"
```

---

### Hour 4: SQLite Database Setup (1 hour)

**12:00 PM - 1:00 PM: Create Database Schema**

**File**: `app/database/schema.sql`

**Antigravity Prompt**:
```
Create simple SQLite database schema for PRAISA demo.

Requirements:
1. Table: patients
   - id INTEGER PRIMARY KEY AUTOINCREMENT
   - patient_id TEXT UNIQUE (e.g., "HA001")
   - hospital_id TEXT (e.g., "hospital_a")
   - name TEXT
   - dob DATE
   - mobile TEXT
   - gender TEXT
   - abha_number TEXT
   - address TEXT
   - state TEXT

2. Table: visits
   - id INTEGER PRIMARY KEY AUTOINCREMENT
   - visit_id TEXT UNIQUE (e.g., "VA001")
   - patient_id TEXT (foreign key to patients.patient_id)
   - admission_date DATETIME
   - visit_type TEXT (OPD/IPD/Emergency)
   - diagnosis TEXT
   - doctor_name TEXT

3. Indexes:
   - CREATE INDEX idx_patient_id ON patients(patient_id);
   - CREATE INDEX idx_abha ON patients(abha_number);
   - CREATE INDEX idx_visit_patient ON visits(patient_id);

Generate complete SQLite schema.
```

**Create Database**:
```bash
# Create database
sqlite3 praisa_demo.db < app/database/schema.sql

# Verify tables created
sqlite3 praisa_demo.db "SELECT name FROM sqlite_master WHERE type='table';"
# Expected: patients, visits
```

---

### Hour 5: Data Loader (1 hour)

**2:00 PM - 3:00 PM: Load CSV to Database**

**File**: `app/database/loader.py`

**Antigravity Prompt**:
```
Create CSV data loader for PRAISA demo SQLite database.

Requirements:
1. Function: load_patients_from_csv(csv_path: str, hospital_id: str)
   - Read CSV file with pandas
   - Insert into patients table
   - Add hospital_id column
   - Handle duplicates (skip if patient_id exists)
   - Return count of inserted records

2. Function: load_visits_from_csv(csv_path: str)
   - Read CSV file
   - Insert into visits table
   - Handle duplicates (skip if visit_id exists)
   - Return count of inserted records

3. Main function: load_all_data()
   - Load hospital_a_patients.csv (hospital_id="hospital_a")
   - Load hospital_b_patients.csv (hospital_id="hospital_b")
   - Load hospital_a_visits.csv
   - Load hospital_b_visits.csv
   - Print summary statistics

4. Dependencies: pip install pandas

5. Include error handling and logging

Generate complete data loader with main() function.
```

**Run Loader**:
```bash
# Install pandas
pip install pandas

# Load data
python app/database/loader.py

# Expected output:
# Loaded 10 patients from hospital_a
# Loaded 10 patients from hospital_b
# Loaded 20 visits from hospital_a
# Loaded 20 visits from hospital_b
# Total: 20 patients, 40 visits

# Verify in database
sqlite3 praisa_demo.db "SELECT COUNT(*) FROM patients;"
# Expected: 20

sqlite3 praisa_demo.db "SELECT COUNT(*) FROM visits;"
# Expected: 40
```

---

### Hour 6-8: Patient APIs (3 hours)

**3:00 PM - 6:00 PM: Create Database Access Layer**

**File**: `app/database/db.py`

**Antigravity Prompt**:
```
Create database access layer for PRAISA demo using SQLAlchemy.

Requirements:
1. Setup SQLAlchemy with SQLite:
   from sqlalchemy import create_engine
   from sqlalchemy.orm import sessionmaker
   
   engine = create_engine('sqlite:///praisa_demo.db')
   SessionLocal = sessionmaker(bind=engine)

2. Function: get_patient(patient_id: str) -> dict
   - Query patient by patient_id
   - Return as dictionary
   - Return None if not found

3. Function: search_patients(name: str = None, abha: str = None) -> list
   - Search by name (partial match) OR abha_number (exact)
   - Return list of patient dictionaries
   - Limit to 10 results

4. Function: get_patient_visits(patient_id: str) -> list
   - Get all visits for a patient
   - Order by admission_date DESC
   - Return list of visit dictionaries

5. Include proper session management (with context manager)

Generate complete database access layer.
```

**File**: `app/routes/patients.py`

**Antigravity Prompt**:
```
Create patient API routes for PRAISA demo.

Requirements:
1. GET /api/patients/{patient_id}
   - Return patient details
   - 404 if not found

2. GET /api/patients/search?name=...&abha=...
   - Search patients by name or ABHA
   - Return list of matching patients

3. GET /api/patients/{patient_id}/history
   - Return all visits for patient
   - Include patient details + visits list

4. Use FastAPI with Pydantic models for responses

5. Include error handling

Generate complete patient routes.
```

**Verify**:
```bash
# Start API (Senior Engineer's main.py should import these routes)
uvicorn app.main:app --reload

# Test endpoints
curl http://localhost:8000/api/patients/HA001
# Expected: Patient details for Ramesh Singh

curl "http://localhost:8000/api/patients/search?name=Ramesh"
# Expected: List with HA001 and HB001 (Ramesh and Ramehs)

curl http://localhost:8000/api/patients/HA001/history
# Expected: Patient + 2 visits (diabetes diagnosis + follow-up)
```

---

## Day 2: Integration + Testing (8 hours)

### Hour 1-2: Integration with Senior Engineer (2 hours)

**9:00 AM - 11:00 AM: Connect APIs to Matching**

**Tasks**:
1. Ensure database is accessible from Senior's matching code
2. Test matching with real database data
3. Fix any connection issues

**Integration Test**:
```python
# File: tests/test_integration.py

def test_match_golden_pair():
    """Test matching HA001 (Ramesh) with HB001 (Ramehs)"""
    from app.database.db import get_patient
    from app.matching.simple_matcher import match_patients
    
    patient_a = get_patient("HA001")  # Ramesh Singh
    patient_b = get_patient("HB001")  # Ramehs Singh
    
    result = match_patients(patient_a, patient_b)
    
    assert result['match_score'] >= 90.0
    assert result['method'] in ['ABHA_EXACT', 'PHONETIC_INDIAN']
    assert result['recommendation'] == 'MATCH'

# Run test
pytest tests/test_integration.py -v
```

---

### Hour 3-4: Create Demo Scenarios (2 hours)

**11:00 AM - 1:00 PM: Document Demo Data**

**File**: `DEMO_DATA.md`

```markdown
# PRAISA Demo Data Guide

## Golden Pairs (For Demo)

### Pair 1: Ramesh Singh (Phonetic Match)
- **Hospital A**: HA001, Ramesh Singh, 12-3456-7890-1234
- **Hospital B**: HB001, Ramehs Singh, 12-3456-7890-1234 (typo in name)
- **Match Method**: ABHA Exact (100%) OR Phonetic (90%)
- **Story**: Diabetes patient, visited Hospital B for chest pain

### Pair 2: Priya Sharma (Phonetic Match)
- **Hospital A**: HA002, Priya Sharma, 12-3456-7890-2345
- **Hospital B**: HB002, Prya Sharma, 12-3456-7890-2345 (typo)
- **Match Method**: ABHA Exact (100%) OR Phonetic (90%)
- **Story**: Headache patient, follow-up at Hospital B

### Pair 3: Vijay Kumar (Transliteration)
- **Hospital A**: HA003, Vijay Kumar, 12-3456-7890-3456
- **Hospital B**: HB003, Wijay Kumar, 12-3456-7890-3456 (v→w)
- **Match Method**: ABHA Exact (100%) OR Phonetic (90%)
- **Story**: Orthopedic patient

## Non-Matches (For Contrast)

### Different Patients
- **Hospital A**: HA004, Amit Kumar
- **Hospital B**: HB006, Amit Patel
- **Match Method**: Fuzzy (low score ~40%)
- **Result**: NO_MATCH

## Demo Scenario

Use **Pair 1 (Ramesh Singh)** for main demo:

1. Search for "Ramesh Singh" in Hospital A
2. Show match with "Ramehs Singh" in Hospital B
3. Highlight: 90% match using Phonetic matching
4. Show unified history:
   - Hospital A: Diabetes diagnosis (Oct 2025)
   - Hospital B: Chest pain visit (Dec 2025)
5. Impact: Doctors now know about diabetes!
```

---

### Hour 5-6: Testing & Bug Fixes (2 hours)

**2:00 PM - 4:00 PM: Comprehensive Testing**

**Test Checklist**:
```bash
# 1. Database tests
sqlite3 praisa_demo.db "SELECT * FROM patients WHERE patient_id='HA001';"
# Verify: Ramesh Singh data correct

# 2. API tests
curl http://localhost:8000/api/patients/HA001
curl http://localhost:8000/api/patients/HA001/history
curl "http://localhost:8000/api/patients/search?name=Ramesh"

# 3. Matching tests
curl -X POST http://localhost:8000/api/match \
  -H "Content-Type: application/json" \
  -d '{
    "patient_a": {"patient_id": "HA001"},
    "patient_b": {"patient_id": "HB001"}
  }'
# Expected: High match score

# 4. Integration tests
pytest tests/test_integration.py -v

# 5. Load all golden pairs and verify matches
python scripts/test_all_golden_pairs.py
```

**File**: `scripts/test_all_golden_pairs.py`

**Antigravity Prompt**:
```
Create script to test all golden pairs for PRAISA demo.

Requirements:
1. Load all 5 golden pairs from database
2. Run match_patients() on each pair
3. Print results in table format
4. Verify all match scores >= 80%
5. Flag any failures

Generate complete test script.
```

---

### Hour 7-8: Documentation & Handoff (2 hours)

**4:00 PM - 6:00 PM: Final Documentation**

**File**: `DATABASE_GUIDE.md`

```markdown
# PRAISA Demo Database Guide

## Quick Start

```bash
# Database location
praisa_demo.db

# View all patients
sqlite3 praisa_demo.db "SELECT patient_id, name, hospital_id FROM patients;"

# View golden pairs
sqlite3 praisa_demo.db "
SELECT a.patient_id, a.name, a.hospital_id, 
       b.patient_id, b.name, b.hospital_id
FROM patients a
JOIN patients b ON a.abha_number = b.abha_number
WHERE a.hospital_id = 'hospital_a' 
  AND b.hospital_id = 'hospital_b'
ORDER BY a.patient_id;
"
```

## Schema

### patients table
- patient_id: Unique ID (HA001, HB001, etc.)
- hospital_id: hospital_a or hospital_b
- name: Full name
- dob: Date of birth
- mobile: Phone number
- gender: M/F
- abha_number: Government health ID
- address: Full address
- state: Indian state

### visits table
- visit_id: Unique ID (VA001, VB001, etc.)
- patient_id: Links to patients
- admission_date: Visit date/time
- visit_type: OPD/IPD/Emergency
- diagnosis: Medical diagnosis
- doctor_name: Attending doctor

## Demo Data Summary

- **Total Patients**: 20 (10 per hospital)
- **Golden Pairs**: 5 (same patient in both hospitals)
- **Total Visits**: 40 (20 per hospital)
- **Match Rate**: 5/10 = 50% (realistic!)

## Troubleshooting

**Database locked?**
```bash
# Close all connections
pkill -f sqlite3
rm praisa_demo.db-journal  # if exists
```

**Need to reload data?**
```bash
rm praisa_demo.db
sqlite3 praisa_demo.db < app/database/schema.sql
python app/database/loader.py
```
```

---

## Deliverables Checklist

### Data
- [ ] 4 CSV files created (20 patients, 40 visits)
- [ ] 5 golden pairs with realistic variations
- [ ] Data loaded into SQLite database
- [ ] DEMO_DATA.md documented

### Database
- [ ] SQLite database created
- [ ] Schema with 2 tables + indexes
- [ ] 20 patients loaded
- [ ] 40 visits loaded
- [ ] Database accessible from APIs

### APIs
- [ ] GET /api/patients/{id} working
- [ ] GET /api/patients/search working
- [ ] GET /api/patients/{id}/history working
- [ ] All endpoints tested

### Integration
- [ ] Connected to Senior's matching code
- [ ] All golden pairs match correctly
- [ ] Integration tests passing
- [ ] Demo scenario tested

---

## Success Metrics

| Metric | Target | How to Verify |
|--------|--------|---------------|
| **Patients in DB** | 20 | `SELECT COUNT(*) FROM patients;` |
| **Golden Pairs** | 5 | Query with ABHA join |
| **Match Rate** | 5/5 = 100% | `test_all_golden_pairs.py` |
| **API Response** | <50ms | `curl` timing |
| **Data Quality** | Realistic | Manual review |

---

## Key Talking Points for Demo

1. **"Realistic demo data with 5 golden pairs"** - Shows it works
2. **"50% match rate is realistic"** - Not everyone visits both hospitals
3. **"Handles typos and transliteration"** - Ramesh vs Ramehs, Vijay vs Wijay
4. **"Simple SQLite for demo, PostgreSQL for production"** - Scalable

---

**You're building the data foundation that makes the demo believable!** 💾✨

**Focus on quality golden pairs that showcase phonetic matching.** 🎯

**Good luck!** 🚀
