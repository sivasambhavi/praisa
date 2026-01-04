# Scripts Directory

This directory contains utility scripts for PRAISA development and demo.

## Available Scripts

### `setup_database.py`
Initializes the database and loads mock patient data.

**Usage**:
```bash
python scripts/setup_database.py
```

**What it does**:
- Creates `praisa_demo.db` SQLite database
- Loads 20 patients from CSV files (10 per hospital)
- Loads 40 visits from CSV files (20 per hospital)
- Displays summary of loaded data

---

### `test_golden_pairs.py`
Comprehensive testing of all 5 golden pairs with detailed output.

**Usage**:
```bash
python scripts/test_golden_pairs.py
```

**What it does**:
- Tests combined matching (ABHA + Phonetic + Fuzzy)
- Tests phonetic matching independently
- Displays match scores and methods used
- Returns exit code 0 if all tests pass, 1 if any fail

---

### `start_demo.sh` (Linux/Mac)
Starts the PRAISA demo server.

**Usage**:
```bash
bash scripts/start_demo.sh
```

**What it does**:
- Checks if database exists (runs setup if needed)
- Starts FastAPI server on http://localhost:8000
- Opens API docs at http://localhost:8000/docs

---

### `start_demo.bat` (Windows)
Starts the PRAISA demo server on Windows.

**Usage**:
```cmd
scripts\start_demo.bat
```

**What it does**:
- Same as `start_demo.sh` but for Windows
- Checks database, starts server
- Displays URLs for API and docs

---

## Quick Start

**First time setup**:
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up database
python scripts/setup_database.py

# 3. Test matching algorithms
python scripts/test_golden_pairs.py

# 4. Start demo server
bash scripts/start_demo.sh  # Linux/Mac
# OR
scripts\start_demo.bat      # Windows
```

**Subsequent runs**:
```bash
# Just start the server
bash scripts/start_demo.sh  # Linux/Mac
# OR
scripts\start_demo.bat      # Windows
```

---

## Notes

- All scripts automatically add the project root to Python path
- Scripts are safe to run multiple times (database setup skips duplicates)
- Use Ctrl+C to stop the demo server
