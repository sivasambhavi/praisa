# PRAISA UI - Quick Start Guide

## 🚀 Running the Application

### Prerequisites

- Node.js installed (download from [nodejs.org](https://nodejs.org/))
- Backend server running at `http://localhost:8000`

### Start Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

Open browser to: **http://localhost:5173**

---

## 🔍 Testing Search Features

### 1. Search by Patient Name

- Click **"Patient Name"** tab
- Enter: `Ramesh`
- Select hospital: `Hospital A (Apollo)`
- Click **"Search Patient Records"**

### 2. Search by ABHA Number

- Click **"ABHA Number"** tab
- Enter: `12-3456-7890-1234`
- Click search

### 3. Search by Aadhar

- Click **"Aadhar Number"** tab
- Enter 12-digit Aadhar number
- Click search

### 4. Search by Phone

- Click **"Phone Number"** tab
- Enter: `9876543210`
- Click search

---

## 🎨 UI Features

✅ **Glassmorphic Design** - Frosted glass cards with backdrop blur  
✅ **Gradient Backgrounds** - Vibrant purple/blue/cyan theme  
✅ **Smooth Animations** - Fade-in, slide-up, scale effects  
✅ **Responsive Layout** - Mobile, tablet, desktop support  
✅ **Multi-Criteria Search** - Name, ABHA, Aadhar, Phone  
✅ **Premium Patient Cards** - Gradient avatars, demographics, actions  
✅ **Loading States** - Skeleton loaders and spinners  
✅ **Empty States** - Helpful messages when no results

---

## 📁 Files Modified

| File                                | Changes                                   |
| ----------------------------------- | ----------------------------------------- |
| `src/index.css`                     | Complete design system with glassmorphism |
| `src/components/AdvancedSearch.jsx` | NEW - Multi-criteria search interface     |
| `src/components/PatientCard.jsx`    | NEW - Premium patient card component      |
| `src/components/PatientList.jsx`    | NEW - Patient results grid                |
| `src/App.jsx`                       | Updated with new components and layout    |
| `src/api/client.js`                 | Updated for multi-criteria search         |

---

## 🐛 Troubleshooting

**Issue**: npm not found  
**Solution**: Install Node.js from nodejs.org and restart terminal

**Issue**: Backend connection error  
**Solution**: Ensure backend is running at http://localhost:8000

**Issue**: No results found  
**Solution**: Check that test data exists in database

---

## 📞 Need Help?

Check the full [walkthrough.md](file:///C:/Users/Aparna/.gemini/antigravity/brain/af4cfbd3-0892-4c36-b8a2-6706829ab17b/walkthrough.md) for detailed documentation.
