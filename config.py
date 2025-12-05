import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")
    DEBUG = True
    SESSION_TYPE = 'filesystem'
    
    # Model config
    MODEL_PATH = "yolov8n.pt"
    MODEL_VERSION = "v1.0"    # TCS GenAI Lab API Configuration
    AI_API_KEY = os.getenv("AI_API_KEY", "sk-7oPG011CjuKcUPIUZ4FuRA")
    AI_API_BASE_URL = os.getenv("AI_API_BASE_URL", "https://genailab.tcs.in/v1")
    AI_MODEL_NAME = os.getenv("AI_MODEL_NAME", "azure/genailab-maas-gpt-4o-mini")
    AI_EMBED_MODEL_NAME = os.getenv("AI_EMBED_MODEL_NAME", "azure/genailab-maas-text-embedding-3-large")
