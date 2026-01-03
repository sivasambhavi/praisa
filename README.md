# PRAISA - AI-Powered Healthcare Interoperability Platform
## 2-Day POC Demo

**Demo Date**: January 4-5, 2026  
**Team**: 3 Cloud AI Engineers  
**Goal**: Working demo with 95% accuracy on Indian name matching  

---

## Quick Start

### For All Engineers (Do This First!)

```bash
# Clone repository
git clone <repo-url>
cd praisa

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify setup
python -c "import fastapi; print('✅ Setup complete!')"
```

---

## Project Structure

```
praisa/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore file
├── .env.example                 # Environment variables template
│
├── docs/                        # 📚 Documentation (READ THESE FIRST!)
│   ├── EXECUTION_GUIDE.md       # ⭐ START HERE - Step-by-step sequence
│   ├── SENIOR_ENGINEER_DEMO_PRD.md
│   ├── MID_ENGINEER_DEMO_PRD.md
│   ├── JUNIOR_ENGINEER_DEMO_PRD.md
│   └── 6_MONTH_PRODUCTION_ROADMAP.md
│
├── data/                        # 📊 Mock patient data (Mid Engineer)
│   ├── hospital_a_patients.csv  # 10 patients from Hospital A
│   ├── hospital_b_patients.csv  # 10 patients from Hospital B (5 golden pairs)
│   ├── hospital_a_visits.csv    # 20 visits
│   ├── hospital_b_visits.csv    # 20 visits
│   └── README.md                # Data documentation
│
├── app/                         # 🐍 Backend Python code
│   ├── __init__.py
│   ├── main.py                  # FastAPI application (Senior Engineer)
│   │
│   ├── matching/                # 🧠 Matching algorithms (Senior Engineer)
│   │   ├── __init__.py
│   │   ├── abha_match.py        # ABHA exact matching
│   │   ├── phonetic_match.py    # ⭐ Phonetic matching for Indian names
│   │   ├── fuzzy_match.py       # Fuzzy name matching
│   │   └── simple_matcher.py    # Combines all 3 strategies
│   │
│   ├── database/                # 💾 Database layer (Mid Engineer)
│   │   ├── __init__.py
│   │   ├── schema.sql           # SQLite schema
│   │   ├── db.py                # Database access layer
│   │   └── loader.py            # CSV data loader
│   │
│   ├── routes/                  # 🛣️ API routes
│   │   ├── __init__.py
│   │   ├── patients.py          # Patient CRUD APIs (Mid Engineer)
│   │   └── matching.py          # Matching API (Senior Engineer)
│   │
│   └── models/                  # 📋 Pydantic models
│       ├── __init__.py
│       ├── patient.py           # Patient data model
│       └── match.py             # Match result model
│
├── frontend/                    # 🎨 React UI (Junior Engineer)
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── SearchForm.jsx       # Patient search
│   │   │   ├── MatchResults.jsx     # ⭐ Match display (WOW moment!)
│   │   │   └── UnifiedHistory.jsx   # Timeline view
│   │   └── api/
│   │       └── client.js            # API client
│   └── README.md
│
├── tests/                       # 🧪 Test files
│   ├── __init__.py
│   ├── test_abha_match.py       # ABHA matching tests
│   ├── test_phonetic_match.py   # Phonetic matching tests
│   ├── test_fuzzy_match.py      # Fuzzy matching tests
│   ├── test_simple_matcher.py   # Integration tests
│   ├── test_db.py               # Database tests
│   └── test_integration.py      # Full flow tests
│
├── scripts/                     # 🔧 Utility scripts
│   ├── setup_database.sh        # Database setup script
│   ├── test_all_golden_pairs.py # Test all 5 golden pairs
│   └── generate_demo_data.py    # Backup data generator
│
├── demo/                        # 🎬 Demo materials (Junior Engineer)
│   ├── DEMO_SCRIPT.md           # 3-minute demo script
│   ├── pitch_deck/
│   │   └── PRAISA_Pitch_Deck.pdf
│   └── video/
│       └── demo_video_link.txt  # YouTube/Loom links
│
└── praisa_demo.db              # 💾 SQLite database (generated)
```

---

## Workflow by Engineer

### 🔴 Mid Engineer - Start Here First!

**Your files**:
- `data/*.csv` - Generate mock data
- `app/database/` - Database setup
- `app/routes/patients.py` - Patient APIs

**Day 1 Morning (9:30 AM - 12:00 PM)**:
```bash
# 1. Generate mock data using ChatGPT
# Save to data/*.csv

# 2. Create database
sqlite3 praisa_demo.db < app/database/schema.sql

# 3. Load data
python app/database/loader.py

# 4. Commit
git add data/ app/database/ praisa_demo.db
git commit -m "Add mock data and database"
git push

# ✅ Notify team: "Database ready! 20 patients loaded"
```

---

### 🟢 Senior Engineer - Wait for Mid's Database

**Your files**:
- `app/matching/` - All matching algorithms
- `app/main.py` - FastAPI backend
- `app/routes/matching.py` - Matching API

**Day 1 (11:00 AM - 5:00 PM)**:
```bash
# 1. Pull Mid's database
git pull

# 2. Create matching algorithms
# Use Antigravity prompts from docs/SENIOR_ENGINEER_DEMO_PRD.md

# 3. Test
pytest tests/test_*.py -v

# 4. Commit
git add app/matching/ tests/
git commit -m "Add matching algorithms"
git push

# ✅ Notify team: "Phonetic matching ready! 90% on Ramesh↔Ramehs"
```

---

### 🔵 Junior Engineer - Can Start Anytime

**Your files**:
- `frontend/` - All UI components
- `demo/` - Demo video & pitch deck

**Day 1 (1:00 PM - 5:00 PM)**:
```bash
# 1. Create UI components
cd frontend
npm install
npm run dev

# Use Bolt.new prompts from docs/JUNIOR_ENGINEER_DEMO_PRD.md

# 2. Commit
git add frontend/
git commit -m "Add UI components"
git push

# ✅ Notify team: "UI ready! Search, match, history views done"
```

---

## Running the Demo

### Backend (Terminal 1)
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Start FastAPI server
uvicorn app.main:app --reload

# Server running at: http://localhost:8000
# API docs: http://localhost:8000/docs
```

### Frontend (Terminal 2)
```bash
cd frontend
npm run dev

# UI running at: http://localhost:5173
```

### Test the Demo
```bash
# 1. Open browser: http://localhost:5173
# 2. Search for "Ramesh Singh"
# 3. Click "Match with Hospital B"
# 4. Select "Ramehs Singh"
# 5. See 90% match score! ⭐
# 6. Click "View Unified History"
# 7. See visits from both hospitals
```

---

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_phonetic_match.py -v

# Check coverage
pytest tests/ --cov=app --cov-report=html
```

---

## Git Workflow

### Branching Strategy
```bash
# Main branch: main
# Feature branches: feature/<engineer>-<component>

# Example:
git checkout -b feature/mid-database
git checkout -b feature/senior-phonetic
git checkout -b feature/junior-ui
```

### Commit Messages
```bash
# Format: [Engineer] Component: Description

# Examples:
git commit -m "[Mid] Database: Add SQLite schema and loader"
git commit -m "[Senior] Matching: Add phonetic matching for Indian names"
git commit -m "[Junior] UI: Add match results display"
```

### Pull Requests
```bash
# Before merging:
1. All tests pass: pytest tests/ -v
2. Code formatted: black app/ tests/
3. No console errors in frontend
4. Reviewed by at least 1 other engineer
```

---

## Environment Variables

Create `.env` file (copy from `.env.example`):
```bash
# Database
DATABASE_URL=sqlite:///./praisa_demo.db

# API
API_HOST=0.0.0.0
API_PORT=8000

# Frontend
VITE_API_URL=http://localhost:8000
```

---

## Dependencies

### Python (Backend)
```
fastapi==0.109.0
uvicorn==0.27.0
sqlalchemy==2.0.25
pydantic==2.5.3
rapidfuzz==3.6.1
jellyfish==1.0.3
pandas==2.1.4
pytest==7.4.4
black==24.1.1
```

### Node.js (Frontend)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.5"
  },
  "devDependencies": {
    "vite": "^5.0.11",
    "tailwindcss": "^3.4.1"
  }
}
```

---

## Troubleshooting

### Database locked?
```bash
pkill -f sqlite3
rm praisa_demo.db-journal
```

### Frontend not connecting to backend?
```bash
# Check CORS in app/main.py
# Ensure allow_origins=["*"] for development
```

### Tests failing?
```bash
# Ensure database exists
ls praisa_demo.db

# Ensure data loaded
sqlite3 praisa_demo.db "SELECT COUNT(*) FROM patients;"
# Expected: 20
```

---

## Demo Day Checklist

### Day 1 End
- [ ] Database: 20 patients, 40 visits loaded
- [ ] Matching: All 3 strategies working
- [ ] APIs: Patient CRUD + matching endpoints
- [ ] UI: Search, match, history components
- [ ] Tests: All passing

### Day 2 End
- [ ] Integration: Full flow working
- [ ] Demo video: 3 minutes, uploaded
- [ ] Pitch deck: 10 slides, PDF ready
- [ ] GitHub: All code committed
- [ ] Submission: Completed

---

## Key Features

✅ **3 Matching Strategies**:
1. ABHA Exact Match (100%)
2. Phonetic Match for Indian Names (90%) ⭐ WOW FACTOR
3. Fuzzy Match (80%+)

✅ **95% Accuracy** on demo data

✅ **<100ms Response Time**

✅ **ABDM Compliant** (roadmap)

---

## Contact

**Team**: 3 Cloud AI Engineers  
**Email**: team@praisa.health  
**GitHub**: [Your repo URL]  

---

## License

MIT License - See LICENSE file

---

**Read `docs/EXECUTION_GUIDE.md` for step-by-step instructions!** 📖

**Good luck with the demo!** 🚀
