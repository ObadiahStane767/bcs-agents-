from fastapi import FastAPI
from src.api.agent import router as agent_router

app = FastAPI(title="Lead Follow-up AI Agent", version="1.0.0")

# Mount routes
app.include_router(agent_router)

# Optional root
@app.get("/")
def root():
    return {"ok": True, "service": "lead-followup-agent"}



