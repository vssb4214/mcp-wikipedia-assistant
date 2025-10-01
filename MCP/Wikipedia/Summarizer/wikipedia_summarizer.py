#!/usr/bin/env python3
"""
Wikipedia Summarizer with MCP Integration
Standalone Wikipedia summarization tool using Model Context Protocol.
"""

import os
import sys
import asyncio
import json
from dotenv import load_dotenv
from fastmcp import Client as MCPClient
from ollama import Client as OllamaClient

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
ollama_client = OllamaClient(host=OLLAMA_URL)

def print_marvin(msg):
    """Print messages with Marvin prefix"""
    print(f"[Marvin] {msg}")

async def list_tools():
    """List available Wikipedia MCP tools"""
    mcp_client = MCPClient({
        "mcpServers": {
            "wikipedia": {
                "command": "wikipedia-mcp"
            }
        }
    })
    async with mcp_client:
        tools = await mcp_client.list_tools()
    return tools

async def call_tool(tool_name, params):
    """Call a Wikipedia MCP tool"""
    mcp_client = MCPClient({
        "mcpServers": {
            "wikipedia": {
                "command": "wikipedia-mcp"
            }
        }
    })
    async with mcp_client:
        result = await mcp_client.call_tool(tool_name, params)
    return result

def pretty_print_tools(tools):
    """Pretty print available tools"""
    print("\nAvailable Wikipedia MCP Tools:")
    try:
        print(json.dumps(tools, indent=2, default=str))
    except Exception as e:
        print_marvin(f"Failed to pretty-print tools as JSON. Reason: {e}")
        print(tools)
    
    for idx, tool in enumerate(tools):
        # Try to get name and description
        name = getattr(tool, 'name', str(tool))
        desc = getattr(tool, 'description', None)
        if not desc and hasattr(tool, 'meta') and tool.meta and 'description' in tool.meta:
            desc = tool.meta['description']
        print(f"  {idx+1}. {name}")
        if desc:
            print(f"     - {desc}")
    print()

def get_tool_schema(tool):
    """Get tool schema information"""
    # Try to get inputSchema from tool object
    if hasattr(tool, 'inputSchema') and tool.inputSchema:
        return tool.inputSchema
    
    # Try to get schema from meta
    if hasattr(tool, 'meta') and tool.meta and 'inputSchema' in tool.meta:
        return tool.meta['inputSchema']
    
    return None

async def search_wikipedia(query: str):
    """Search Wikipedia for a topic"""
    try:
        result = await call_tool("search", {"query": query})
        return result
    except Exception as e:
        print_marvin(f"Error searching Wikipedia: {e}")
        return None

async def get_wikipedia_page(title: str):
    """Get a Wikipedia page by title"""
    try:
        result = await call_tool("get_page", {"title": title})
        return result
    except Exception as e:
        print_marvin(f"Error getting Wikipedia page: {e}")
        return None

async def summarize_with_ollama(text: str, model: str = "llama2"):
    """Summarize text using Ollama"""
    try:
        prompt = f"Please provide a concise summary of the following text:\n\n{text[:2000]}"
        
        response = ollama_client.generate(
            model=model,
            prompt=prompt,
            options={
                "temperature": 0.3,
                "top_p": 0.9,
                "max_tokens": 500
            }
        )
        
        return response['response']
    except Exception as e:
        print_marvin(f"Error with Ollama summarization: {e}")
        return None

async def main():
    """Main function for Wikipedia summarization"""
    print_marvin("Wikipedia Summarizer with MCP Integration")
    print_marvin("Loading Wikipedia tools...")
    
    try:
        # List available tools
        tools = await list_tools()
        pretty_print_tools(tools)
        
        # Interactive loop
        while True:
            query = input("\nEnter a Wikipedia topic to search (or 'quit' to exit): ").strip()
            
            if query.lower() in ['quit', 'exit', 'bye']:
                print_marvin("Goodbye!")
                break
            
            if not query:
                continue
            
            print_marvin(f"Searching for: {query}")
            
            # Search Wikipedia
            search_results = await search_wikipedia(query)
            if not search_results:
                print_marvin("No search results found")
                continue
            
            print_marvin("Search results:")
            print(json.dumps(search_results, indent=2, default=str))
            
            # Get the first result
            if isinstance(search_results, list) and len(search_results) > 0:
                first_result = search_results[0]
                title = first_result.get('title', query)
                
                print_marvin(f"Getting page: {title}")
                
                # Get the full page
                page_content = await get_wikipedia_page(title)
                if page_content:
                    print_marvin("Page content retrieved")
                    
                    # Summarize with Ollama
                    print_marvin("Generating summary...")
                    summary = await summarize_with_ollama(str(page_content))
                    
                    if summary:
                        print_marvin("Summary:")
                        print(f"\n{summary}\n")
                    else:
                        print_marvin("Failed to generate summary")
                else:
                    print_marvin("Failed to retrieve page content")
            else:
                print_marvin("No valid search results")
    
    except Exception as e:
        print_marvin(f"Error: {e}")
        return

if __name__ == "__main__":
    asyncio.run(main())