"""
Sales Rep Agent API for Lead Follow-up AI Agent
Handles lead analysis and next action planning for sales representatives.
"""

import json
import logging
from uuid import uuid4
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field, field_validator

from src.services.llm_service import analyze_lead, plan_next_action

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["lead"])

# ---- Legacy models for backwards compatibility ----
class LeadIn(BaseModel):
    zoho_id: str = Field(..., description="Zoho record ID")
    name: Optional[str] = None
    first_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[str] = Field(None, description="Email | WhatsApp | Instagram | etc.")
    interest: Optional[str] = None
    due_date: Optional[str] = Field(None, description="YYYY-MM-DD")
    notes: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    thread_key: Optional[str] = None         # Thread identifier for conversation tracking

    class Config:
        extra = "ignore"  # ignore any unexpected fields from upstream

class LeadDecision(BaseModel):
    zoho_id: str
    channel: str
    priority: int
    to_agent: bool
    notes: Optional[str] = None
    message: Optional[str] = None   # optional drafted copy
    intent: Optional[str] = None    # e.g., interior_design/general
    score: Optional[int] = None
    source: Optional[str] = None
    thread_key: Optional[str] = None         # Thread identifier for conversation tracking

# ---- New Sales Rep Agent models ----
class LeadContact(BaseModel):
    zoho_id: str
    name: Optional[str] = None
    first_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    interests: Optional[List[str]] = None
    source: Optional[str] = None
    
    @field_validator('interests', mode='before')
    @classmethod
    def validate_interests(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            return [v] if v.strip() else []
        if isinstance(v, list):
            return v
        return []

class LeadState(BaseModel):
    intent: Optional[str] = "general"        # e.g., interior_design/general
    preferred_channel: Optional[str] = None  # Email | WhatsApp | Phone | Instagram DM
    history: Optional[List[Dict[str, Any]]] = None  # [{role, text, channel, ts}]
    last_outcome: Optional[str] = None       # e.g., no_reply / busy / asked_price
    next_follow_up_at: Optional[str] = None  # ISO timestamp

class LeadRequest(BaseModel):
    lead: LeadContact
    state: Optional[LeadState] = LeadState()
    metadata: Optional[Dict[str, Any]] = {}

class ActionMessage(BaseModel):
    subject: Optional[str] = None
    body: Optional[str] = None
    whatsapp_text: Optional[str] = None

class ActionPlan(BaseModel):
    plan_id: str
    action: str                   # send_message | schedule_followup | handoff | stop
    channel: Optional[str] = None # Email | WhatsApp | Phone | Instagram DM
    message: Optional[ActionMessage] = None
    metadata: Dict[str, Any] = {} # {priority,to_agent,ai_notes,suggested_followup_in_hours?}
    log: Optional[str] = None
    store: Dict[str, Any] = {}    # write‑backs to CRM e.g. {decision_channel, decision_priority, ai_notes}

# ---- Legacy endpoint for backwards compatibility ----
@router.post("/lead", response_model=LeadDecision)
async def process_lead(lead: LeadIn):
    # Require at least one contact method
    if not (lead.email or lead.phone):
        raise HTTPException(status_code=400, detail="Provide email or phone.")

    # Call LLM/business logic
    decision = await analyze_lead(lead.model_dump())

    # Fill required fields with sensible defaults
    return LeadDecision(
        zoho_id=lead.zoho_id,
        channel=decision.get("channel") or (lead.source or "Email"),
        priority=int(decision.get("priority", 5)),
        to_agent=bool(decision.get("to_agent", True)),
        notes=decision.get("notes") or "",
        message=decision.get("message"),
        intent=decision.get("intent"),
        score=decision.get("score"),
        source=lead.source
        
        
    )

# ---- New Sales Rep Agent endpoints ----
@router.post("/next_action", response_model=ActionPlan)
async def next_action(payload: LeadRequest):
    """
    Determine the next action in a lead's journey.
    Returns action plan with thread_key passed through unchanged.
    """
    try:
        lead_dict = payload.lead.model_dump()
        state_dict = (payload.state or LeadState()).model_dump()

        # Extract thread_key from metadata with explicit key existence check
        metadata_dict = payload.metadata or {}
        thread_key = (metadata_dict or {}).get("thread_key", "")
        
        # Debug log to confirm the extracted thread_key
        logger.info(f"[/next_action] Extracted thread_key: {thread_key}")
        logger.info(f"[/next_action] Metadata: {metadata_dict}")

        plan = await plan_next_action(lead_dict, state_dict, metadata_dict)

        # Use the extracted thread_key
        plan_thread_key = thread_key

        plan.setdefault("plan_id", str(uuid4()))
        plan.setdefault("action", "wait") # Default action if LLM doesn't provide one
        plan.setdefault("channel", None)
        
        # Handle message as ActionMessage object
        message_data = plan.get("message", {})
        if isinstance(message_data, dict):
            plan["message"] = ActionMessage(
                subject=message_data.get("subject"),
                body=message_data.get("body"),
                whatsapp_text=message_data.get("whatsapp_text")
            )
        elif message_data is None:
            plan["message"] = None
        else:
            # If message is a string, put it in body
            plan["message"] = ActionMessage(body=str(message_data))

        # Ensure metadata is a dictionary and include required fields
        plan_metadata = plan.setdefault("metadata", {})
        plan_metadata.setdefault("thread_key", plan_thread_key) # Ensure thread_key is in metadata
        plan_metadata.setdefault("to_agent", False)
        plan_metadata.setdefault("ai_notes", "Action plan generated")
        plan_metadata.setdefault("suggested_follow_up_in_hours", 48)
        plan_metadata.setdefault("source", lead_dict.get("source")) # Add source from lead data
        plan_metadata.setdefault("country", lead_dict.get("country")) # Add country from lead data

        # Ensure store field exists (ActionPlan model requires it)
        plan.setdefault("store", {})

        # Debug log to confirm the extracted thread_key and metadata
        logger.info(f"[/next_action] Extracted thread_key: {thread_key}, Outgoing thread_key: {plan_metadata.get('thread_key')}")
        logger.info(f"[/next_action] Source: {lead_dict.get('source')}, Country: {lead_dict.get('country')}")
        logger.info(f"[/next_action] Metadata: {metadata_dict}")

        return ActionPlan(**plan)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lead processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Lead processing failed: {e}")

class RespondIn(BaseModel):
    plan_id: Optional[str] = None
    zoho_id: Optional[str] = None
    incoming_text: str
    channel: str                  # WhatsApp | Email | etc.
    timestamp: Optional[str] = None
    state: Optional[LeadState] = LeadState()

@router.post("/respond", response_model=ActionPlan)
async def respond(inbound: RespondIn):
    try:
        minimal_lead = {"zoho_id": inbound.zoho_id}
        state = (inbound.state or LeadState()).model_dump()
        state["history"] = (state.get("history") or []) + [{
            "role": "customer", "text": inbound.incoming_text,
            "channel": inbound.channel, "ts": inbound.timestamp
        }]
        plan = await plan_next_action(minimal_lead, state)
        plan.setdefault("plan_id", inbound.plan_id or str(uuid4()))
        return ActionPlan(**plan)
    except HTTPException:
        # re-raise explicit 4xx we triggered
        raise
    except Exception as e:
        # guard against accidental 500s with a readable message
        # (optional: log `e` with traceback)
        raise HTTPException(status_code=500, detail=f"Lead processing failed: {e}")

@router.get("/health")
async def health():
    return {"status": "ok"}

from fastapi import Request

@router.post("/debug_echo_any")
async def debug_echo_any(req: Request):
    raw = await req.body()
    try:
        parsed = await req.json()
    except Exception:
        parsed = None
    return {
        "content_type": req.headers.get("content-type"),
        "raw_text": raw.decode("utf-8", errors="replace"),
        "parsed_json": parsed,
    }

from fastapi import Request

@router.post("/next_action_flex", response_model=ActionPlan)
async def next_action_flex(req: Request):
    # ---- robust body parsing ----
    raw = await req.body()
    if not raw or not raw.strip():
        raise HTTPException(status_code=400, detail="Empty request body; send JSON.")

    ctype = (req.headers.get("content-type") or "").lower()
    try:
        if "application/json" in ctype:
            body = json.loads(raw)
        else:
            body = json.loads(raw)  # last-ditch
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

    # ---- flex shape normalization ----
    try:
        if "lead" not in body:
            lead = {
                "zoho_id":  body.get("zoho_id"),
                "name":     body.get("name"),
                "first_name": body.get("first_name"),
                "email":    body.get("email"),
                "phone":    body.get("phone"),
                "city":     body.get("city"),
                "country":  body.get("country"),
                "interests": body.get("interests") or [],
                "notes":     body.get("notes") or "",
            }
            if isinstance(lead["interests"], str):
                lead["interests"] = [lead["interests"]]
            state = {"intent": (body.get("intent") or "general")}
            # allow raw thread_key/subject on flat
            if body.get("thread_key"):
                state["thread_key"] = body["thread_key"]
            if body.get("subject"):
                state["subject"] = body["subject"]
            if body.get("history"):
                state["history"] = body["history"]
            
            # Extract metadata including thread_key
            metadata = {}
            if body.get("thread_key"):
                metadata["thread_key"] = body["thread_key"]
        else:
            lead = body.get("lead") or {}
            state = body.get("state") or {"intent": "general"}

        plan = await plan_next_action(lead, state)
        if not isinstance(plan, dict):
            raise ValueError("plan_next_action did not return a dict")

        # ---- normalize ActionPlan shape ----
        plan.setdefault("plan_id", str(uuid4()))
        plan.setdefault("action", "send_message")
        plan.setdefault("channel", plan.get("channel") or "Email")
        plan.setdefault("message", {"subject": None, "body": None, "whatsapp_text": None})
        plan.setdefault("metadata", {"priority": 5, "to_agent": False, "ai_notes": ""})
        plan.setdefault("log", "ok")
        store = plan.setdefault("store", {})
        store.setdefault("decision_channel", plan.get("channel"))
        store.setdefault("decision_priority", plan.get("metadata", {}).get("priority", 5))
        store.setdefault("ai_notes", plan.get("metadata", {}).get("ai_notes", ""))

        # ---- Passthroughs for n8n ----
        hist = (state.get("history") or [])
        last = hist[-1] if hist else {}
        meta = last.get("meta") or {}

        store.setdefault("zoho_id",   lead.get("zoho_id"))
        store.setdefault("name",      lead.get("name") or "")
        store.setdefault("first_name", lead.get("first_name") or "")
        store.setdefault("email",     lead.get("email") or "")
        store.setdefault("thread_key", meta.get("thread_key") or state.get("thread_key") or "")
        store.setdefault("subject",    meta.get("subject") or state.get("subject") or "")

        # small breadcrumb
        plan["metadata"]["history_seen"] = len(hist)
        if hist:
            plan["metadata"]["history_last"] = (last.get("text") or "")

        return ActionPlan(**plan)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"/next_action_flex failed: {e}")

# ---- Process Lead endpoint with metadata ----
class LeadPayload(BaseModel):
    zoho_id: str
    name: Optional[str] = None
    first_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    interest: Optional[str] = None
    due_date: Optional[str] = None
    notes: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class LeadOutput(BaseModel):
    zoho_id: str
    name: Optional[str] = None
    first_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    interest: Optional[str] = None
    due_date: Optional[str] = None
    notes: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

@router.post("/process_lead", response_model=LeadOutput)
async def process_lead(payload: LeadPayload):
    """
    Process lead and return core lead information with thread_key.
    Uses existing thread_key from metadata if provided, otherwise generates one.
    """
    # Check if thread_key is already provided in metadata
    thread_key = None
    if payload.metadata and payload.metadata.get("thread_key"):
        thread_key = payload.metadata.get("thread_key")
        logger.info(f"Using existing thread_key from metadata: {thread_key}")
    else:
        # Generate thread_key from email and source if not provided
        if payload.email and payload.source:
            thread_key = f"{payload.email}-{payload.source}"
        elif payload.email:
            thread_key = f"{payload.email}-Unknown"
        elif payload.source:
            thread_key = f"Unknown-{payload.source}"
        logger.info(f"Generated thread_key: {thread_key}")
        logger.info(f"Input email: {payload.email}, source: {payload.source}")

    # Return core lead information with metadata
    return LeadOutput(
        zoho_id=payload.zoho_id,
        name=payload.name,
        first_name=payload.first_name,
        email=payload.email,
        phone=payload.phone,
        source=payload.source,
        interest=payload.interest,
        due_date=payload.due_date,
        notes=payload.notes,
        city=payload.city,
        country=payload.country,
        metadata={
            "thread_key": thread_key
        }
    )


