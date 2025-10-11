"""
Main FastAPI application for Lead Follow-up AI Agent
"""

import sys
import os
from fastapi import FastAPI

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.agent import router as agent_router

app = FastAPI(title="Lead Follow-up AI Agent", version="1.0.0")

# Mount routes
app.include_router(agent_router)

# Optional root
@app.get("/")
def root():
    return {"ok": True, "service": "lead-followup-agent"}
