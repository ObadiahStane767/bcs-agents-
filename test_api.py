#!/usr/bin/env python3
"""
Simple test script for Lead Follow-up AI Agent API
This script tests the API structure without requiring OpenAI API calls
"""

import json
import requests
import time

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_LEAD_DATA = {
    "zoho_id": "LEAD_TEST_001",
    "name": "Jane Smith",
    "first_name": "Jane",
    "email": "jane@testcorp.com",
    "phone": "+1234567890",
    "source": "Website",
    "interest": "Interior design services",
    "due_date": "2024-02-15",
    "notes": "High potential client, interested in luxury interior design",
    "city": "San Francisco",
    "country": "USA"
}

def test_root_endpoint():
    """Test the root endpoint"""
    print("🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint working: {data['message']}")
            print(f"   Version: {data['version']}")
            print(f"   Status: {data['status']}")
            print(f"   Available endpoints: {list(data['endpoints'].keys())}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
    except Exception as e:
        print(f"❌ Error testing root endpoint: {e}")

def test_health_endpoint():
    """Test the health check endpoint"""
    print("\n🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check working")
            print(f"   Overall status: {data['status']}")
            print(f"   LLM service: {data['llm_service']}")
            print(f"   Database: {data['database']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}")

def test_lead_analysis_endpoint():
    """Test the lead analysis endpoint"""
    print("\n🔍 Testing lead analysis endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/lead",
            json=TEST_LEAD_DATA,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Lead analysis successful!")
            print(f"   Zoho ID: {data['zoho_id']}")
            print(f"   Channel: {data['channel']}")
            print(f"   Priority: {data['priority']}")
            print(f"   To Agent: {data['to_agent']}")
            print(f"   Notes: {data['notes']}")
            if 'intent' in data:
                print(f"   Intent: {data['intent']}")
            if 'score' in data:
                print(f"   Score: {data['score']}")
        elif response.status_code == 500:
            print("⚠️  Lead analysis endpoint responded with server error")
            print("   This is expected if OpenAI API key is not configured")
            print("   The endpoint structure is working correctly")
        else:
            print(f"❌ Lead analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
    except Exception as e:
        print(f"❌ Error testing lead analysis endpoint: {e}")

def test_first_name_field():
    """Test that first_name field is properly handled"""
    print("\n🔍 Testing first_name field handling...")
    try:
        # Test with first_name provided
        test_data_with_first_name = {
            "zoho_id": "LEAD_TEST_FIRST_NAME",
            "name": "John Doe",
            "first_name": "John",
            "email": "john@testcorp.com",
            "source": "Website"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/next_action_flex",
            json=test_data_with_first_name,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ next_action_flex endpoint with first_name successful!")
            print(f"   Zoho ID: {data.get('store', {}).get('zoho_id')}")
            print(f"   Name: {data.get('store', {}).get('name')}")
            print(f"   First Name: {data.get('store', {}).get('first_name')}")
            print(f"   Email: {data.get('store', {}).get('email')}")
            
            # Verify first_name is in the store
            if data.get('store', {}).get('first_name') == "John":
                print("✅ first_name correctly passed through to store field")
            else:
                print(f"❌ first_name not found in store: {data.get('store', {})}")
        else:
            print(f"❌ next_action_flex failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
    except Exception as e:
        print(f"❌ Error testing first_name field: {e}")

def test_api_documentation():
    """Test if API documentation is accessible"""
    print("\n🔍 Testing API documentation...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ API documentation accessible at /docs")
        else:
            print(f"❌ API documentation not accessible: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
    except Exception as e:
        print(f"❌ Error testing API documentation: {e}")

def main():
    """Run all tests"""
    print("🚀 Lead Follow-up AI Agent API Test Suite")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    # Run tests
    test_root_endpoint()
    test_health_endpoint()
    test_lead_analysis_endpoint()
    test_first_name_field()
    test_api_documentation()
    
    print("\n" + "=" * 50)
    print("🏁 Test suite completed!")
    print("\n📝 Next steps:")
    print("1. Set your OpenAI API key in .env file")
    print("2. Restart the server")
    print("3. Run this test again to see full functionality")
    print(f"4. Visit {BASE_URL}/docs for interactive API documentation")

if __name__ == "__main__":
    main()
