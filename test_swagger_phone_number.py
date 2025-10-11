#!/usr/bin/env python3
"""
Test script to verify Swagger test override logic for phone and number channels
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.llm_service import _mock_action_plan

def test_swagger_override_phone_number():
    """Test that Swagger test override forces Phone channel for phone/number inputs"""
    
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
    
    print("=== Testing Swagger Test Override for Phone/Number ===")
    
    # Test 1: phone (lowercase) - should trigger Swagger override
    state_data_phone = {"channel": "phone"}
    result_phone = _mock_action_plan(lead_data, state_data_phone)
    
    print(f"\nTest 1 - phone (should trigger Swagger override):")
    print(f"  Channel: {result_phone.get('channel')}")
    print(f"  Subject: {result_phone.get('message', {}).get('subject')}")
    print(f"  Body: {result_phone.get('message', {}).get('body')}")
    print(f"  WhatsApp Text: {result_phone.get('message', {}).get('whatsapp_text')}")
    
    # Verify Swagger override
    assert result_phone["channel"] == "Phone", f"Expected 'Phone', got '{result_phone['channel']}'"
    assert result_phone["message"]["subject"] is None, "Subject should be None for Phone"
    assert result_phone["message"]["body"] is None, "Body should be None for Phone"
    assert result_phone["message"]["whatsapp_text"] is not None, "WhatsApp text should not be None for Phone"
    print("✓ Swagger override forces Phone channel correctly")
    
    # Test 2: PHONE (uppercase) - should trigger Swagger override
    state_data_phone_upper = {"channel": "PHONE"}
    result_phone_upper = _mock_action_plan(lead_data, state_data_phone_upper)
    
    print(f"\nTest 2 - PHONE (should trigger Swagger override):")
    print(f"  Channel: {result_phone_upper.get('channel')}")
    print(f"  Subject: {result_phone_upper.get('message', {}).get('subject')}")
    print(f"  Body: {result_phone_upper.get('message', {}).get('body')}")
    print(f"  WhatsApp Text: {result_phone_upper.get('message', {}).get('whatsapp_text')}")
    
    # Verify Swagger override
    assert result_phone_upper["channel"] == "Phone", f"Expected 'Phone', got '{result_phone_upper['channel']}'"
    assert result_phone_upper["message"]["subject"] is None, "Subject should be None for Phone"
    assert result_phone_upper["message"]["body"] is None, "Body should be None for Phone"
    assert result_phone_upper["message"]["whatsapp_text"] is not None, "WhatsApp text should not be None for Phone"
    print("✓ Swagger override works with uppercase PHONE")
    
    # Test 3: number (lowercase) - should trigger Swagger override
    state_data_number = {"channel": "number"}
    result_number = _mock_action_plan(lead_data, state_data_number)
    
    print(f"\nTest 3 - number (should trigger Swagger override):")
    print(f"  Channel: {result_number.get('channel')}")
    print(f"  Subject: {result_number.get('message', {}).get('subject')}")
    print(f"  Body: {result_number.get('message', {}).get('body')}")
    print(f"  WhatsApp Text: {result_number.get('message', {}).get('whatsapp_text')}")
    
    # Verify Swagger override
    assert result_number["channel"] == "Phone", f"Expected 'Phone', got '{result_number['channel']}'"
    assert result_number["message"]["subject"] is None, "Subject should be None for Phone"
    assert result_number["message"]["body"] is None, "Body should be None for Phone"
    assert result_number["message"]["whatsapp_text"] is not None, "WhatsApp text should not be None for Phone"
    print("✓ Swagger override works with number")
    
    # Test 4: NUMBER (uppercase) - should trigger Swagger override
    state_data_number_upper = {"channel": "NUMBER"}
    result_number_upper = _mock_action_plan(lead_data, state_data_number_upper)
    
    print(f"\nTest 4 - NUMBER (should trigger Swagger override):")
    print(f"  Channel: {result_number_upper.get('channel')}")
    print(f"  Subject: {result_number_upper.get('message', {}).get('subject')}")
    print(f"  Body: {result_number_upper.get('message', {}).get('body')}")
    print(f"  WhatsApp Text: {result_number_upper.get('message', {}).get('whatsapp_text')}")
    
    # Verify Swagger override
    assert result_number_upper["channel"] == "Phone", f"Expected 'Phone', got '{result_number_upper['channel']}'"
    assert result_number_upper["message"]["subject"] is None, "Subject should be None for Phone"
    assert result_number_upper["message"]["body"] is None, "Body should be None for Phone"
    assert result_number_upper["message"]["whatsapp_text"] is not None, "WhatsApp text should not be None for Phone"
    print("✓ Swagger override works with uppercase NUMBER")
    
    # Test 5: call (should NOT trigger Swagger override, use normal logic)
    state_data_call = {"channel": "call"}
    result_call = _mock_action_plan(lead_data, state_data_call)
    
    print(f"\nTest 5 - call (should NOT trigger Swagger override):")
    print(f"  Channel: {result_call.get('channel')}")
    print(f"  Subject: {result_call.get('message', {}).get('subject')}")
    print(f"  Body: {result_call.get('message', {}).get('body')}")
    print(f"  WhatsApp Text: {result_call.get('message', {}).get('whatsapp_text')}")
    
    # Verify normal logic (not Swagger override)
    assert result_call["channel"] == "Phone", f"Expected 'Phone', got '{result_call['channel']}'"
    assert result_call["message"]["subject"] is None, "Subject should be None for Phone"
    assert result_call["message"]["body"] is None, "Body should be None for Phone"
    assert result_call["message"]["whatsapp_text"] is not None, "WhatsApp text should not be None for Phone"
    print("✓ Normal logic works for call")
    
    print("\n=== All Swagger override tests for phone/number passed! ===")

if __name__ == "__main__":
    test_swagger_override_phone_number()
