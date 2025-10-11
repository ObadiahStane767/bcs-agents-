#!/usr/bin/env python3
"""
Test BCS agent functionality
"""

import os
import sys
sys.path.append('src')

# Set mock mode
os.environ["MOCK_LLM"] = "true"

from services.llm_service import _mock_action_plan

def test_bcs_agent():
    """Test basic BCS agent functionality"""
    
    # Test data
    lead_data = {
        "name": "John Doe",
        "first_name": "John",
        "email": "john@example.com",
        "phone": "+1234567890",
        "source": "Website"
    }
    
    state_data = {
        "preferred_channel": "whatsapp",
        "intent": "general"
    }
    
    print("Testing BCS agent functionality:")
    print("=" * 40)
    
    try:
        result = _mock_action_plan(lead_data, state_data)
        
        print(f"✅ Plan ID: {result.get('plan_id')}")
        print(f"✅ Action: {result.get('action')}")
        print(f"✅ Channel: {result.get('channel')}")
        print(f"✅ Message: {result.get('message', {})}")
        print(f"✅ Metadata: {result.get('metadata', {})}")
        
        # Verify required fields
        assert result.get("plan_id"), "Missing plan_id"
        assert result.get("action"), "Missing action"
        assert result.get("channel"), "Missing channel"
        assert result.get("message"), "Missing message"
        assert result.get("metadata"), "Missing metadata"
        
        print("\n✅ BCS agent is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ BCS agent error: {e}")
        return False

if __name__ == "__main__":
    success = test_bcs_agent()
    sys.exit(0 if success else 1)
