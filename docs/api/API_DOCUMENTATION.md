# PRAISA API Documentation

## Base URL

**Development**: `http://localhost:8000`  
**API Prefix**: `/api`

---

## Authentication

Currently no authentication required (POC demo).  
Production will use JWT tokens.

---

## Endpoints

### Health & Info

#### `GET /`
Root endpoint with API information.

**Response**:
```json
{
  "message": "PRAISA API v1.0",
  "description": "AI-Powered Healthcare Interoperability Platform",
  "docs": "/docs",
  "status": "ready",
  "endpoints": {...}
}
```

#### `GET /health`
Enhanced health check with database status.

**Response**:
```json
{
  "status": "healthy",
  "database": {
    "status": "connected",
    "file_exists": true
  },
  "version": "1.0.0",
  "environment": "development",
  "timestamp": "2026-01-04T12:23:00"
}
```

---

### Patient Endpoints

#### `GET /api/patients/search`
Search patients by name or ABHA number.

**Query Parameters**:
- `name` (optional): Patient name (partial match, min 2 chars)
- `abha` (optional): ABHA number (exact match, min 14 chars)

**Example**:
```bash
GET /api/patients/search?name=Ramesh
GET /api/patients/search?abha=12-3456-7890-1234
```

**Response**:
```json
{
  "results": [
    {
      "patient_id": "HA001",
      "hospital_id": "hospital_a",
      "name": "Ramesh Singh",
      "dob": "1985-03-15",
      "mobile": "9876543210",
      "gender": "M",
      "abha_number": "12-3456-7890-1234",
      "address": "123 MG Road Mumbai",
      "state": "Maharashtra"
    }
  ],
  "count": 1
}
```

#### `GET /api/patients/{patient_id}`
Get patient details by ID.

**Path Parameters**:
- `patient_id`: Unique patient identifier (e.g., "HA001")

**Example**:
```bash
GET /api/patients/HA001
```

**Response**:
```json
{
  "patient_id": "HA001",
  "hospital_id": "hospital_a",
  "name": "Ramesh Singh",
  ...
}
```

**Error (404)**:
```json
{
  "detail": "Patient HA001 not found"
}
```

#### `GET /api/patients/{patient_id}/history`
Get patient's complete visit history.

**Path Parameters**:
- `patient_id`: Unique patient identifier

**Example**:
```bash
GET /api/patients/HA001/history
```

**Response**:
```json
{
  "patient": {...},
  "visits": [
    {
      "visit_id": "VA002",
      "patient_id": "HA001",
      "admission_date": "2025-12-20 14:30:00",
      "visit_type": "OPD",
      "diagnosis": "Diabetes Follow-up",
      "doctor_name": "Dr. Anjali Mehta"
    },
    ...
  ],
  "visit_count": 2
}
```

---

### Matching Endpoint

#### `POST /api/match`
Match two patients using combined strategies.

**Request Body**:
```json
{
  "patient_a": {
    "patient_id": "HA001",
    "name": "Ramesh Singh",
    "abha_number": "12-3456-7890-1234",
    "dob": "1985-03-15",
    ...
  },
  "patient_b": {
    "patient_id": "HB001",
    "name": "Ramehs Singh",
    "abha_number": "12-3456-7890-1234",
    "dob": "1985-03-15",
    ...
  }
}
```

**Response**:
```json
{
  "match_score": 100.0,
  "confidence": "high",
  "method": "ABHA_EXACT",
  "recommendation": "MATCH",
  "patient_a_id": "HA001",
  "patient_b_id": "HB001",
  "details": {
    "abha_result": {
      "score": 100.0,
      "method": "ABHA_EXACT",
      "matched": true,
      "details": "ABHA numbers match: 12-3456-7890-1234"
    },
    "phonetic_result": {...},
    "fuzzy_result": {...}
  }
}
```

**Matching Methods**:
- `ABHA_EXACT`: ABHA numbers match (100% confidence)
- `PHONETIC_INDIAN`: Names match phonetically (90% confidence)
- `FUZZY`: String similarity match (80-100% confidence)
- `NONE`: No match found

**Recommendations**:
- `MATCH`: Auto-match (score >= 80%)
- `REVIEW`: Manual review needed (score 60-79%)
- `NO_MATCH`: Different patients (score < 60%)

**Confidence Levels**:
- `high`: ABHA or phonetic match
- `medium`: Fuzzy match >= 80%
- `low`: Fuzzy match 60-79%
- `none`: No match

---

## Interactive Documentation

Visit `/docs` for Swagger UI with interactive API testing.

**Features**:
- Try out endpoints directly
- See request/response schemas
- View all available parameters
- Test with sample data

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message here"
}
```

**Common Status Codes**:
- `200`: Success
- `400`: Bad request (missing parameters)
- `404`: Resource not found
- `500`: Server error

---

## Rate Limiting

No rate limiting in POC.  
Production will have rate limits.

---

## Examples

### cURL Examples

```bash
# Search by name
curl "http://localhost:8000/api/patients/search?name=Ramesh"

# Get patient details
curl "http://localhost:8000/api/patients/HA001"

# Match two patients
curl -X POST "http://localhost:8000/api/match" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_a": {"patient_id": "HA001", "name": "Ramesh Singh", "abha_number": "12-3456-7890-1234"},
    "patient_b": {"patient_id": "HB001", "name": "Ramehs Singh", "abha_number": "12-3456-7890-1234"}
  }'
```

### Python Examples

```python
import requests

# Search patients
response = requests.get("http://localhost:8000/api/patients/search", params={"name": "Ramesh"})
patients = response.json()

# Match patients
response = requests.post("http://localhost:8000/api/match", json={
    "patient_a": {"patient_id": "HA001", "name": "Ramesh Singh", "abha_number": "12-3456-7890-1234"},
    "patient_b": {"patient_id": "HB001", "name": "Ramehs Singh", "abha_number": "12-3456-7890-1234"}
})
match_result = response.json()
print(f"Match score: {match_result['match_score']}%")
```

---

## WebSocket Support

Not available in POC.  
Production will support real-time updates.
