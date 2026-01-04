"""
FastAPI Main Application

Senior Engineer: Implement this file using Antigravity prompt from docs/SENIOR_ENGINEER_DEMO_PRD.md

TODO:
1. Create FastAPI app with CORS
2. Include routers for patients and matching
3. Add startup/shutdown events
4. Configure OpenAPI docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import patients, matching

app = FastAPI(
    title="PRAISA Healthcare Interoperability API",
    description="AI-Powered Patient Matching - Demo Version",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(patients.router, prefix="/api", tags=["patients"])
app.include_router(matching.router, prefix="/api", tags=["matching"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "PRAISA API v1.0",
        "docs": "/docs",
        "status": "ready"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}
