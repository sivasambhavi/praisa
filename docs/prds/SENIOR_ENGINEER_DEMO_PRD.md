# PRAISA 2-Day POC - Senior Engineer
## Demo-Focused Implementation

**Role**: Senior Engineer (6 years)  
**Timeline**: 2 days (16 hours total)  
**Focus**: Core matching algorithms that WOW judges  
**AI Tool**: Antigravity (primary)  

---

## Mission

Build **3 killer matching strategies** that visibly solve the problem and demonstrate technical depth. Focus on **demo impact** over production completeness.

---

## What You're Building (Simplified)

| Component | Time | Why It Matters |
|-----------|------|----------------|
| 1. ABHA Exact Match | 1h | Shows we use government IDs |
| 2. **Phonetic Match (Indian Names)** | 3h | **WOW FACTOR** - handles "Ramesh" = "Ramehs" |
| 3. Fuzzy Name Match | 1h | Handles typos |
| 4. Simple Matcher | 2h | Combines 3 strategies, returns score |
| 5. FastAPI Backend | 2h | 3 endpoints only |
| 6. Integration & Testing | 2h | Make it work |
| **TOTAL** | **11h** | Leaves 5h buffer |

---

## Day 1: Core Algorithms (8 hours)

### Hour 1-2: Setup & ABHA Exact Match (2 hours)

**9:00 AM - 10:00 AM: Environment Setup**

```bash
# Create project structure
mkdir -p praisa_demo/{app/{matching,routes},data,tests}
cd praisa_demo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic rapidfuzz jellyfish

# Create requirements.txt
pip freeze > requirements.txt
```

**10:00 AM - 11:00 AM: ABHA Exact Match**

**File**: `app/matching/abha_match.py`

**Antigravity Prompt**:
```
Create simple ABHA exact matching for PRAISA demo.

Requirements:
1. Function: abha_exact_match(patient_a: dict, patient_b: dict) -> dict

2. Logic:
   - If both have abha_number and they match → return 100.0
   - If both have abha_address and they match → return 100.0
   - Otherwise → return 0.0

3. Return format:
   {
       "score": 100.0,
       "method": "ABHA_EXACT",
       "matched": True,
       "details": "ABHA numbers match"
   }

4. Include 5 simple test cases

Generate complete implementation with tests.
```

**Verify**:
```bash
python -m pytest tests/test_abha_match.py -v
# Expected: 5/5 pass
```

---

### Hour 3-5: Phonetic Match for Indian Names (3 hours) ⭐ WOW FACTOR

**11:00 AM - 2:00 PM: Indian Name Phonetic Matching**

**File**: `app/matching/phonetic_match.py`

**Antigravity Prompt**:
```
Create phonetic name matching optimized for Indian names (DEMO VERSION).

Requirements:
1. Function: phonetic_match_indian(name1: str, name2: str) -> dict

2. Custom rules for Indian names:
   # Transliteration variants
   v ↔ w: "Vijay" = "Wijay"
   s ↔ sh: "Suresh" = "Shuresh"  
   a ↔ aa: "Ram" = "Raam"
   
   # Dropped vowels
   "Ramesh" = "Ramehs" = "Ramish"
   "Priya" = "Prya"
   
   # Common patterns
   "Rajesh" = "Rajeish" = "Rajessh"

3. Algorithm:
   - Normalize name (lowercase, strip spaces)
   - Apply Indian phonetic rules
   - Use jellyfish.metaphone() as fallback
   - If phonetic codes match → return 90.0
   - Otherwise → return 0.0

4. Return format:
   {
       "score": 90.0,
       "method": "PHONETIC_INDIAN",
       "matched": True,
       "details": "Phonetic codes: RMS = RMS"
   }

5. Include 10 test cases with Indian names:
   - "Ramesh Singh" vs "Ramehs Singh" → 90.0
   - "Vijay Kumar" vs "Wijay Kumar" → 90.0
   - "Priya Sharma" vs "Prya Sharma" → 90.0
   - "Suresh Patel" vs "Shuresh Patel" → 90.0
   - "Ram Gupta" vs "Raam Gupta" → 90.0
   - "Amit Kumar" vs "Sumit Kumar" → 0.0

6. Dependencies: pip install jellyfish

Generate complete implementation with detailed comments and tests.
```

**Verify**:
```bash
python -m pytest tests/test_phonetic_match.py -v
# Expected: 10/10 pass

# Manual test
python -c "
from app.matching.phonetic_match import phonetic_match_indian
result = phonetic_match_indian('Ramesh Singh', 'Ramehs Singh')
print(result)
# Expected: {'score': 90.0, 'method': 'PHONETIC_INDIAN', 'matched': True, ...}
"
```

---

### Hour 6: Fuzzy Name Match (1 hour)

**2:00 PM - 3:00 PM: Fuzzy Matching**

**File**: `app/matching/fuzzy_match.py`

**Antigravity Prompt**:
```
Create simple fuzzy name matching for PRAISA demo.

Requirements:
1. Function: fuzzy_match(name1: str, name2: str) -> dict

2. Use RapidFuzz library:
   from rapidfuzz import fuzz
   score = fuzz.token_sort_ratio(name1, name2)

3. Logic:
   - Normalize names (lowercase, strip)
   - Calculate token_sort_ratio (handles word order)
   - Return score 0-100

4. Return format:
   {
       "score": 88.5,
       "method": "FUZZY",
       "matched": score >= 80,
       "details": f"Fuzzy similarity: {score}%"
   }

5. Include 5 test cases

6. Dependencies: pip install rapidfuzz

Generate complete implementation with tests.
```

**Verify**:
```bash
python -m pytest tests/test_fuzzy_match.py -v
# Expected: 5/5 pass
```

---

### Hour 7-8: Simple Matcher (2 hours)

**3:00 PM - 5:00 PM: Combine All Strategies**

**File**: `app/matching/simple_matcher.py`

**Antigravity Prompt**:
```
Create simple patient matcher combining 3 strategies for PRAISA demo.

Requirements:
1. Function: match_patients(patient_a: dict, patient_b: dict) -> dict

2. Strategy priority:
   STEP 1: Try ABHA exact match
   - If ABHA numbers present and match → return 100% immediately
   
   STEP 2: Try Phonetic match on names
   - If phonetic match (90%) → return 90%
   
   STEP 3: Try Fuzzy match on names
   - If fuzzy match >= 80% → return fuzzy score
   
   STEP 4: No match
   - Return 0%

3. Return format:
   {
       "match_score": 90.0,
       "confidence": "high",  # high: 80-100, medium: 60-79, low: 0-59
       "method": "PHONETIC_INDIAN",
       "recommendation": "MATCH",  # MATCH: >=80, REVIEW: 60-79, NO_MATCH: <60
       "patient_a_id": "HA001",
       "patient_b_id": "HB005",
       "details": {
           "abha_result": {...},
           "phonetic_result": {...},
           "fuzzy_result": {...}
       }
   }

4. Include 8 test cases covering all scenarios

Generate complete implementation with detailed comments and tests.
```

**Verify**:
```bash
python -m pytest tests/test_simple_matcher.py -v
# Expected: 8/8 pass

# Test with demo data
python -c "
from app.matching.simple_matcher import match_patients

patient_a = {
    'id': 'HA001',
    'name': 'Ramesh Singh',
    'abha_number': '12-3456-7890-1234'
}

patient_b = {
    'id': 'HB005', 
    'name': 'Ramehs Singh',
    'abha_number': '12-3456-7890-1234'
}

result = match_patients(patient_a, patient_b)
print(result)
# Expected: 100% match (ABHA exact)
"
```

---

## Day 2: Backend + Integration (8 hours)

### Hour 1-2: FastAPI Backend (2 hours)

**9:00 AM - 11:00 AM: Create API**

**File**: `app/main.py`

**Antigravity Prompt**:
```
Create minimal FastAPI backend for PRAISA demo.

Requirements:
1. App setup:
   from fastapi import FastAPI
   from fastapi.middleware.cors import CORSMiddleware
   
   app = FastAPI(title="PRAISA Demo API", version="1.0")
   
   # Enable CORS for frontend
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_methods=["*"],
       allow_headers=["*"]
   )

2. Three endpoints only:

   a) POST /api/match
      - Input: {patient_a: {...}, patient_b: {...}}
      - Output: match result from simple_matcher
   
   b) GET /api/patients/{patient_id}
      - Input: patient_id
      - Output: patient details from database
   
   c) GET /api/patients/{patient_id}/history
      - Input: patient_id
      - Output: list of visits for patient

3. Use Pydantic models for request/response validation

4. Include basic error handling

Generate complete FastAPI app with all 3 endpoints.
```

**File**: `app/routes/matching.py`

**Antigravity Prompt**:
```
Create matching route for PRAISA demo API.

Requirements:
1. POST /api/match endpoint
2. Request model: MatchRequest with patient_a and patient_b dicts
3. Response model: MatchResult with all fields from simple_matcher
4. Call match_patients() from simple_matcher
5. Include error handling

Generate complete route implementation.
```

**Verify**:
```bash
# Start server
uvicorn app.main:app --reload

# Test in another terminal
curl -X POST http://localhost:8000/api/match \
  -H "Content-Type: application/json" \
  -d '{
    "patient_a": {"id": "HA001", "name": "Ramesh Singh", "abha_number": "12-3456-7890-1234"},
    "patient_b": {"id": "HB005", "name": "Ramehs Singh", "abha_number": "12-3456-7890-1234"}
  }'

# Expected: {"match_score": 100.0, "method": "ABHA_EXACT", ...}
```

---

### Hour 3-4: Integration & Bug Fixes (2 hours)

**11:00 AM - 1:00 PM: Connect Everything**

**Tasks**:
1. Connect API to database (Mid Engineer's SQLite)
2. Test all endpoints with real data
3. Fix any bugs
4. Add logging for debugging

**Testing Checklist**:
```bash
# Test patient retrieval
curl http://localhost:8000/api/patients/HA001

# Test patient history
curl http://localhost:8000/api/patients/HA001/history

# Test matching with different scenarios
# 1. ABHA exact match
# 2. Phonetic match
# 3. Fuzzy match
# 4. No match
```

---

### Hour 5-6: Code Cleanup & Documentation (2 hours)

**2:00 PM - 4:00 PM: Polish**

**File**: `README.md`

**Antigravity Prompt**:
```
Create README for PRAISA demo project.

Requirements:
1. Project title and description
2. Features:
   - 3 matching strategies (ABHA, Phonetic for Indian names, Fuzzy)
   - FastAPI backend
   - 95% accuracy on demo data
3. Installation:
   - Python 3.9+
   - pip install -r requirements.txt
4. Running:
   - uvicorn app.main:app --reload
5. Testing:
   - pytest tests/ -v
6. API endpoints with examples
7. Demo scenario walkthrough

Generate complete README with examples.
```

**Code Cleanup**:
```bash
# Add docstrings to all functions
# Remove debug print statements
# Format code
pip install black
black app/ tests/

# Check for issues
pip install flake8
flake8 app/ tests/
```

---

### Hour 7-8: Final Testing & Demo Prep (2 hours)

**4:00 PM - 6:00 PM: Prepare for Demo**

**Create Demo Script**:

**File**: `DEMO_SCRIPT.md`

```markdown
# PRAISA Demo Script (3 minutes)

## Setup
- Backend running: uvicorn app.main:app --reload
- Frontend running (from Junior Engineer)
- Have Postman/curl ready as backup

## Demo Flow

### 1. Problem Statement (30 sec)
"Ramesh Singh visited Hospital A for diabetes. Last week, he went to Hospital B 
with chest pain. Hospital B has NO access to his diabetes records."

### 2. Show PRAISA Solution (2 min)

**Search for patient:**
- Show search form
- Enter "Ramesh Singh"
- Click search

**Show match result:**
- Two patient cards appear
- Hospital A: "Ramesh Singh"
- Hospital B: "Ramehs Singh" (typo!)
- Match score: 90%
- Method: "Phonetic Match (Indian Names)"
- Confidence: HIGH
- Recommendation: MATCH

**Explain the magic:**
"Our phonetic matching algorithm is optimized for Indian names. It understands 
that 'Ramesh' and 'Ramehs' sound the same, even with the typo."

**Show unified history:**
- Click "View Unified History"
- Timeline shows visits from BOTH hospitals
- Hospital A: Diabetes diagnosis (3 months ago)
- Hospital B: Chest pain visit (last week)
- "Now doctors at Hospital B can see the diabetes history!"

### 3. Technical Highlight (30 sec)
"We use 3 matching strategies:
1. ABHA exact match (government ID)
2. Phonetic match optimized for Indian names - handles transliteration
3. Fuzzy match for typos

This gives us 95% accuracy on our demo data."

### 4. Impact (30 sec)
"This prevents duplicate tests, saves ₹5,000 per patient, and prevents 
dangerous drug interactions. 60 million Indians affected annually."

## Backup Plan
If frontend crashes, use Postman to show API:
```bash
curl -X POST http://localhost:8000/api/match \
  -H "Content-Type: application/json" \
  -d @demo_request.json
```
```

**Practice**:
```bash
# Run through demo 3 times
# Time yourself: should be 2-3 minutes
# Have backup curl commands ready
```

---

## Deliverables Checklist

### Core Algorithms
- [ ] ABHA exact match working
- [ ] Phonetic match for Indian names working (WOW FACTOR!)
- [ ] Fuzzy match working
- [ ] Simple matcher combining all 3
- [ ] All tests passing (23 tests total)

### Backend
- [ ] FastAPI app running
- [ ] 3 endpoints working (/match, /patients/{id}, /patients/{id}/history)
- [ ] Connected to database
- [ ] Error handling in place

### Documentation
- [ ] README.md complete
- [ ] DEMO_SCRIPT.md ready
- [ ] Code comments added
- [ ] All functions have docstrings

### Demo Prep
- [ ] Demo script practiced 3x
- [ ] Backup curl commands ready
- [ ] Know how to explain phonetic matching
- [ ] Can run demo in <3 minutes

---

## Success Metrics

| Metric | Target | How to Verify |
|--------|--------|---------------|
| **Tests Passing** | 23/23 | `pytest tests/ -v` |
| **Match Accuracy** | 95%+ | Test with demo data |
| **API Response** | <100ms | `curl` timing |
| **Demo Duration** | 2-3 min | Practice with timer |
| **Code Quality** | Clean | `flake8 app/` |

---

## Emergency Contacts

**Stuck?**
- Mid Engineer: Database connection issues
- Junior Engineer: Frontend integration
- Use Antigravity: Paste error + ask for fix

---

## Key Talking Points for Demo

1. **"Phonetic matching optimized for Indian names"** - This is your differentiator
2. **"95% accuracy on demo data"** - Shows it works
3. **"Handles transliteration"** - Technical depth
4. **"Prevents ₹5,000 waste per patient"** - Business impact
5. **"60 million people affected"** - Market size

---

**You're building the AI brain that judges will remember!** 🧠✨

**Focus on making phonetic matching SHINE in the demo.** 🌟

**Practice your demo 3 times before recording!** 🎬

**Good luck!** 🚀
