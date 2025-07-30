import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4")
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Agent Configuration
    max_iterations: int = int(os.getenv("MAX_ITERATIONS", "5"))
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    
    # Tool API Endpoints (To be configured by Onepath team)
    availability_api_url: str = os.getenv("AVAILABILITY_API_URL", "https://api.onepath.ai/v1/availability")
    pricing_api_url: str = os.getenv("PRICING_API_URL", "https://api.onepath.ai/v1/pricing")
    
    # API Authentication (To be configured by Onepath team)
    internal_api_key: str = os.getenv("INTERNAL_API_KEY", "")

settings = Settings()
