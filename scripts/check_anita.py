"""Check Anita patients and test the match"""
import sqlite3

conn = sqlite3.connect('praisa_demo.db')
cursor = conn.cursor()

print("=" * 70)
print("ANITA PATIENTS")
print("=" * 70)

cursor.execute("""
    SELECT patient_id, name, hospital_id, abha_number, dob, gender
    FROM patients 
    WHERE name LIKE '%Anita%'
    ORDER BY name
""")

for row in cursor.fetchall():
    print(f"{row[0]} | {row[1]:20} | {row[2]:12} | ABHA: {str(row[3]):18} | DOB: {row[4]} | Gender: {row[5]}")

print("\n" + "=" * 70)
print("SPECIFIC PATIENTS FROM MATCH")
print("=" * 70)

# HA008 - Anita Desai
cursor.execute("SELECT * FROM patients WHERE patient_id='HA008'")
row = cursor.fetchone()
cols = [desc[0] for desc in cursor.description]
print("\nHA008 (Anita Desai):")
patient_a = dict(zip(cols, row))
for k, v in patient_a.items():
    print(f"  {k}: {v}")

# HD013 - Anita Verma
cursor.execute("SELECT * FROM patients WHERE patient_id='HD013'")
row = cursor.fetchone()
print("\nHD013 (Anita Verma):")
patient_b = dict(zip(cols, row))
for k, v in patient_b.items():
    print(f"  {k}: {v}")

print("\n" + "=" * 70)
print("COMPARISON")
print("=" * 70)
print(f"Name: {patient_a['name']} vs {patient_b['name']}")
print(f"  First: Anita vs Anita - SAME")
print(f"  Last: Desai vs Verma -DIFFERENT!")
print(f"ABHA: {patient_a['abha_number']} vs {patient_b['abha_number']} - DIFFERENT!")
print(f"DOB: {patient_a['dob']} vs {patient_b['dob']} - DIFFERENT!")
print(f"Gender: {patient_a['gender']} vs {patient_b['gender']}")

print("\nThis should be a NO_MATCH (score < 30%)!")

conn.close()
