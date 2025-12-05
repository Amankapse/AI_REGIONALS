from langchain_openai import ChatOpenAI
import httpx
import sys

print("🔧 Setting up TCS API client...")
try:
    client = httpx.Client(verify=False, timeout=30.0)  # TCS lab requirement with timeout
    
    print("🤖 Initializing ChatOpenAI with TCS endpoint...")
    llm = ChatOpenAI(
        base_url="https://genailab.tcs.in/v1",
        model="azure/genailab-maas-gpt-4o-mini",  # Correct model name from API
        api_key="sk-7oPG011CjuKcUPIUZ4FuRA",
        http_client=client
    )
    
    print("📡 Sending test request to TCS GenAI Lab...")
    response = llm.invoke("Test API: Quality inspection RCA ready!")
    print("✅ API Response:")
    print(response.content)
    
except Exception as e:
    print(f"❌ API Error: {e}")
    sys.exit(1) 