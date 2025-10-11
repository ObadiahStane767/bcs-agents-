#!/usr/bin/env python3
"""
Generate exact Swagger UI payload for testing
"""

import json

print("Exact Swagger UI payloads to test:")
print("=" * 50)

print("\n1. Using preferred_channel in state:")
print("Endpoint: POST /next_action")
print("Payload:")
print(json.dumps({
    "lead": {
        "name": "John Doe",
        "first_name": "John", 
        "email": "john@example.com",
        "phone": "+1234567890",
        "source": "Website"
    },
    "state": {
        "preferred_channel": "phone",
        "intent": "general"
    },
    "metadata": {}
}, indent=2))

print("\n2. Using channel in metadata:")
print("Endpoint: POST /next_action")
print("Payload:")
print(json.dumps({
    "lead": {
        "name": "John Doe",
        "first_name": "John",
        "email": "john@example.com", 
        "phone": "+1234567890",
        "source": "Website"
    },
    "state": {
        "intent": "general"
    },
    "metadata": {
        "channel": "phone"
    }
}, indent=2))

print("\n3. Using /next_action_flex endpoint:")
print("Endpoint: POST /next_action_flex")
print("Payload:")
print(json.dumps({
    "name": "John Doe",
    "first_name": "John",
    "email": "john@example.com",
    "phone": "+1234567890", 
    "source": "Website",
    "channel": "phone",
    "intent": "general"
}, indent=2))

print("\n" + "=" * 50)
print("Expected Response for phone/number channels:")
print("- channel: 'Phone'")
print("- message.subject: null")
print("- message.body: null") 
print("- message.whatsapp_text: 'Hi John! Thanks for visiting...'")
print("\nIf you're getting email logic (subject/body), check:")
print("1. MOCK_LLM environment variable is set to 'true'")
print("2. You're using the correct endpoint")
print("3. The payload format matches exactly")
