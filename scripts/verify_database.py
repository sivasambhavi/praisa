"""
Database Verification Script

Checks database integrity, patient counts, and search functionality.
"""

import sqlite3
import sys

# Connect to database
conn = sqlite3.connect('praisa_demo.db')
cursor = conn.cursor()

print("=" * 80)
print("PRAISA DATABASE VERIFICATION REPORT")
print("=" * 80)
print()

# 1. Check hospital counts
print("1. HOSPITAL PATIENT COUNTS")
print("-" * 80)
cursor.execute("""
    SELECT hospital_id, COUNT(*) as count 
    FROM patients 
    GROUP BY hospital_id 
    ORDER BY hospital_id
""")
results = cursor.fetchall()
total = 0
for hosp_id, count in results:
    print(f"   {hosp_id}: {count} patients")
    total += count
print(f"   TOTAL: {total} patients")
print()

# 2. Check specific patient
print("2. TEST PATIENT SEARCH (HA001)")
print("-" * 80)
cursor.execute("SELECT * FROM patients WHERE patient_id='HA001'")
row = cursor.fetchone()
if row:
    columns = [desc[0] for desc in cursor.description]
    print("   ✓ Found HA001:")
    for col, val in zip(columns, row):
        print(f"     {col}: {val}")
else:
    print("   ✗ HA001 NOT FOUND!")
print()

# 3. Search by name
print("3. NAME SEARCH TEST (Ramesh)")
print("-" * 80)
cursor.execute("SELECT patient_id, name, hospital_id FROM patients WHERE name LIKE '%Ramesh%'")
results = cursor.fetchall()
print(f"   Found {len(results)} patients with 'Ramesh' in name:")
for pid, name, hosp in results[:10]:
    print(f"     {pid} | {name} | {hosp}")
print()

# 4. Check golden pairs (ABHA duplicates)
print("4. GOLDEN PAIRS CHECK (Same ABHA across hospitals)")
print("-" * 80)
cursor.execute("""
    SELECT abha_number, COUNT(*) as count, GROUP_CONCAT(patient_id) as ids
    FROM patients
    WHERE abha_number IS NOT NULL AND abha_number != ''
    GROUP BY abha_number
    HAVING count > 1
    ORDER BY count DESC
    LIMIT 10
""")
results = cursor.fetchall()
print(f"   Found {len(results)} golden pairs:")
for abha, count, ids in results:
    print(f"     ABHA: {abha} → {count} patients ({ids})")
print()

# 5. Test hospital filter
print("5. HOSPITAL FILTER TEST")
print("-" * 80)
for hosp_id in ['hospital_a', 'hospital_b', 'hospital_c', 'hospital_d', 'hospital_e']:
    cursor.execute("SELECT COUNT(*) FROM patients WHERE hospital_id=?", (hosp_id,))
    count = cursor.fetchone()[0]
    status = "✓" if count > 0 else "✗"
    print(f"   {status} {hosp_id}: {count} patients")
print()

# 6. Check visit counts
print("6. VISIT COUNTS")
print("-" * 80)
cursor.execute("SELECT COUNT(*) FROM visits")
visit_count = cursor.fetchone()[0]
print(f"   Total visits: {visit_count}")
cursor.execute("""
    SELECT v.patient_id, COUNT(*) as visit_count
    FROM visits v
    GROUP BY v.patient_id
    ORDER BY visit_count DESC
    LIMIT 5
""")
results = cursor.fetchall()
print(f"   Top patients by visit count:")
for pid, count in results:
    print(f"     {pid}: {count} visits")
print()

# 7. Case sensitivity test
print("7. CASE SENSITIVITY TEST")
print("-" * 80)
test_names = ['Ramesh', 'RAMESH', 'ramesh', 'RaMeSh']
for test_name in test_names:
    cursor.execute("SELECT COUNT(*) FROM patients WHERE name LIKE ?", (f'%{test_name}%',))
    count = cursor.fetchone()[0]
    print(f"   '{test_name}': {count} results")
print()

# 8. Check for Hospital 'A' vs 'hospital_a'
print("8. HOSPITAL ID FORMAT CHECK")
print("-" * 80)
for short_id in ['A', 'B', 'C', 'D', 'E']:
    cursor.execute("SELECT COUNT(*) FROM patients WHERE hospital_id=?", (short_id,))
    count = cursor.fetchone()[0]
    print(f"   hospital_id='{short_id}': {count} patients")
print()

print("=" * 80)
print("END OF REPORT")
print("=" * 80)

conn.close()
