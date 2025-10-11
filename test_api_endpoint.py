#!/usr/bin/env python3
"""
Test the actual API endpoint to see what's happening
"""

import os
import sys
import json
sys.path.append('src')

# Set mock mode
os.environ["MOCK_LLM"] = "true"

from services.llm_service import plan_next_action

async def test_api_endpoint():
    """Test the actual plan_next_action function"""
    
    # Test data simulating Swagger UI payload
    lead_data = {
        "name": "John Doe",
        "first_name": "John",
        "email": "john@example.com",
        "phone": "+1234567890",
        "source": "Website"
    }
    
    state_data = {
        "preferred_channel": "phone",
        "intent": "general"
    }
    
    metadata_data = {}
    
    print("Testing plan_next_action function directly:")
    print("=" * 50)
    print(f"lead_data: {lead_data}")
    print(f"state_data: {state_data}")
    print(f"metadata_data: {metadata_data}")
    print(f"MOCK_LLM: {os.getenv('MOCK_LLM')}")
    
    try:
        result = await plan_next_action(lead_data, state_data, metadata_data)
        
        print(f"\nResult:")
        print(f"  plan_id: {result.get('plan_id')}")
        print(f"  action: {result.get('action')}")
        print(f"  channel: {result.get('channel')}")
        
        message = result.get("message", {})
        print(f"  message.subject: {message.get('subject')}")
        print(f"  message.body: {message.get('body')}")
        print(f"  message.whatsapp_text: {message.get('whatsapp_text')}")
        
        # Check if it's using email logic
        if message.get("subject") and message.get("body") and not message.get("whatsapp_text"):
            print(f"\n❌ Using EMAIL logic (wrong for phone)")
        elif message.get("whatsapp_text") and not message.get("subject") and not message.get("body"):
            print(f"\n✅ Using WHATSAPP logic (correct for phone)")
        else:
            print(f"\n⚠️  Mixed or unexpected message format")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_api_endpoint())
