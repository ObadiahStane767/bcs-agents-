#!/usr/bin/env python3
"""
Test in-person override skip logic for phone/number/whatsapp channels
"""

import os
import sys
sys.path.append('src')

# Set mock mode
os.environ["MOCK_LLM"] = "true"

from services.llm_service import _mock_action_plan

def test_in_person_override_skip():
    """Test that in-person leads skip override for phone/number/whatsapp channels"""
    
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
            "expected": "in_person_followup"  # Should use in-person logic
        },
        {
            "name": "preferred_channel = phone",
            "state_data": {"preferred_channel": "phone", "intent": "general"},
            "metadata_data": {},
            "expected": "whatsapp_logic"  # Should skip in-person, use WhatsApp logic
        },
        {
            "name": "preferred_channel = number",
            "state_data": {"preferred_channel": "number", "intent": "general"},
            "metadata_data": {},
            "expected": "whatsapp_logic"  # Should skip in-person, use WhatsApp logic
        },
        {
            "name": "preferred_channel = whatsapp",
            "state_data": {"preferred_channel": "whatsapp", "intent": "general"},
            "metadata_data": {},
            "expected": "whatsapp_logic"  # Should skip in-person, use WhatsApp logic
        },
        {
            "name": "metadata.channel = phone",
            "state_data": {"intent": "general"},
            "metadata_data": {"channel": "phone"},
            "expected": "whatsapp_logic"  # Should skip in-person, use WhatsApp logic
        },
        {
            "name": "preferred_channel = email",
            "state_data": {"preferred_channel": "email", "intent": "general"},
            "metadata_data": {},
            "expected": "in_person_followup"  # Should use in-person logic (email is not WhatsApp channel)
        }
    ]
    
    print("Testing in-person override skip logic:")
    print("=" * 50)
    
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
        print(f"   → AI Notes: '{ai_notes[:50]}...'")
        
        # Determine if it used in-person logic or WhatsApp logic
        if "in-person followup" in ai_notes.lower():
            actual_logic = "in_person_followup"
        elif message and message.get("whatsapp_text") and not message.get("subject"):
            actual_logic = "whatsapp_logic"
        elif message and message.get("subject") and message.get("body"):
            actual_logic = "email_logic"
        else:
            actual_logic = "other_logic"
        
        print(f"   → Logic used: {actual_logic}")
        print(f"   → Expected: {test_case['expected']}")
        
        if actual_logic == test_case['expected']:
            print(f"   ✅ PASS")
        else:
            print(f"   ❌ FAIL")

if __name__ == "__main__":
    test_in_person_override_skip()
