# PRAISA 2-Day POC - Execution Guide
## Step-by-Step Implementation Sequence

**Timeline**: 2 days (16 hours total)  
**Team**: 3 engineers working in parallel with dependencies  
**Goal**: Working demo by end of Day 2  

---

## Quick Overview

```
Day 1 Morning:  Mid → Senior → Junior (sequential)
Day 1 Afternoon: All parallel
Day 2 Morning:  Integration (all together)
Day 2 Afternoon: Demo prep (Junior leads)
```

---

## Day 1: Build Core Features

### 🔴 CRITICAL PATH: Start Here

**Time**: 9:00 AM - 9:30 AM (30 min)  
**Who**: **ALL ENGINEERS TOGETHER**  
**What**: Team Setup & Alignment

**Tasks**:
```bash
# 1. Create project structure (Mid Engineer leads)
mkdir -p praisa_demo/{app/{matching,routes,database},data,tests,frontend}
cd praisa_demo

# 2. Initialize git
git init
git remote add origin <your-repo-url>

# 3. Create virtual environment (Senior Engineer)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 4. Install base dependencies
pip install fastapi uvicorn sqlalchemy pydantic

# 5. Create requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Initial setup"

# 6. Assign tasks
- Mid: Start on mock data generation
- Senior: Start on environment setup
- Junior: Start on UI wireframes (paper/Figma)
```

**Deliverable**: Project structure ready, everyone knows their tasks

---

### Phase 1: Foundation (9:30 AM - 12:00 PM) - 2.5 hours

#### Step 1.1: Mid Engineer - Generate Mock Data (9:30 AM - 12:00 PM)

**Priority**: 🔴 **CRITICAL** - Everyone needs this data!

**Tasks**:
1. Use ChatGPT to generate 4 CSV files (see Mid Engineer PRD)
2. Save to `data/` folder
3. Verify 5 golden pairs exist
4. **Commit to git immediately**

**Commands**:
```bash
# After generating CSVs
git add data/*.csv
git commit -m "Add mock patient data with 5 golden pairs"
git push

# Notify team in chat
"✅ Mock data ready! 5 golden pairs: HA001↔HB001, HA002↔HB002, etc."
```

**Deliverable**: 4 CSV files committed to git

**⏸️ BLOCKER**: Senior and Junior are blocked until this is done!

---

#### Step 1.2: Senior Engineer - Setup + ABHA Match (9:30 AM - 11:00 AM)

**Wait for**: Mid Engineer's CSV files committed

**Tasks**:
1. Install additional dependencies
2. Create ABHA exact match function
3. Write tests

**Commands**:
```bash
# Pull Mid's data
git pull

# Install dependencies
pip install rapidfuzz jellyfish pytest
pip freeze > requirements.txt

# Create ABHA match
# (Use Antigravity prompt from Senior PRD)

# Test
pytest tests/test_abha_match.py -v

# Commit
git add app/matching/abha_match.py tests/test_abha_match.py
git commit -m "Add ABHA exact matching"
git push
```

**Deliverable**: ABHA matching working, tests passing

---

#### Step 1.3: Mid Engineer - Database Setup (12:00 PM - 1:00 PM)

**Dependency**: Mock data already created

**Tasks**:
1. Create SQLite schema
2. Create database
3. Load CSV data

**Commands**:
```bash
# Create schema
# (Use Antigravity prompt from Mid PRD)

# Create database
sqlite3 praisa_demo.db < app/database/schema.sql

# Install pandas
pip install pandas
pip freeze > requirements.txt

# Load data
python app/database/loader.py

# Verify
sqlite3 praisa_demo.db "SELECT COUNT(*) FROM patients;"
# Expected: 20

# Commit
git add app/database/*.py app/database/schema.sql praisa_demo.db
git commit -m "Add SQLite database with patient data"
git push

# Notify team
"✅ Database ready! 20 patients, 40 visits loaded"
```

**Deliverable**: Database file committed, data loaded

**⏸️ BLOCKER**: Senior needs this for API testing!

---

### Phase 2: Core Algorithms (1:00 PM - 5:00 PM) - 4 hours

#### Step 2.1: Senior Engineer - Phonetic Matching (11:00 AM - 2:00 PM) ⭐ WOW FACTOR

**Dependency**: None (can work in parallel)

**Tasks**:
1. Create phonetic matching for Indian names
2. Write 10 test cases
3. Test with golden pairs

**Commands**:
```bash
# Create phonetic match
# (Use Antigravity prompt from Senior PRD)

# Test
pytest tests/test_phonetic_match.py -v

# Manual test with real data
python -c "
from app.matching.phonetic_match import phonetic_match_indian
result = phonetic_match_indian('Ramesh Singh', 'Ramehs Singh')
print(result)
"

# Commit
git add app/matching/phonetic_match.py tests/test_phonetic_match.py
git commit -m "Add phonetic matching for Indian names"
git push

# Notify team
"✅ Phonetic matching ready! Handles Ramesh↔Ramehs, Vijay↔Wijay"
```

**Deliverable**: Phonetic matching working - THIS IS YOUR DIFFERENTIATOR!

---

#### Step 2.2: Senior Engineer - Fuzzy Match + Simple Matcher (2:00 PM - 5:00 PM)

**Dependency**: ABHA and Phonetic matches done

**Tasks**:
1. Create fuzzy matching
2. Create simple matcher combining all 3
3. Test with database data

**Commands**:
```bash
# Pull latest (Mid's database)
git pull

# Create fuzzy match
# (Use Antigravity prompt from Senior PRD)

# Create simple matcher
# (Use Antigravity prompt from Senior PRD)

# Test
pytest tests/test_fuzzy_match.py -v
pytest tests/test_simple_matcher.py -v

# Integration test with real data
python -c "
from app.database.db import get_patient
from app.matching.simple_matcher import match_patients

patient_a = get_patient('HA001')
patient_b = get_patient('HB001')
result = match_patients(patient_a, patient_b)
print(f'Match score: {result[\"match_score\"]}%')
"

# Commit
git add app/matching/*.py tests/test_*.py
git commit -m "Add fuzzy matching and simple matcher"
git push

# Notify team
"✅ All 3 matching strategies working! 90% score on Ramesh↔Ramehs"
```

**Deliverable**: Complete matching engine ready

---

#### Step 2.3: Mid Engineer - Patient APIs (1:00 PM - 4:00 PM)

**Wait for**: Database setup complete

**Tasks**:
1. Create database access layer
2. Create patient API routes
3. Test endpoints

**Commands**:
```bash
# Create database access layer
# (Use Antigravity prompt from Mid PRD)

# Create patient routes
# (Use Antigravity prompt from Mid PRD)

# Test
pytest tests/test_db.py -v

# Commit
git add app/database/db.py app/routes/patients.py
git commit -m "Add patient APIs"
git push

# Notify team
"✅ Patient APIs ready! GET /api/patients/{id} working"
```

**Deliverable**: Patient APIs working

---

#### Step 2.4: Junior Engineer - UI Components (1:00 PM - 5:00 PM)

**Dependency**: None initially (can work on static UI)

**Tasks**:
1. Create search form
2. Create match results display
3. Create unified history view

**Commands**:
```bash
# Create React app with Vite
cd frontend
npm create vite@latest . -- --template react
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Create components using Bolt.new
# (Use prompts from Junior PRD)

# Test locally
npm run dev
# Open http://localhost:5173

# Commit
git add frontend/
git commit -m "Add UI components"
git push

# Notify team
"✅ UI components ready! Search, match results, history views done"
```

**Deliverable**: UI components built (not connected yet)

---

### 🔴 END OF DAY 1 CHECKPOINT (5:00 PM)

**Status Check** (15 min team meeting):

```
✅ Mid Engineer:
   - Mock data: 20 patients, 5 golden pairs
   - Database: SQLite with all data loaded
   - APIs: Patient CRUD working

✅ Senior Engineer:
   - ABHA exact match: Working
   - Phonetic match: Working (WOW FACTOR!)
   - Fuzzy match: Working
   - Simple matcher: Combining all 3

✅ Junior Engineer:
   - Search UI: Built
   - Match results: Built
   - History view: Built
   - (Not connected to backend yet)

❌ Not Done Yet:
   - FastAPI backend integration
   - UI ↔ Backend connection
   - Demo video
   - Pitch deck
```

**Evening Homework** (Optional, 1-2 hours):
- Senior: Start FastAPI backend
- Mid: Review integration points
- Junior: Start pitch deck content

---

## Day 2: Integration + Demo

### Phase 3: Integration (9:00 AM - 1:00 PM) - 4 hours

#### Step 3.1: Senior Engineer - FastAPI Backend (9:00 AM - 11:00 AM)

**Dependency**: All matching code + patient APIs done

**Tasks**:
1. Create main FastAPI app
2. Add matching route
3. Connect to database

**Commands**:
```bash
# Pull latest
git pull

# Create FastAPI app
# (Use Antigravity prompt from Senior PRD)

# Start server
uvicorn app.main:app --reload

# Test in another terminal
curl http://localhost:8000/api/patients/HA001
curl -X POST http://localhost:8000/api/match \
  -H "Content-Type: application/json" \
  -d @test_match_request.json

# Commit
git add app/main.py app/routes/matching.py
git commit -m "Add FastAPI backend with matching endpoint"
git push

# Notify team
"✅ Backend running on http://localhost:8000"
"✅ Swagger docs: http://localhost:8000/docs"
```

**Deliverable**: Backend API running

---

#### Step 3.2: ALL ENGINEERS - Integration Testing (11:00 AM - 1:00 PM)

**Who**: Everyone together

**Tasks**:
1. Connect frontend to backend
2. Test full user flow
3. Fix bugs

**Test Scenario**:
```
1. Mid Engineer: Ensure backend running
   uvicorn app.main:app --reload

2. Junior Engineer: Start frontend
   cd frontend
   npm run dev

3. Senior Engineer: Monitor logs, fix issues

4. ALL: Test together
   - Search for "Ramesh" → Should show HA001
   - Click "Match with Hospital B"
   - Select HB001 (Ramehs)
   - See match result: 90% score
   - Click "View Unified History"
   - See 3 visits (2 from A, 1 from B)

5. Fix any bugs immediately

6. Test all 5 golden pairs

7. Commit all fixes
   git add .
   git commit -m "Integration complete - all features working"
   git push
```

**Deliverable**: Full demo flow working end-to-end

---

### 🔴 LUNCH BREAK (1:00 PM - 2:00 PM)

**Relax! You've built the core product!** 🎉

---

### Phase 4: Demo Preparation (2:00 PM - 6:00 PM) - 4 hours

#### Step 4.1: Junior Engineer - Demo Video (2:00 PM - 5:00 PM) ⭐ CRITICAL

**Dependency**: Full demo working

**Tasks**:
1. Practice demo script (30 min)
2. Practice run #1 (30 min)
3. Practice run #2 (30 min)
4. FINAL RECORDING (30 min)
5. Review & upload (1 hour)

**Commands**:
```bash
# Ensure backend running
cd praisa_demo
uvicorn app.main:app --reload

# Ensure frontend running
cd frontend
npm run dev

# Open Loom
# Follow demo script from Junior PRD
# Record 3-minute demo

# Upload to:
- YouTube (unlisted)
- Loom
- Google Drive

# Test all links

# Share with team
"✅ Demo video uploaded!"
"YouTube: https://youtu.be/..."
"Loom: https://loom.com/..."
```

**Deliverable**: 3-minute demo video uploaded

---

#### Step 4.2: Junior Engineer - Pitch Deck (2:00 PM - 5:00 PM)

**Parallel with demo video** (work on deck while waiting for recording)

**Tasks**:
1. Create 10 slides in Canva
2. Add screenshots from demo
3. Add demo video link
4. Export as PDF

**Checklist**:
```
Slides:
[ ] 1. Title
[ ] 2. Problem
[ ] 3. Solution
[ ] 4. How It Works
[ ] 5. Key Innovation (Phonetic Matching)
[ ] 6. Market Opportunity
[ ] 7. Business Model
[ ] 8. Competitive Advantage
[ ] 9. 6-Month Roadmap
[ ] 10. Ask

Screenshots needed:
[ ] Match results (90% score)
[ ] Unified history
[ ] Phonetic match explanation

Export:
[ ] PDF < 10MB
[ ] PowerPoint (backup)
```

**Deliverable**: Pitch deck PDF ready

---

#### Step 4.3: Senior + Mid Engineers - Code Cleanup (2:00 PM - 4:00 PM)

**Tasks**:
1. Add docstrings
2. Remove debug prints
3. Format code
4. Update README

**Commands**:
```bash
# Format code
pip install black
black app/ tests/

# Remove debug prints
grep -r "print(" app/ | wc -l  # Should be 0

# Update README
# (Use Antigravity prompt from Senior PRD)

# Final commit
git add .
git commit -m "Code cleanup and documentation"
git push
```

**Deliverable**: Clean, documented code

---

### Phase 5: Final Review (5:00 PM - 6:00 PM) - 1 hour

#### Step 5.1: ALL ENGINEERS - Final Testing

**Checklist**:
```bash
# 1. Backend
[ ] uvicorn app.main:app --reload
[ ] http://localhost:8000/docs (Swagger UI loads)
[ ] All endpoints working

# 2. Frontend
[ ] npm run dev
[ ] http://localhost:5173 (UI loads)
[ ] Search works
[ ] Match works
[ ] History works

# 3. Demo video
[ ] YouTube link works
[ ] Loom link works
[ ] Duration: 2:30-3:00
[ ] Audio clear
[ ] Shows all features

# 4. Pitch deck
[ ] PDF < 10MB
[ ] All 10 slides
[ ] No typos
[ ] Screenshots included
[ ] Demo video link works

# 5. GitHub
[ ] All code committed
[ ] README.md complete
[ ] requirements.txt up to date
[ ] .gitignore present
```

---

### 🔴 FINAL SUBMISSION (6:00 PM)

**Who**: Junior Engineer (with team review)

**Tasks**:
1. Prepare submission text
2. Upload to competition platform
3. Screenshot confirmation

**Submission Checklist**:
```
[ ] Team name
[ ] Project title: PRAISA - AI-Powered Healthcare Interoperability
[ ] Description (use template from Junior PRD)
[ ] Demo video link (YouTube)
[ ] GitHub repo link
[ ] Pitch deck PDF uploaded
[ ] Theme selected: Health IT Systems
[ ] Submit button clicked
[ ] Confirmation screenshot saved
[ ] Shared in team chat
```

---

## Dependency Chart

```
Day 1 Morning:
Mid (Mock Data) → Senior (ABHA Match)
                → Mid (Database)
                → Junior (UI - can start)

Day 1 Afternoon:
Senior (Phonetic) → Senior (Fuzzy) → Senior (Simple Matcher)
Mid (Database) → Mid (APIs)
Junior (UI components - independent)

Day 2 Morning:
Senior (FastAPI) → ALL (Integration)

Day 2 Afternoon:
Junior (Demo Video + Pitch Deck)
Senior + Mid (Code Cleanup)
```

---

## Communication Protocol

### Slack/WhatsApp Messages

**When you complete a milestone**:
```
✅ [Your Name]: [Component] ready!
Example: "✅ Mid: Database ready! 20 patients, 40 visits loaded"
```

**When you're blocked**:
```
🔴 [Your Name]: Blocked on [Component]
Example: "🔴 Senior: Blocked on database - waiting for Mid's commit"
```

**When you need help**:
```
🆘 [Your Name]: Need help with [Issue]
Example: "🆘 Junior: Frontend not connecting to backend - CORS error?"
```

---

## Emergency Backup Plan

### If Behind Schedule

**End of Day 1 - Not everything done?**

**Priority order**:
1. ✅ **MUST HAVE**: Phonetic matching working
2. ✅ **MUST HAVE**: Database with golden pairs
3. ✅ **MUST HAVE**: Basic UI
4. ⚠️ **NICE TO HAVE**: All 3 matching strategies
5. ⚠️ **NICE TO HAVE**: Polished UI

**Cut if needed**:
- Fuzzy matching (just use ABHA + Phonetic)
- Unified history view (just show match results)
- Fancy UI animations

**NEVER CUT**:
- Phonetic matching (your differentiator!)
- Demo video (70% of score!)
- Pitch deck (70% of score!)

---

## Success Criteria

### Minimum Viable Demo (Must Have)
- [ ] Search for patient works
- [ ] Match shows 90% score for Ramesh↔Ramehs
- [ ] Phonetic matching explanation visible
- [ ] Demo video uploaded (3 min)
- [ ] Pitch deck complete (10 slides)

### Ideal Demo (Nice to Have)
- [ ] All 3 matching strategies working
- [ ] Unified history view
- [ ] Polished UI with animations
- [ ] All 5 golden pairs tested
- [ ] Clean, documented code

---

## Final Checklist (Before Submission)

```
Technical:
[ ] Backend running without errors
[ ] Frontend running without errors
[ ] All 5 golden pairs match correctly
[ ] Tests passing: pytest tests/ -v
[ ] Code formatted: black app/ tests/
[ ] README.md complete

Demo Materials:
[ ] Demo video: 2:30-3:00 minutes
[ ] Demo video: Shows phonetic matching
[ ] Demo video: Audio clear
[ ] Pitch deck: 10 slides
[ ] Pitch deck: No typos
[ ] Pitch deck: PDF < 10MB

Submission:
[ ] GitHub repo public
[ ] All code committed
[ ] Demo video link tested
[ ] Pitch deck uploaded
[ ] Submission confirmed
[ ] Screenshot saved
```

---

**You've got this! Follow the sequence, communicate often, and focus on the WOW factor!** 🚀

**Remember: Phonetic matching + Demo video + Pitch deck = Your winning formula!** 🏆

**Good luck!** ✨
