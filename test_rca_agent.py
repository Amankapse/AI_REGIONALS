import requests
import json

print("🔧 Testing RCA Agent with TCS GenAI Lab...")

url = "https://genailab.tcs.in/v1/chat/completions"
headers = {
    "Authorization": "Bearer sk-7oPG011CjuKcUPIUZ4FuRA",
    "Content-Type": "application/json"
}

# RCA prompt similar to what the agent will use
rca_prompt = """
Analyze manufacturing defect image with YOLO detections: ['person', 'bottle']

Generate professional RCA report in JSON format:
{
    "defect_type": "primary_defect",
    "root_causes": ["cause1", "cause2"],
    "immediate_action": "What to do NOW",
    "short_term_fix": "24-48hr fixes", 
    "long_term_prevention": "Process improvements",
    "risk_level": "CRITICAL|HIGH|MEDIUM|LOW",
    "estimated_cost": "$X-XXK",
    "downtime_estimate": "X hours"
}

Manufacturing context: PCB assembly line (IPC-A-610 Class 2)
"""

payload = {
    "model": "azure/genailab-maas-gpt-4o-mini",
    "messages": [{"role": "user", "content": rca_prompt}],
    "max_tokens": 500
}

try:
    print("📡 Testing RCA generation...")
    response = requests.post(url, headers=headers, json=payload, timeout=60, verify=False)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ RCA Agent Response:")
        print(data["choices"][0]["message"]["content"])
        print("\n🎉 TCS API is working for RCA Agent!")
    else:
        print(f"❌ API Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Connection Error: {e}")
