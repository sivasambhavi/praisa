"""
Test phonetic matching without ABHA to showcase the algorithm
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.matching.phonetic_match import phonetic_match_indian

# Test cases for phonetic matching
test_cases = [
    ('Ramesh Singh', 'Ramehs Singh', 'Typo in name'),
    ('Priya Sharma', 'Prya Sharma', 'Dropped vowel'),
    ('Vijay Kumar', 'Wijay Kumar', 'v->w transliteration'),
    ('Amit Kumar', 'Amit Kumarr', 'Extra r'),
    ('Sunita Gupta', 'Suneeta Gupta', 'Vowel variation i->ee'),
    ('Suresh Patel', 'Shuresh Patel', 's->sh transliteration'),
    ('Ram Gupta', 'Raam Gupta', 'Vowel elongation a->aa'),
    ('Amit Kumar', 'Sumit Kumar', 'Different names - should NOT match'),
]

print("=" * 80)
print("PRAISA - Phonetic Matching for Indian Names (WOW FACTOR!)")
print("=" * 80)
print()

for name1, name2, description in test_cases:
    result = phonetic_match_indian(name1, name2)
    score = result['score']
    matched = result['matched']
    
    status = "[OK]" if matched else "[XX]"
    
    print(f"{status} {name1:20s} <-> {name2:20s}")
    print(f"   Score: {score:5.1f}% | {description}")
    print(f"   Details: {result['details']}")
    print()

print("=" * 80)
print("Phonetic Matching Test Complete!")
print("=" * 80)
