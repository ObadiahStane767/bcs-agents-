#!/usr/bin/env python3
"""
Test in-person sources always use in-person followup messages
"""

import os
import sys
sys.path.append('src')

# Set mock mode
os.environ["MOCK_LLM"] = "true"

from services.llm_service import _mock_action_plan

def test_in_person_always_followup():
    """Test that in-person sources always use in-person followup messages"""
    
    # Test data with in-person source (Harrods)
    lead_data = {
        "name": "John Doe",
        "first_name": "John",
        "email": "john@example.com",
        "phone": "+1234567890",
        "source": "Harrods",  # This is an in-person source
        "interests": ["cribs", "nursery"],  # Add interests to avoid Harrods guardrail
        "notes": "Looking for nursery furniture"  # Add notes to avoid Harrods guardrail
    }
    
    test_cases = [
        {
            "name": "No channel specified",
            "state_data": {"intent": "general"},
            "metadata_data": {},
            "expected_channel": "Email",  # Default for Harrods
            "expected_message_type": "in_person_followup"
        },
        {
            "name": "preferred_channel = phone",
            "state_data": {"preferred_channel": "phone", "intent": "general"},
            "metadata_data": {},
            "expected_channel": "Phone",  # Should respect channel choice
            "expected_message_type": "in_person_followup"  # But use in-person message
        },
        {
            "name": "preferred_channel = whatsapp",
            "state_data": {"preferred_channel": "whatsapp", "intent": "general"},
            "metadata_data": {},
            "expected_channel": "WhatsApp",  # Should respect channel choice
            "expected_message_type": "in_person_followup"  # But use in-person message
        },
        {
            "name": "metadata.channel = phone",
            "state_data": {"intent": "general"},
            "metadata_data": {"channel": "phone"},
            "expected_channel": "Phone",  # Should respect channel choice
            "expected_message_type": "in_person_followup"  # But use in-person message
        }
    ]
    
    print("Testing in-person sources always use in-person followup:")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   state_data: {test_case['state_data']}")
        print(f"   metadata_data: {test_case['metadata_data']}")
        
        result = _mock_action_plan(
            lead_data, 
            test_case['state_data'], 
            test_case['metadata_data']
        )
        
        actual_channel = result.get("channel")
        message = result.get("message", {})
        ai_notes = result.get("metadata", {}).get("ai_notes", "")
        
        print(f"   → Channel: '{actual_channel}'")
        print(f"   → Expected Channel: '{test_case['expected_channel']}'")
        print(f"   → AI Notes: '{ai_notes[:50]}...'")
        
        # Check if it used in-person logic
        is_in_person_message = "in-person followup" in ai_notes.lower()
        
        print(f"   → Uses in-person message: {is_in_person_message}")
        print(f"   → Expected: {test_case['expected_message_type']}")
        
        # Check channel
        channel_correct = actual_channel == test_case['expected_channel']
        message_correct = is_in_person_message
        
        if channel_correct and message_correct:
            print(f"   ✅ PASS")
        else:
            print(f"   ❌ FAIL")
            if not channel_correct:
                print(f"      Channel mismatch: got '{actual_channel}', expected '{test_case['expected_channel']}'")
            if not message_correct:
                print(f"      Message type mismatch: got standard message, expected in-person followup")

def test_in_store_copy_differs():
    """Ensure In-Store payloads use bespoke copy instead of Harrods text."""
    lead_data_in_store = {
        "name": "Maria Lopez",
        "first_name": "Maria",
        "email": "maria@example.com",
        "phone": "+1234567890",
        "source": "In-Store"
    }
    instore_plan = _mock_action_plan(lead_data_in_store, {"intent": "general"}, {})
    message = instore_plan.get("message") or {}
    subject = message.get("subject") or ""
    body = (message.get("body") or "").lower()
    assert "Lovely meeting you in store" in subject, "Subject should reflect in-store phrasing"
    assert "lovely meeting you in store" in body, "Body should use in-store friendly copy"


if __name__ == "__main__":
    test_in_person_always_followup()
    test_in_store_copy_differs()
