import sqlite3

conn = sqlite3.connect('praisa_demo.db')
cursor = conn.cursor()

print("=" * 70)
print("ROHIT PATIENTS IN DATABASE")
print("=" * 70)

cursor.execute("""
    SELECT patient_id, name, hospital_id, abha_number, dob, mobile
    FROM patients 
    WHERE name LIKE '%Rohit%'
    ORDER BY hospital_id, patient_id
""")

results = cursor.fetchall()
print(f"\nFound {len(results)} patients with 'Rohit' in name:\n")

for pid, name, hosp, abha, dob, mobile in results:
    print(f"{pid} | {name:20} | {hosp:12} | ABHA: {str(abha):15} | DOB: {dob} | Mobile: {mobile}")

print("\n" + "=" * 70)
print("CHECKING SPECIFIC PATIENTS FROM MATCH")
print("=" * 70)

# Check HD009 (Rohit Malhotra)
print("\n1. HD009 (Rohit Malhotra):")
cursor.execute("SELECT * FROM patients WHERE patient_id='HD009'")
row = cursor.fetchone()
if row:
    cols = [desc[0] for desc in cursor.description]
    for col, val in zip(cols, row):
        print(f"   {col}: {val}")
else:
    print("   NOT FOUND!")

# Check HA013 (Ramehs Malhotra)
print("\n2. HA013 (from match result - should be 'Ramehs Malhotra'):")
cursor.execute("SELECT * FROM patients WHERE patient_id='HA013'")
row = cursor.fetchone()
if row:
    cols = [desc[0] for desc in cursor.description]
    for col, val in zip(cols, row):
        print(f"   {col}: {val}")
else:
    print("   NOT FOUND!")

print("\n" + "=" * 70)
print("NAME SIMILARITY CHECK")
print("=" * 70)
print("\nComparing 'Rohit Malhotra' vs 'Ramehs Malhotra':")
print("  First names: Rohit vs Ramehs - COMPLETELY DIFFERENT!")
print("  Last names: Malhotra vs Malhotra - SAME")
print("\nThis should NOT be a 94.8% match!")

conn.close()
