import os
from fastmcp import FastMCP
import sys
import asyncio
from fastapi.middleware.cors import CORSMiddleware
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capabilities import setup_capabilities

# Create MCP server
mcp = FastMCP("RAG MCP Server")


# Register capabilities
setup_capabilities(mcp)

async def show_tools():
    """Display available tools"""
    print("RAG MCP Server - Use with --stdio flag for MCP communication")
    print("Available tools:")
    tools = await mcp.get_tools()
    for tool_name, tool in tools.items():
        print(f"  - {tool.name}: {tool.description or 'No description'}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        asyncio.run(mcp.run())
    else:
        mcp.run(transport="http", port=8000, path="/mcp")
