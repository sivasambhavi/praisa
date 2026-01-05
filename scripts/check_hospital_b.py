import sqlite3

conn = sqlite3.connect('praisa_demo.db')
cursor = conn.cursor()

print("\nPatients in Hospital B:")
print("=" * 60)
cursor.execute("SELECT patient_id, name FROM patients WHERE hospital_id='hospital_b' ORDER BY name")
for pid, name in cursor.fetchall():
    print(f"  {pid}: {name}")

print("\n\nSearching for 'Ramesh' in hospital_b:")
print("=" * 60)
cursor.execute("SELECT patient_id, name FROM patients WHERE hospital_id='hospital_b' AND name LIKE '%Ramesh%'")
results = cursor.fetchall()
if results:
    for pid, name in results:
        print(f"  {pid}: {name}")
else:
    print("  NO RESULTS - 'Ramesh' NOT in hospital_b!")

print("\n\nSearching for 'Ramehs' in hospital_b (typo variant):")
print("=" * 60)
cursor.execute("SELECT patient_id, name FROM patients WHERE hospital_id='hospital_b' AND name LIKE '%Ramehs%'")
results = cursor.fetchall()
if results:
    for pid, name in results:
        print(f"  {pid}: {name}")
else:
    print("  NO RESULTS")

conn.close()
