# Wikipedia MCP + CloudNatix API Integration

Simple Wikipedia assistant using CloudNatix API with MCP (Model Context Protocol) tools.

## Setup

1. **Install dependencies:**
```bash
pip install -r Summarizer/requirements.txt
```

2. **Set your CloudNatix API key (optional):**
```bash
export CLOUDNATIX_API_KEY="your-api-key-here"
```
*Note: A default API key is provided in the configuration, but you can override it with your own.*

3. **Ensure Wikipedia MCP server is running:**
```bash
wikipedia-mcp
```

## Usage

Run the interactive assistant:
```bash
python wikipedia_bot.py
```

Ask questions about Wikipedia topics and the bot will use MCP tools to fetch information.

## Configuration

Environment variables in `.env` file:
- `CLOUDNATIX_API_KEY` - Your CloudNatix API key (optional, defaults to provided key)
- `CLOUDNATIX_API_URL` - API endpoint (default: https://api.llm.cloudnatix.com/v1/chat/completions)
- `CLOUDNATIX_MODEL` - Model to use (default: Qwen-Qwen3-4B)
- `CLOUDNATIX_TEMPERATURE` - Temperature setting (default: 0.1)
- `CLOUDNATIX_MAX_TOKENS` - Max tokens (default: 8218)
- `CLOUDNATIX_TOP_P` - Top-p sampling (default: 0.9)
- `CLOUDNATIX_FREQUENCY_PENALTY` - Frequency penalty (default: 0.3)
- `CLOUDNATIX_PRESENCE_PENALTY` - Presence penalty (default: 0.5)

## Files

- `wikipedia_bot.py` - Main bot script
- `config.py` - Configuration management
- `Summarizer/requirements.txt` - Python dependencies

The implementation follows CloudNatix's tool calling API structure for MCP integration. 