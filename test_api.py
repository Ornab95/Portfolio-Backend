"""
Final test script with clear output formatting.
"""
import requests
import json

# API endpoint
url = "http://localhost:8000/api/contact"

# Test data
data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "subject": "Portfolio Inquiry",
    "message": "Hi! I came across your portfolio and I'm very impressed with your work. I would love to discuss a potential project opportunity with you."
}

print("=" * 60)
print("FastAPI Contact Form - Final Test")
print("=" * 60)
print(f"\n📧 Sending test email to: arnabbiswas426@gmail.com")
print(f"📍 API Endpoint: {url}\n")

try:
    response = requests.post(url, json=data)
    
    print(f"✅ Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success: {result.get('success')}")
        print(f"📨 Message: {result.get('message')}")
        print(f"\n🎉 TEST PASSED! Check your email inbox at arnabbiswas426@gmail.com")
    else:
        print(f"❌ Error: {response.json()}")
        print(f"\n⚠️ TEST FAILED")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"\n⚠️ TEST FAILED")

print("=" * 60)
