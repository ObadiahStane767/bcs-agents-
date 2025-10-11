#!/usr/bin/env python3
"""
Test script to verify Swagger test override logic
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.llm_service import _mock_action_plan

def test_swagger_override():
    """Test that Swagger test override forces WhatsApp channel"""
    
    # Sample lead data
    lead_data = {
        "zoho_id": "test_123",
        "name": "John Doe",
        "first_name": "John",
        "email": "john@example.com",
        "phone": "+1234567890",
        "source": "Website",
        "interests": ["cot bed"],
        "notes": "Interested in nursery furniture"
    }
    
    print("=== Testing Swagger Test Override ===")
    
    # Test 1: whatsapp (lowercase) - should trigger Swagger override
    state_data_whatsapp = {"channel": "whatsapp"}
    result_whatsapp = _mock_action_plan(lead_data, state_data_whatsapp)
    
    print(f"\nTest 1 - whatsapp (should trigger Swagger override):")
    print(f"  Channel: {result_whatsapp.get('channel')}")
    print(f"  Subject: {result_whatsapp.get('message', {}).get('subject')}")
    print(f"  Body: {result_whatsapp.get('message', {}).get('body')}")
    print(f"  WhatsApp Text: {result_whatsapp.get('message', {}).get('whatsapp_text')}")
    
    # Verify Swagger override
    assert result_whatsapp["channel"] == "WhatsApp", f"Expected 'WhatsApp', got '{result_whatsapp['channel']}'"
    assert result_whatsapp["message"]["subject"] is None, "Subject should be None for WhatsApp"
    assert result_whatsapp["message"]["body"] is None, "Body should be None for WhatsApp"
    assert result_whatsapp["message"]["whatsapp_text"] is not None, "WhatsApp text should not be None"
    print("✓ Swagger override forces WhatsApp channel correctly")
    
    # Test 2: WHATSAPP (uppercase) - should trigger Swagger override
    state_data_whatsapp_upper = {"channel": "WHATSAPP"}
    result_whatsapp_upper = _mock_action_plan(lead_data, state_data_whatsapp_upper)
    
    print(f"\nTest 2 - WHATSAPP (should trigger Swagger override):")
    print(f"  Channel: {result_whatsapp_upper.get('channel')}")
    print(f"  Subject: {result_whatsapp_upper.get('message', {}).get('subject')}")
    print(f"  Body: {result_whatsapp_upper.get('message', {}).get('body')}")
    print(f"  WhatsApp Text: {result_whatsapp_upper.get('message', {}).get('whatsapp_text')}")
    
    # Verify Swagger override
    assert result_whatsapp_upper["channel"] == "WhatsApp", f"Expected 'WhatsApp', got '{result_whatsapp_upper['channel']}'"
    assert result_whatsapp_upper["message"]["subject"] is None, "Subject should be None for WhatsApp"
    assert result_whatsapp_upper["message"]["body"] is None, "Body should be None for WhatsApp"
    assert result_whatsapp_upper["message"]["whatsapp_text"] is not None, "WhatsApp text should not be None"
    print("✓ Swagger override works with uppercase WHATSAPP")
    
    # Test 3: wa (abbreviation) - should NOT trigger Swagger override, use normal logic
    state_data_wa = {"channel": "wa"}
    result_wa = _mock_action_plan(lead_data, state_data_wa)
    
    print(f"\nTest 3 - wa (should NOT trigger Swagger override):")
    print(f"  Channel: {result_wa.get('channel')}")
    print(f"  Subject: {result_wa.get('message', {}).get('subject')}")
    print(f"  Body: {result_wa.get('message', {}).get('body')}")
    print(f"  WhatsApp Text: {result_wa.get('message', {}).get('whatsapp_text')}")
    
    # Verify normal logic (not Swagger override)
    assert result_wa["channel"] == "WhatsApp", f"Expected 'WhatsApp', got '{result_wa['channel']}'"
    assert result_wa["message"]["subject"] is None, "Subject should be None for WhatsApp"
    assert result_wa["message"]["body"] is None, "Body should be None for WhatsApp"
    assert result_wa["message"]["whatsapp_text"] is not None, "WhatsApp text should not be None"
    print("✓ Normal logic works for wa abbreviation")
    
    # Test 4: email - should NOT trigger Swagger override
    state_data_email = {"channel": "email"}
    result_email = _mock_action_plan(lead_data, state_data_email)
    
    print(f"\nTest 4 - email (should NOT trigger Swagger override):")
    print(f"  Channel: {result_email.get('channel')}")
    print(f"  Subject: {result_email.get('message', {}).get('subject')}")
    print(f"  Body: {result_email.get('message', {}).get('body')}")
    print(f"  WhatsApp Text: {result_email.get('message', {}).get('whatsapp_text')}")
    
    # Verify normal logic (not Swagger override)
    assert result_email["channel"] == "Email", f"Expected 'Email', got '{result_email['channel']}'"
    assert result_email["message"]["subject"] is not None, "Subject should not be None for Email"
    assert result_email["message"]["body"] is not None, "Body should not be None for Email"
    assert result_email["message"]["whatsapp_text"] is None, "WhatsApp text should be None for Email"
    print("✓ Normal logic works for email channel")
    
    print("\n=== All Swagger override tests passed! ===")

if __name__ == "__main__":
    test_swagger_override()
