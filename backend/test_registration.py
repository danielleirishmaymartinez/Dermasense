"""
Quick test script to verify registration endpoint works
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Test registration
test_user = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123",
    "full_name": "Test User"
}

print("Testing registration endpoint...")
try:
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=test_user,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 201:
        print("✅ Registration successful!")
        data = response.json()
        print(f"User ID: {data.get('id')}")
        print(f"Username: {data.get('username')}")
    else:
        print(f"❌ Registration failed: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

