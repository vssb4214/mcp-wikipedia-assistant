#!/bin/bash

echo "[Marvin] Setting up the Wikipedia MCP + CloudNatix integration. The universe demands it."

# Check if Python 3.11+ is available
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
if [[ $(echo "$python_version >= 3.11" | bc -l) -eq 1 ]]; then
    echo "[Marvin] Python $python_version detected. At least the universe got something right."
else
    echo "[Marvin] Warning: Python 3.11+ recommended. Current version: $python_version"
fi

# Install Python dependencies
echo "[Marvin] Installing Python dependencies..."
cd Summarizer
pip install -r requirements.txt
cd ..

# Check if MCP server is available
echo "[Marvin] Checking MCP server availability..."
if command -v poetry &> /dev/null; then
    echo "[Marvin] Poetry found. Setting up MCP server..."
    cd MCP-Server
    poetry install
    echo "[Marvin] MCP server dependencies installed."
    cd ..
else
    echo "[Marvin] Poetry not found. Please install Poetry to run the MCP server."
    echo "[Marvin] Visit: https://python-poetry.org/docs/#installation"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "[Marvin] Creating .env file for configuration..."
    cat > .env << EOF
# CloudNatix API Configuration
CLOUDNATIX_API_KEY=YOUR_API_KEY_HERE
CLOUDNATIX_API_URL=https://api.llm.cloudnatix.com/v1/chat/completions
CLOUDNATIX_MODEL=Qwen-Qwen3-4B
CLOUDNATIX_TEMPERATURE=0.1
CLOUDNATIX_MAX_TOKENS=8218
CLOUDNATIX_TOP_P=0.9
CLOUDNATIX_FREQUENCY_PENALTY=0.3
CLOUDNATIX_PRESENCE_PENALTY=0.5

# MCP Configuration
MCP_SERVER_COMMAND=wikipedia-mcp

# Optional: Ollama configuration (for legacy support)
OLLAMA_URL=http://localhost:11434
EOF
    echo "[Marvin] .env file created. The universe now has configuration."
else
    echo "[Marvin] .env file already exists. The universe is consistent for once."
fi

echo "[Marvin] Setup complete. The universe continues its indifferent march."
echo "[Marvin] To start the Wikipedia bot, run: python wikipedia_bot.py"
echo "[Marvin] Remember to set your API keys in the .env file."