#!/usr/bin/env python3
"""
Wikipedia MCP Bot with CloudNatix API Integration
Interactive Wikipedia assistant using Model Context Protocol (MCP) tools.
"""

import json
import asyncio
import aiohttp
from typing import List, Dict, Any
from fastmcp import Client as MCPClient
from config import (
    CLOUDNATIX_API_KEY, CLOUDNATIX_API_URL, CLOUDNATIX_MODEL, 
    CLOUDNATIX_TEMPERATURE, CLOUDNATIX_MAX_TOKENS, CLOUDNATIX_TOP_P,
    CLOUDNATIX_FREQUENCY_PENALTY, CLOUDNATIX_PRESENCE_PENALTY,
    SYSTEM_PROMPT, WIKIPEDIA_MCP_CONFIG
)

def print_marvin(msg):
    """Print messages with Marvin prefix"""
    print(f"[Marvin] {msg}")

def log_messages(messages: List[Dict[str, Any]], context: str = ""):
    """Log the messages being sent to CloudNatix API"""
    print(f"\n{'='*60}")
    print(f"[Marvin] Messages being sent to CloudNatix {context}:")
    print(f"{'='*60}")
    
    for i, message in enumerate(messages, 1):
        role = message.get("role", "unknown")
        content = message.get("content", "")
        
        print(f"\n--- Message {i} [{role.upper()}] ---")
        
        if role == "system":
            print(f"Content: {content[:100]}{'...' if len(content) > 100 else ''}")
        elif role == "user":
            print(f"Content: {content}")
        elif role == "assistant":
            print(f"Content: {content}")
            if "tool_calls" in message:
                tool_calls = message["tool_calls"]
                print(f"Tool Calls ({len(tool_calls)}):")
                for tc in tool_calls:
                    print(f"  - {tc.get('function', {}).get('name', 'unknown')}({tc.get('function', {}).get('arguments', {})})")
        elif role == "tool":
            print(f"Tool Call ID: {message.get('tool_call_id', 'unknown')}")
            print(f"Result: {content[:200]}{'...' if len(content) > 200 else ''}")
    
    print(f"{'='*60}\n")

async def get_wikipedia_tools() -> List[Dict[str, Any]]:
    """Get Wikipedia tools from MCP server in CloudNatix format"""
    try:
        mcp_client = MCPClient(WIKIPEDIA_MCP_CONFIG)
        async with mcp_client:
            tools = await mcp_client.list_tools()
        
        # Convert MCP tools to CloudNatix format
        cloudnatix_tools = []
        for tool in tools:
            tool_schema = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema if hasattr(tool, 'inputSchema') else {}
                }
            }
            cloudnatix_tools.append(tool_schema)
        
        return cloudnatix_tools
    except Exception as e:
        print_marvin(f"Error getting Wikipedia tools: {e}")
        return []

async def call_wikipedia_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Call a Wikipedia tool via MCP"""
    try:
        mcp_client = MCPClient(WIKIPEDIA_MCP_CONFIG)
        async with mcp_client:
            result = await mcp_client.call_tool(tool_name, arguments)
        return str(result)
    except Exception as e:
        return f"Error calling tool {tool_name}: {e}"

async def chat_with_cloudnatix(messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Send messages to CloudNatix API with tool calling support"""
    headers = {
        "Authorization": f"Bearer {CLOUDNATIX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": CLOUDNATIX_MODEL,
        "messages": messages,
        "tools": tools,
        "tool_choice": "auto",
        "temperature": CLOUDNATIX_TEMPERATURE,
        "max_tokens": CLOUDNATIX_MAX_TOKENS,
        "top_p": CLOUDNATIX_TOP_P,
        "frequency_penalty": CLOUDNATIX_FREQUENCY_PENALTY,
        "presence_penalty": CLOUDNATIX_PRESENCE_PENALTY
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(CLOUDNATIX_API_URL, headers=headers, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_text = await response.text()
                print_marvin(f"API Error {response.status}: {error_text}")
                return {"error": f"API Error {response.status}: {error_text}"}

async def process_tool_calls(response: Dict[str, Any], messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Process tool calls from the API response"""
    if "choices" not in response or not response["choices"]:
        return messages
    
    choice = response["choices"][0]
    message = choice["message"]
    
    # Add assistant message to conversation
    messages.append(message)
    
    # Check for tool calls
    if "tool_calls" in message and message["tool_calls"]:
        print_marvin("Processing tool calls...")
        
        for tool_call in message["tool_calls"]:
            function_name = tool_call["function"]["name"]
            function_args = json.loads(tool_call["function"]["arguments"])
            
            print_marvin(f"Calling tool: {function_name} with args: {function_args}")
            
            # Call the Wikipedia tool
            tool_result = await call_wikipedia_tool(function_name, function_args)
            
            # Add tool result to messages
            tool_message = {
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": tool_result
            }
            messages.append(tool_message)
        
        # Get final response after tool calls
        final_response = await chat_with_cloudnatix(messages, [])
        if "choices" in final_response and final_response["choices"]:
            final_message = final_response["choices"][0]["message"]
            messages.append(final_message)
    
    return messages

async def main():
    """Main conversation loop"""
    print_marvin("Starting Wikipedia MCP Bot with CloudNatix API")
    print_marvin("Loading Wikipedia tools...")
    
    # Get available tools
    tools = await get_wikipedia_tools()
    if not tools:
        print_marvin("No Wikipedia tools available. Make sure wikipedia-mcp is running.")
        return
    
    print_marvin(f"Loaded {len(tools)} Wikipedia tools")
    
    # Initialize conversation
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    print_marvin("Ready! Ask me anything about Wikipedia topics.")
    print_marvin("Type 'quit' to exit.")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print_marvin("Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Add user message
            messages.append({"role": "user", "content": user_input})
            
            # Log messages being sent
            log_messages(messages, "initial request")
            
            # Send to CloudNatix API
            response = await chat_with_cloudnatix(messages, tools)
            
            if "error" in response:
                print_marvin(f"Error: {response['error']}")
                continue
            
            # Process tool calls if any
            messages = await process_tool_calls(response, messages)
            
            # Get the final response
            if messages and messages[-1]["role"] == "assistant":
                final_content = messages[-1]["content"]
                print_marvin(f"Response: {final_content}")
            else:
                print_marvin("No response received")
            
        except KeyboardInterrupt:
            print_marvin("\nGoodbye!")
            break
        except Exception as e:
            print_marvin(f"Error: {e}")
            continue

if __name__ == "__main__":
    asyncio.run(main())