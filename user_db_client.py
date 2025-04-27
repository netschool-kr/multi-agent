# Translated from user_db_client.py citeturn0file0
# MCP client and LangGraph agent setup
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI  # using OpenAI GPT-4 model as an example
import os



async def main():
    # 1. Configure parameters to run the MCP server (UserService) process in STDIO mode
    server_params = StdioServerParameters(
        command="python",
        args=[svrpath]  # Path to the MCP server script
    )
    # 2. Connect to the MCP server with an STDIO client and start session
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize MCP session (exchange server metadata)
            await session.initialize()
            # 3. Load available tools from server (retrieve tool metadata)
            tools = await load_mcp_tools(session)
            # 4. Create a LangGraph agent with LLM model and tools
            model = ChatOpenAI(model="gpt-4")
            agent = create_react_agent(model, tools)
            # 5. Run agent with natural language query (agent invokes tools to generate response)
            query = {"messages": "What is the name of user with ID 1?"}
            result = await agent.ainvoke(query)
            # Print results
            for message in result["messages"]:
                print(message.content)

# Run in asynchronous context
if __name__ == "__main__":
    svrpath = "./user_db_server.py"
    asyncio.run(main())
