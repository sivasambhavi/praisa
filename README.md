# PRAISA - AI-Powered Healthcare Interoperability Platform

**PRAISA** (Patient Record Aggregation & Intelligent Search Algorithm) is a state-of-the-art healthcare interoperability platform designed to unify patient records across disparate hospital systems. By leveraging advanced AI matching algorithms, PRAISA ensures 95%+ accuracy in record linkage, even with variations in Indian names, data entry errors, and missing identifiers.

---

## 📚 Documentation

For detailed instructions, please refer to the following guides:

| Guide                                                   | Description                                        |
| ------------------------------------------------------- | -------------------------------------------------- |
| [**Quick Start**](docs/guides/QUICK_START.md)           | Get the project up and running in minutes.         |
| [**Execution Guide**](docs/guides/EXECUTION_GUIDE.md)   | Step-by-step development and execution flow.       |
| [**Deployment Guide**](docs/guides/DEPLOYMENT_GUIDE.md) | Instructions for deploying to production.          |
| [**API Documentation**](docs/api/API_DOCUMENTATION.md)  | Comprehensive API reference for backend endpoints. |

> **Note:** If you are new to the project, start with the **[Quick Start Guide](docs/guides/QUICK_START.md)**.

---

## 🚀 Key Features

- **Advanced Patient Matching**:
  - **ABHA Exact Match**: 100% accuracy using unique health IDs.
  - **Phonetic Match**: Specialized algorithms (Soundex, Metaphone) for Indian names (e.g., "Ramesh" vs "Ramehs").
  - **Fuzzy Match**: Levenshtein distance-based matching for typos and OCR errors.
- **Unified Patient History**: Aggregates visits, prescriptions, and diagnoses from multiple hospital nodes into a single timeline.
- **High Performance**: Optimized search and retrieval with <100ms response time.
- **Modern UI**: Intuitive, responsive React-based frontend with a premium user experience.

---

## 🛠️ Technology Stack

### Backend

- **Framework**: FastAPI (Python 3.10+)
- **Database**: SQLite (Development), PostgreSQL (Production ready)
- **Algorithms**: `rapidfuzz`, `jellyfish` for string matching
- **Testing**: `pytest`

### Frontend

- **Framework**: React 18 + Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios

---

## 📂 Project Structure

```text
praisa/
├── app/                        # 🐍 Backend Application
│   ├── database/               # Database models and connection logic
│   ├── matching/               # Core matching algorithms (Phonetic, Fuzzy, etc.)
│   ├── models/                 # Pydantic data schemas
│   ├── routes/                 # FastAPI route definitions
│   └── main.py                 # Application entry point
│
├── data/                       # 📊 Mock Data & Seeds
│   ├── hospital_a_patients.csv
│   └── hospital_b_patients.csv
│
├── docs/                       # 📚 Project Documentation
│   ├── api/                    # API Specs
│   ├── guides/                 # Implementation & Deployment Guides
│   ├── prds/                   # Product Requirement Documents
│   └── roadmap/                # Future Roadmap
│
├── frontend/                   # 🎨 React Frontend Application
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   └── api/                # Frontend API client
│   └── package.json
│
├── scripts/                    # 🔧 Utility & Maintenance Scripts
│   ├── setup_database.sh
│   └── generate_demo_data.py
│
├── tests/                      # 🧪 Automated Tests
│   └── ...
│
├── .env.example                # Environment variables template
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## ⚡ Quick Start (Developer)

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

# Run the server
uvicorn app.main:app --reload
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

Visit `http://localhost:5173` to view the application.

---

## 🤝 Contributing

1. Fork the repository.
2. Create feature branch (`git checkout -b feature/amazing-feature`).
3. Commit changes (`git commit -m 'Add amazing feature'`).
4. Push to branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Team**: Cloud AI Engineers  
**Contact**: team@praisa.health
