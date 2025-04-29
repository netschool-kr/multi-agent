# ecommerce_agent_client.py - MCP Client and LangGraph Agent Setup
import os
from dotenv import load_dotenv, find_dotenv

# Load OPENAI_API_KEY from .env file
load_dotenv(find_dotenv())
openai_api_key = os.getenv('OPENAI_API_KEY')

# Configure OpenAI API key
import openai
openai.api_key = openai_api_key

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI  # OpenAI GPT-4 model (LangChain OpenAI wrapper)
from utils import show_graph

# Set paths based on execution environment
if os.environ.get("EXEC_ENV") == "vscode":
    # If running in VSCode (relative to src folder)
    server_script = "./ecommerce_service_server.py"
    python_command = "C:\\Users\\user\\anaconda3\\envs\\langgraph-mcp\\python.exe"
else:
    # If running in a DOS terminal (root directory)
    server_script = "./ecommerce_service_server.py"
    python_command = "python"

async def main():
    # 1. Set parameters to run MCP server process in STDIO mode
    server_params = StdioServerParameters(
        command=python_command,
        args=[server_script]  # Path to MCP server script
    )
    # 2. Connect to MCP server as STDIO client and start session
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 3. Initialize MCP session (exchange initial metadata with server)
            await session.initialize()
            # 4. Load list of available tools from the server
            tools = await load_mcp_tools(session)
            # 5. Create a LangGraph agent with LLM model and tools
            model = ChatOpenAI(model="gpt-4")  # OpenAI GPT-4 model instance (requires API key)
            agent = create_react_agent(model, tools)
            show_graph(agent)
            # 6. Handle user query using the agent
            query = {"messages": "Recommend an inexpensive laptop that is in stock." }
            result = await agent.ainvoke(query)
            # 7. Print the results
            for message in result["messages"]:
                print(message.content)

# Execute the async function
if __name__ == "__main__":
    asyncio.run(main())
