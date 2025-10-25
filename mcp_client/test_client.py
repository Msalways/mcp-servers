import sys
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

async def main():
    client = MultiServerMCPClient({
        "rag_server": {
            "transport": "streamable_http",
            "url": "http://localhost:8000/mcp"
        }
    })

    tools = await client.get_tools()
    print(f"Retrieved tools: {tools}")

    # Test embedding text
    print("\n--- Testing embed_text tool ---")
    embed_tool = next((t for t in tools if t.name == "embed_text"), None)
    if embed_tool:
        result = await embed_tool.ainvoke({"text_content": "This is a test document about artificial intelligence and machine learning.", "title": "AI Test Doc", "namespace": "test"})
        print(f"Embed result: {result}")
    else:
        print("embed_text tool not found")

    # Test querying
    print("\n--- Testing query_all_docs tool ---")
    query_tool = next((t for t in tools if t.name == "query_all_docs"), None)
    if query_tool:
        result = await query_tool.ainvoke({"query": "artificial intelligence", "k": 5})
        print(f"Query result: {result}")
    else:
        print("query_all_docs tool not found")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
