import asyncio
import sys
sys.path.append('.')
from fastmcp import FastMCP

async def test():
    mcp = FastMCP('test')
    
    # Add a simple tool to test
    @mcp.tool()
    def hello(name: str) -> str:
        return f"Hello, {name}!"
    
    tools = await mcp.get_tools()
    print(f"Tools type: {type(tools)}")
    print(f"Tools: {tools}")
    if tools:
        # Tools is a dict, get the first key
        first_key = list(tools.keys())[0]
        tool = tools[first_key]
        print(f"First tool type: {type(tool)}")
        print(f"First tool attributes: {dir(tool)}")
        # Check if it has name and description attributes
        if hasattr(tool, 'name'):
            print(f"Tool name: {tool.name}")
        if hasattr(tool, 'description'):
            print(f"Tool description: {tool.description}")

if __name__ == "__main__":
    asyncio.run(test())