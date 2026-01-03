# PRAISA Mock Patient Data

## Files

1. **hospital_a_patients.csv** - 10 patients from Hospital A
2. **hospital_b_patients.csv** - 10 patients from Hospital B (includes 5 golden pairs)
3. **hospital_a_visits.csv** - 20 visits for Hospital A patients
4. **hospital_b_visits.csv** - 20 visits for Hospital B patients

## Golden Pairs (Same Patient in Both Hospitals)

| Hospital A | Hospital B | Variation Type | Match Method |
|------------|------------|----------------|--------------|
| HA001: Ramesh Singh | HB001: Ramehs Singh | Typo in name | Phonetic (90%) |
| HA002: Priya Sharma | HB002: Prya Sharma | Typo in name | Phonetic (90%) |
| HA003: Vijay Kumar | HB003: Wijay Kumar | v→w transliteration | Phonetic (90%) |
| HA004: Suresh Patel | HB004: Shuresh Patel | s→sh transliteration | Phonetic (90%) |
| HA005: Ram Gupta | HB005: Raam Gupta | a→aa variation | Phonetic (90%) |

## CSV Format

### Patients CSV
```csv
patient_id,name,dob,mobile,gender,abha_number,address,state
HA001,Ramesh Singh,1985-03-15,9876543210,M,12-3456-7890-1234,"123 MG Road Mumbai",Maharashtra
```

### Visits CSV
```csv
visit_id,patient_id,admission_date,visit_type,diagnosis,doctor_name
VA001,HA001,2025-10-15 09:00:00,OPD,Type 2 Diabetes Mellitus,Dr. Anjali Mehta
```

## How to Generate

**Mid Engineer**: Use ChatGPT with the prompt from `docs/MID_ENGINEER_DEMO_PRD.md` to generate all 4 CSV files.

## How to Load

```bash
# After generating CSVs, load into database:
python app/database/loader.py
```

## Verification

```bash
# Check files exist
ls data/*.csv

# Check line counts
wc -l data/*.csv
# Expected: 11, 11, 21, 21 (including headers)

# Verify golden pairs
head -6 data/hospital_a_patients.csv
head -6 data/hospital_b_patients.csv
```
