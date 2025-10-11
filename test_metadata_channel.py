#!/usr/bin/env python3
"""
Test Swagger override with metadata channel field
"""

import os
import sys
sys.path.append('src')

# Set mock mode
os.environ["MOCK_LLM"] = "true"

from services.llm_service import _mock_action_plan

def test_swagger_override_with_metadata():
    """Test that Swagger override works with channel in metadata"""
    
    # Test data
    lead_data = {
        "name": "John Doe",
        "first_name": "John",
        "email": "john@example.com",
        "phone": "+1234567890",
        "source": "Website"
    }
    
    state_data = {
        "intent": "general"
        # No preferred_channel set
    }
    
    metadata_data = {
        "channel": "phone"  # Channel in metadata
    }
    
    print("Testing Swagger override with channel in metadata:")
    print("=" * 55)
    
    result = _mock_action_plan(lead_data, state_data, metadata_data)
    
    actual_channel = result.get("channel")
    message = result.get("message", {})
    
    print(f"metadata.channel='phone' → channel='{actual_channel}'")
    
    # Check channel
    assert actual_channel == "Phone", f"Expected 'Phone', got '{actual_channel}'"
    
    # Check message fields - Phone should use whatsapp_text only
    assert message.get("whatsapp_text") is not None, "Phone should have whatsapp_text"
    assert message.get("subject") is None, "Phone should not have subject"
    assert message.get("body") is None, "Phone should not have body"
    
    print(f"  ✅ Message fields correct")
    print(f"  ✅ WhatsApp text: {message.get('whatsapp_text', '')[:50]}...")
    
    print("\n✅ Swagger override with metadata channel works!")

if __name__ == "__main__":
    test_swagger_override_with_metadata()
