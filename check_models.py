import requests
import json

print("🔧 Checking available models on TCS GenAI Lab...")

url = "https://genailab.tcs.in/v1/models"
headers = {
    "Authorization": "Bearer sk-7oPG011CjuKcUPIUZ4FuRA",
    "Content-Type": "application/json"
}

try:
    print("📡 Getting available models...")
    response = requests.get(url, headers=headers, timeout=30, verify=False)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Available Models:")
        for model in data.get("data", []):
            print(f"  - {model.get('id', 'Unknown')}")
    else:
        print(f"❌ API Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Connection Error: {e}")