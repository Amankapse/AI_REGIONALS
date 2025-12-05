import requests
import json

print("🔧 Testing TCS API connectivity...")

url = "https://genailab.tcs.in/v1/chat/completions"
headers = {
    "Authorization": "Bearer sk-7oPG011CjuKcUPIUZ4FuRA",
    "Content-Type": "application/json"
}

payload = {
    "model": "azure/genailab-maas-gpt-4o-mini",  # Fixed: correct model name
    "messages": [{"role": "user", "content": "Test API: Quality inspection RCA ready!"}],
    "max_tokens": 50
}

try:
    print("📡 Sending request to TCS GenAI Lab...")
    response = requests.post(url, headers=headers, json=payload, timeout=30, verify=False)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ API Response:")
        print(data["choices"][0]["message"]["content"])
    else:
        print(f"❌ API Error: {response.status_code}")
        
except Exception as e:
    print(f"❌ Connection Error: {e}")
