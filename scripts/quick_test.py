"""Quick database test"""
import sqlite3

conn = sqlite3.connect('praisa_demo.db')
cursor = conn.cursor()

# Test 1: Count by hospital
print("=" * 60)
print("HOSPITAL COUNTS:")
cursor.execute("SELECT hospital_id, COUNT(*) FROM patients GROUP BY hospital_id")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} patients")

# Test 2: Find Ramesh
print("\nRAMESH SEARCH:")
cursor.execute("SELECT patient_id, name, hospital_id FROM patients WHERE name LIKE '%Ramesh%' LIMIT 5")
for row in cursor.fetchall():
    print(f"  {row[0]} | {row[1]} | {row[2]}")

# Test 3: Test Hospital A filter
print("\nHOSPITAL_A FILTER TEST:")
cursor.execute("SELECT COUNT(*) FROM patients WHERE hospital_id='hospital_a'")
count = cursor.fetchone()[0]
print(f"  hospital_id='hospital_a': {count} patients")

conn.close()
print("\n" + "=" * 60)
