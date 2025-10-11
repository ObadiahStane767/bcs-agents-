#!/usr/bin/env python3
"""
Demo script for Lead Follow-up AI Agent
Shows how to use the API with various lead scenarios
"""

import json
import requests
import time
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
API_ENDPOINT = f"{BASE_URL}/api/v1/lead"

# Example lead scenarios
LEAD_SCENARIOS = {
    "high_value_enterprise": {
        "zoho_id": "LEAD_001",
        "name": "Sarah Johnson",
        "email": "sarah.johnson@techcorp.com",
        "phone": "+1-555-0123",
        "source": "LinkedIn",
        "interest": "AI-powered analytics and cloud infrastructure",
        "due_date": "2024-03-15",
        "notes": "CTO reached out directly, high decision-making authority",
        "city": "San Francisco",
        "country": "USA"
    },
    
    "startup_opportunity": {
        "zoho_id": "LEAD_002",
        "name": "Mike Chen",
        "email": "mike@innovatestart.io",
        "phone": "+1-555-0456",
        "source": "Website",
        "interest": "Payment processing and fraud detection",
        "due_date": "2024-04-30",
        "notes": "Series A funding secured, ready to scale",
        "city": "Austin",
        "country": "USA"
    },
    
    "repeat_customer": {
        "zoho_id": "LEAD_003",
        "name": "Lisa Rodriguez",
        "email": "lisa.rodriguez@globalretail.com",
        "phone": "+1-555-0789",
        "source": "Referral",
        "interest": "E-commerce platform upgrade",
        "due_date": "2024-06-15",
        "notes": "Previous customer, successful implementation 2 years ago",
        "city": "Chicago",
        "country": "USA"
    },
    
    "cold_lead": {
        "zoho_id": "LEAD_004",
        "name": "David Wilson",
        "email": "david@localservices.com",
        "phone": "+1-555-0321",
        "source": "Cold Outreach",
        "interest": "Website redesign and basic CRM",
        "due_date": "2024-05-01",
        "notes": "Small business owner, limited tech knowledge",
        "city": "Denver",
        "country": "USA"
    }
}

def print_separator(title: str):
    """Print a formatted separator"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def analyze_lead(scenario_name: str, lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze a lead using the API
    
    Args:
        scenario_name: Name of the scenario
        lead_data: Lead data to analyze
        
    Returns:
        API response or error information
    """
    print(f"\n🔍 Analyzing: {scenario_name}")
    print(f"   Name: {lead_data['name']}")
    print(f"   Email: {lead_data['email']}")
    print(f"   Source: {lead_data['source']}")
    print(f"   Interest: {lead_data['interest']}")
    
    try:
        response = requests.post(
            API_ENDPOINT,
            json=lead_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Analysis Complete!")
            print(f"   Channel: {result['channel']}")
            print(f"   Priority: {result['priority']}/10")
            print(f"   To Agent: {'Yes' if result['to_agent'] else 'No'}")
            print(f"   Notes: {result['notes']}")
            if 'intent' in result:
                print(f"   Intent: {result['intent']}")
            if 'score' in result:
                print(f"   Score: {result['score']}")
            return result
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return {"error": response.status_code, "details": response.text}
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        return {"error": "connection_failed"}
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return {"error": "timeout"}
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return {"error": str(e)}

def run_demo():
    """Run the complete demo"""
    print("🚀 Lead Follow-up AI Agent Demo")
    print("=" * 60)
    print(f"🌐 API Base URL: {BASE_URL}")
    print(f"📡 Endpoint: {API_ENDPOINT}")
    print(f"📚 Documentation: {BASE_URL}/docs")
    print(f"🔍 Health Check: {BASE_URL}/api/v1/health")
    
    # Check if server is running
    try:
        health_response = requests.get(f"{BASE_URL}/api/v1/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ Server is running and healthy!")
        else:
            print("⚠️  Server responded but health check failed")
    except:
        print("❌ Server is not running. Start it with: python start_server.py")
        return
    
    # Run through all scenarios
    results = {}
    for scenario_name, lead_data in LEAD_SCENARIOS.items():
        result = analyze_lead(scenario_name, lead_data)
        results[scenario_name] = result
        
        # Small delay between requests
        time.sleep(1)
    
    # Summary
    print_separator("Demo Summary")
    successful_analyses = sum(1 for r in results.values() if 'error' not in r)
    total_scenarios = len(LEAD_SCENARIOS)
    
    print(f"📊 Scenarios tested: {total_scenarios}")
    print(f"✅ Successful analyses: {successful_analyses}")
    print(f"❌ Failed analyses: {total_scenarios - successful_analyses}")
    
    if successful_analyses > 0:
        print("\n🎯 Sample AI Recommendations:")
        for scenario_name, result in results.items():
            if 'error' not in result:
                print(f"   {scenario_name}: {result['channel']} (Priority: {result['priority']})")
    
    print("\n📝 Next Steps:")
    print("1. Review the AI recommendations above")
    print("2. Check the database for stored decisions")
    print("3. Customize the LLM prompt in src/config.py")
    print("4. Integrate with your n8n workflow")
    print("5. Deploy to production using DEPLOYMENT.md guide")

def main():
    """Main function"""
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")

if __name__ == "__main__":
    main()
