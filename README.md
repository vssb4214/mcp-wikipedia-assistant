# MCP Wikipedia Assistant

A comprehensive Wikipedia assistant built with Model Context Protocol (MCP) integration, featuring CloudNatix API support and Ollama summarization capabilities.

## Features

- **Wikipedia MCP Integration**: Direct access to Wikipedia tools via Model Context Protocol
- **CloudNatix API Support**: Advanced language model integration with tool calling
- **Ollama Summarization**: Local AI-powered text summarization
- **Interactive Chat Interface**: Natural conversation with Wikipedia knowledge
- **DuckDB Demo**: Database operations demonstration
- **Modular Architecture**: Separate components for different functionalities

## Project Structure

```
├── MCP/
│   ├── MCP/
│   │   ├── mcp_demo.py          # DuckDB demonstration
│   │   ├── create_sample_db.py  # Database setup
│   │   └── sample.db            # Sample database
│   └── Wikipedia/
│       ├── wikipedia_bot.py     # Main Wikipedia assistant
│       ├── config.py            # Configuration management
│       ├── setup.sh             # Setup script
│       ├── Summarizer/
│       │   ├── wikipedia_summarizer.py  # Ollama summarization
│       │   └── requirements.txt         # Dependencies
│       └── MCP-Server/          # MCP server configuration
└── README.md                    # This file
```

## Quick Start

### 1. Install Dependencies

For the main Wikipedia bot:
```bash
cd MCP/Wikipedia
pip install -r Summarizer/requirements.txt
```

### 2. Set Up API Keys

Create a `.env` file in the `MCP/Wikipedia` directory:
```bash
# CloudNatix API (optional - defaults provided)
CLOUDNATIX_API_KEY="your-api-key-here"

# Ollama Configuration
OLLAMA_URL="http://localhost:11434"
```

### 3. Start Wikipedia MCP Server

Ensure the Wikipedia MCP server is running:
```bash
wikipedia-mcp
```

### 4. Run the Assistant

```bash
python wikipedia_bot.py
```

## Usage Examples

### Wikipedia Bot
```bash
cd MCP/Wikipedia
python wikipedia_bot.py
```

Ask questions like:
- "Tell me about artificial intelligence"
- "What is the history of Paris?"
- "Explain quantum computing"

### Wikipedia Summarizer
```bash
cd MCP/Wikipedia/Summarizer
python wikipedia_summarizer.py
```

Interactive summarization of Wikipedia articles with Ollama.

### MCP Demo
```bash
cd MCP/MCP
python mcp_demo.py
```

Demonstrates database operations with DuckDB.

## Configuration

### CloudNatix API Settings
- `CLOUDNATIX_API_KEY`: Your CloudNatix API key
- `CLOUDNATIX_API_URL`: API endpoint (default: https://api.llm.cloudnatix.com/v1/chat/completions)
- `CLOUDNATIX_MODEL`: Model to use (default: Qwen-Qwen3-4B)
- `CLOUDNATIX_TEMPERATURE`: Temperature setting (default: 0.1)
- `CLOUDNATIX_MAX_TOKENS`: Max tokens (default: 8218)

### Ollama Settings
- `OLLAMA_URL`: Ollama server URL (default: http://localhost:11434)

## Components

### 1. Wikipedia Bot (`wikipedia_bot.py`)
- Interactive Wikipedia assistant
- CloudNatix API integration
- Tool calling support
- Real-time conversation

### 2. Wikipedia Summarizer (`wikipedia_summarizer.py`)
- Standalone summarization tool
- Ollama integration
- MCP Wikipedia access
- Interactive search and summarize

### 3. MCP Demo (`mcp_demo.py`)
- DuckDB database operations
- Sample AWS instances data
- Simple query demonstrations

## Dependencies

### Core Requirements
- `aiohttp>=3.8.0`: Async HTTP client
- `fastmcp>=0.1.0`: Model Context Protocol client
- `python-dotenv>=1.0.0`: Environment variable management

### Optional Dependencies
- `ollama`: Local AI model integration
- `duckdb`: Database operations

## Setup Scripts

### Wikipedia Setup
```bash
cd MCP/Wikipedia
chmod +x setup.sh
./setup.sh
```

### MCP Server Setup
```bash
cd MCP/Wikipedia/MCP-Server
# Follow the README in that directory
```

## API Integration

### CloudNatix API
The bot uses CloudNatix's tool calling API structure for MCP integration:
- Automatic tool discovery
- Function calling support
- Streaming responses
- Error handling

### Wikipedia MCP
Direct integration with Wikipedia MCP server:
- Search functionality
- Page retrieval
- Content extraction
- Real-time access

## Troubleshooting

### Common Issues

1. **Wikipedia MCP Server Not Running**
   ```bash
   # Install and start wikipedia-mcp
   npm install -g wikipedia-mcp
   wikipedia-mcp
   ```

2. **API Key Issues**
   - Check your `.env` file
   - Verify API key permissions
   - Test with default keys first

3. **Ollama Connection Issues**
   - Ensure Ollama is running: `ollama serve`
   - Check OLLAMA_URL in configuration
   - Verify model availability

### Debug Mode
Enable detailed logging by setting environment variables:
```bash
export DEBUG=1
export LOG_LEVEL=DEBUG
```

## Development

### Adding New Tools
1. Extend the MCP configuration
2. Add tool definitions in `config.py`
3. Implement tool calling logic
4. Update the conversation flow

### Custom Models
- Modify `CLOUDNATIX_MODEL` in config
- Update Ollama model in summarizer
- Adjust temperature and token settings

## License

This project is for educational and development purposes. Please respect API usage limits and terms of service.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Ensure MCP servers are running
4. Check API key configuration
