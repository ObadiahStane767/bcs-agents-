#!/usr/bin/env python3
"""
Test Swagger override with preferred_channel field
"""

import os
import sys
sys.path.append('src')

# Set mock mode
os.environ["MOCK_LLM"] = "true"

from services.llm_service import _mock_action_plan

def test_swagger_override_with_preferred_channel():
    """Test that Swagger override works with preferred_channel field"""
    
    # Test data
    lead_data = {
        "name": "John Doe",
        "first_name": "John",
        "email": "john@example.com",
        "phone": "+1234567890",
        "source": "Website"
    }
    
    # Test cases for preferred_channel
    test_cases = [
        ("whatsapp", "WhatsApp"),
        ("phone", "Phone"), 
        ("number", "Phone"),
        ("email", "Email"),
        ("call", "Phone"),
        ("wa", "WhatsApp")
    ]
    
    print("Testing Swagger override with preferred_channel field:")
    print("=" * 60)
    
    for preferred_channel, expected_channel in test_cases:
        state_data = {
            "preferred_channel": preferred_channel,
            "intent": "general"
        }
        
        result = _mock_action_plan(lead_data, state_data)
        
        actual_channel = result.get("channel")
        message = result.get("message", {})
        
        print(f"preferred_channel='{preferred_channel}' → channel='{actual_channel}'")
        
        # Check channel
        assert actual_channel == expected_channel, f"Expected '{expected_channel}', got '{actual_channel}'"
        
        # Check message fields based on channel
        if actual_channel in {"WhatsApp", "Phone"}:
            assert message.get("whatsapp_text") is not None, "WhatsApp/Phone should have whatsapp_text"
            assert message.get("subject") is None, "WhatsApp/Phone should not have subject"
            assert message.get("body") is None, "WhatsApp/Phone should not have body"
        else:  # Email
            assert message.get("subject") is not None, "Email should have subject"
            assert message.get("body") is not None, "Email should have body"
            assert message.get("whatsapp_text") is None, "Email should not have whatsapp_text"
        
        print(f"  ✅ Message fields correct")
    
    print("\n✅ All Swagger override tests with preferred_channel passed!")

if __name__ == "__main__":
    test_swagger_override_with_preferred_channel()
