# PRAISA - AI-Powered Healthcare Interoperability Platform

**PRAISA** (Patient Record Aggregation & Intelligent Search Algorithm) is a state-of-the-art healthcare interoperability platform designed to unify patient records across disparate hospital systems. By leveraging advanced AI matching algorithms, PRAISA ensures 95%+ accuracy in record linkage, even with variations in Indian names, data entry errors, and missing identifiers.

---

## 🚀 Key Features

### 1. Advanced Patient Matching
- **ABHA Interaction**: 100% accuracy using government-issued unique health IDs.
- **Phonetic Matching**: Specialized algorithms (Soundex, Metaphone) to handle Indian name variations (e.g., "Ramesh" vs "Ramehs").
- **Fuzzy Matching**: Levenshtein distance-based matching for typos and OCR errors.
- **Deep Verification**: Heuristic weighting engine that adapts to data patterns.

### 2. Unified Patient History
Aggregates visits, prescriptions, and diagnoses from multiple hospital nodes into a single, chronological timeline.

### 3. Cross-Hospital Search
Seamlessly searches for patients across connected hospital nodes using Name, Mobile, Aadhaar, or ABHA number.

---

## 🏗️ End-to-End Architecture & Workflow

PRAISA uses a multi-stage pipeline to process and match patient records. Here is the flow demonstrated with real-world examples.

### Architecture Diagram
`Frontend UI` ➔ `FastAPI Backend` ➔ `Normalization Layer` ➔ `Matching Engine (Waterfall)` ➔ `Unified Response`

### Example 1: The "Good Record" (Successful Match)
**Scenario**: A doctor searches for "Ramesh Singh". The system finds a record in Hospital B that has a typo ("Ramehs Singh") but shares a government health ID (ABHA).

1.  **Input**: Search query `Ramesh Singh` triggers a scan of all connected hospital nodes.
2.  **Discovery**: System retrieves:
    *   **Local**: `Ramesh Singh` (Hospital A)
    *   **Remote**: `Ramehs Singh` (Hospital B)
3.  **Matching Engine Processing**:
    *   **Step 1 (ABHA Check)**: Both records have ABHA `12-3456-7890-1234`.
    *   **Result**: 🎯 **100% Match Confidence**.
4.  **UI Output**:
    *   **Status**: 🟢 **EXACT MATCH**
    *   **Action**: Automatically merges history.
    *   **Visual Result**: Doctor sees a single, unified timeline with visits from *both* hospitals.

### Example 2: The "Bad Record" (Ambiguous/No Match)
**Scenario**: A doctor searches for "Amit Kumar". The system finds "Amit Sharma" in another hospital. Data quality is low (missing phone numbers).

1.  **Input**: Search query `Amit Kumar`.
2.  **Discovery**: System retrieves:
    *   **Local**: `Amit Kumar` (Male, 24)
    *   **Remote**: `Amit Sharma` (Male, 25)
3.  **Matching Engine Processing**:
    *   **Step 1 (ABHA Check)**: IDs are missing or different. ❌
    *   **Step 2 (Phonetic)**: "Kumar" and "Sharma" do NOT sound alike. ❌
    *   **Step 3 (Fuzzy)**: Edit distance is too high. Score: 45%.
    *   **Result**: ⚠️ **Low Confidence (< 60%)**.
4.  **UI Output**:
    *   **Status**: 🔴 **NO MATCH**
    *   **Action**: Records are kept separate.
    *   **Visual Result**: System prevents a dangerous merge, ensuring patient safety.

---

## 🛠️ Technology Stack

| Component | Tech Stack |
| :--- | :--- |
| **Backend** | Python 3.10+, FastAPI, SQLAlchemy, SQLite (POC) |
| **Frontend** | React 18, Vite, Tailwind CSS, Axios |
| **Algorithms** | `rapidfuzz`, `jellyfish` (Phonetic/Fuzzy Logic) |
| **Testing** | `pytest`, `flake8` |

---

## 📂 Project Structure

```text
praisa/
├── app/                        # 🐍 Backend Application
│   ├── database/               # Database models & connection logic
│   ├── matching/               # Core matching algorithms
│   ├── models/                 # Pydantic data schemas
│   ├── routes/                 # FastAPI endpoints
│   └── main.py                 # Application entry point
│
├── frontend/                   # 🎨 React Frontend
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   └── api/                # API Integration
│   └── package.json
│
├── scripts/                    # 🔧 Utility Scripts
│   ├── setup_database.py       # DB Initialization & Seeding
│   └── start_demo.bat          # One-click demo start (Windows)
│
├── docs/                       # 📚 Documentation
│   └── api/                    # Detailed API Docs
│
└── requirements.txt            # Python Dependencies
```

---

## ⚡ Quick Start Guide

### Prerequisites
- Python 3.9+
- Node.js 18+

### 1. Backend Setup
```bash
# Clone the repository
git clone <repo-url>
cd praisa

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize Database & Load Mock Data
python scripts/setup_database.py

# Start Backend Server
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start Frontend Dev Server
npm run dev
```

Visit `http://localhost:5173` to verify the application is running.

---

## 🔌 API Reference (Summary)

Detailed documentation works at `http://localhost:8000/docs`.

### Patients
- `GET /api/patients/search`: Search by `name`, `abha`, `aadhaar`, or `phone`.
- `GET /api/patients/{id}`: Get full patient details.
- `GET /api/patients/{id}/history`: Get unified visit history.

### Matching
- `POST /api/match`: Compare two patient records for a match probability.
  ```json
  {
    "patient_a": { "name": "Ramesh", ... },
    "patient_b": { "name": "Ramehs", ... }
  }
  ```

---

## 🔮 Future Roadmap (4-Month Plan)

### Phase 1: Pilot & "Golden Data" Collection (Month 1)
- **Goal**: Deploy Hybrid System to collect verification data.
- **Actions**:
  - Deploy to 2 Pilot Hospitals.
  - Implement Human-in-the-Loop (HITL) feedback for "Review" matches.
  - Harvest "Verified Matches" (Golden Data) for future training.

### Phase 2: Federated Architecture (Month 2)
- **Goal**: Privacy-First Federated Network.
- **Actions**:
  - Install local "PRAISA Nodes" at hospitals.
  - Implement **Privacy-Preserving Record Linkage (PPRL)** using Bloom Filters.
  - HIPAA/DISHA Security Audit.

### Phase 3: Deep Learning Upgrade (Month 3)
- **Goal**: Replace heuristic model with Siamese Neural Networks.
- **Actions**:
  - Train Transformer-based models on the Golden Data.
  - Improve accuracy on complex comparisons to **99.5%**.

### Phase 4: ABDM Integration & Scale (Month 4)
- **Goal**: National Stack Integration.
- **Actions**:
  - Official ABDM Compliance (Consent Manager, ABHA linking).
  - Scale to 10+ Hospitals.

---

## 🤝 Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

**Team**: Tryminds 
