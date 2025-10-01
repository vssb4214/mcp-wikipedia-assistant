"""
Simple configuration for Wikipedia MCP + CloudNatix API integration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# CloudNatix API Configuration
CLOUDNATIX_API_KEY = os.getenv("CLOUDNATIX_API_KEY", "YOUR_API_KEY_HERE")
CLOUDNATIX_API_URL = os.getenv("CLOUDNATIX_API_URL", "https://api.llm.cloudnatix.com/v1/chat/completions")
CLOUDNATIX_MODEL = os.getenv("CLOUDNATIX_MODEL", "Qwen-Qwen3-4B")
CLOUDNATIX_TEMPERATURE = float(os.getenv("CLOUDNATIX_TEMPERATURE", "0.1"))
CLOUDNATIX_MAX_TOKENS = int(os.getenv("CLOUDNATIX_MAX_TOKENS", "8218"))
CLOUDNATIX_TOP_P = float(os.getenv("CLOUDNATIX_TOP_P", "0.9"))
CLOUDNATIX_FREQUENCY_PENALTY = float(os.getenv("CLOUDNATIX_FREQUENCY_PENALTY", "0.3"))
CLOUDNATIX_PRESENCE_PENALTY = float(os.getenv("CLOUDNATIX_PRESENCE_PENALTY", "0.5"))

# System prompt for Wikipedia assistant
SYSTEM_PROMPT = "You are a helpful assistant that can use Wikipedia tools to answer questions. Use the available tools to provide accurate information."

# MCP Configuration
WIKIPEDIA_MCP_CONFIG = {
    "mcpServers": {
        "wikipedia": {
            "command": "wikipedia-mcp"
        }
    }
}