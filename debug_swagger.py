#!/usr/bin/env python3
"""
Debug Swagger override issue with phone/number channels
"""

import os
import sys
sys.path.append('src')

# Set mock mode
os.environ["MOCK_LLM"] = "true"

from services.llm_service import _mock_action_plan

def debug_swagger_override():
    """Debug why Swagger override isn't working for phone/number"""
    
    # Test data simulating Swagger UI payload
    lead_data = {
        "name": "John Doe",
        "first_name": "John",
        "email": "john@example.com",
        "phone": "+1234567890",
        "source": "Website"
    }
    
    # Test different scenarios
    test_cases = [
        {
            "name": "preferred_channel = phone",
            "state_data": {"preferred_channel": "phone", "intent": "general"},
            "metadata_data": {}
        },
        {
            "name": "preferred_channel = number", 
            "state_data": {"preferred_channel": "number", "intent": "general"},
            "metadata_data": {}
        },
        {
            "name": "metadata.channel = phone",
            "state_data": {"intent": "general"},
            "metadata_data": {"channel": "phone"}
        },
        {
            "name": "metadata.channel = number",
            "state_data": {"intent": "general"}, 
            "metadata_data": {"channel": "number"}
        },
        {
            "name": "state.channel = phone",
            "state_data": {"channel": "phone", "intent": "general"},
            "metadata_data": {}
        }
    ]
    
    print("Debugging Swagger override for phone/number channels:")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print(f"   state_data: {test_case['state_data']}")
        print(f"   metadata_data: {test_case['metadata_data']}")
        
        result = _mock_action_plan(
            lead_data, 
            test_case['state_data'], 
            test_case['metadata_data']
        )
        
        actual_channel = result.get("channel")
        message = result.get("message", {})
        
        print(f"   → Result channel: '{actual_channel}'")
        print(f"   → Has subject: {message.get('subject') is not None}")
        print(f"   → Has body: {message.get('body') is not None}")
        print(f"   → Has whatsapp_text: {message.get('whatsapp_text') is not None}")
        
        # Check if it's using email logic (has subject/body) vs WhatsApp logic (has whatsapp_text only)
        if message.get("subject") and message.get("body") and not message.get("whatsapp_text"):
            print(f"   ❌ Using EMAIL logic (wrong for phone/number)")
        elif message.get("whatsapp_text") and not message.get("subject") and not message.get("body"):
            print(f"   ✅ Using WHATSAPP logic (correct for phone/number)")
        else:
            print(f"   ⚠️  Mixed or unexpected message format")

if __name__ == "__main__":
    debug_swagger_override()
