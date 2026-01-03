# PRAISA Frontend

## Setup

```bash
cd frontend
npm install
npm run dev
```

## Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── SearchForm.jsx       # Patient search
│   │   ├── MatchResults.jsx     # Match display (WOW moment!)
│   │   └── UnifiedHistory.jsx   # Timeline view
│   ├── api/
│   │   └── client.js            # API client
│   ├── App.jsx                  # Main app
│   └── main.jsx                 # Entry point
└── package.json
```

## Components

### SearchForm.jsx
Junior Engineer: Use Bolt.new prompt from `docs/JUNIOR_ENGINEER_DEMO_PRD.md`

### MatchResults.jsx ⭐ WOW MOMENT
Junior Engineer: This is the most important component! Shows:
- Two patient cards side-by-side
- Match score (90%)
- Method: "Phonetic Match (Indian Names)"
- Confidence: HIGH

### UnifiedHistory.jsx
Junior Engineer: Timeline of visits from both hospitals

## Running

```bash
npm run dev
# Open http://localhost:5173
```
