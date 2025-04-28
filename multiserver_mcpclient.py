import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
# from src_langgraph.utils import show_graph

# Load environment variables from .env file
load_dotenv()
if os.environ.get("EXEC_ENV") == "vscode":
    # If running inside VSCode (base: src folder)
    server_script_path = "./"
    python_command = "C:\\Users\\user\\anaconda3\\envs\\langgraph-mcp\\python.exe"
else:
    # If running from a DOS shell (base: project root)
    server_script_path = "./"
    python_command = "python"
# Example queries:
# "What is weather in newyork"
# "What is FastMCP?"
# "summarize this youtube video in 50 words, here is a video link: https://www.youtube.com/watch?v=2f3K43FHRKo"
query = input("Query:")

# Define LLM
model = ChatOpenAI(model="gpt-4o")

# Define and run MCP-connected agent
async def run_agent():
    async with MultiServerMCPClient(
        {
            "tavily": {
                "command": python_command,
                "args": [server_script_path + "tavily_search.py"],
                "transport": "stdio",
            },
            "youtube_transcript": {
                "command": python_command,
                "args": [server_script_path + "yt_transcript.py"],
                "transport": "stdio",
            },
            "news_extractor": {
                "command": python_command,
                "args": [server_script_path + "news_mcp_server.py"],
                "transport": "stdio",
            },
            "elevenlabs": {
                "command": python_command,
                "args": [server_script_path + "elevenlabs_mcp_server.py"],
                "transport": "stdio",
            },
        }
    ) as client:
        # Load available tools
        tools = client.get_tools()
        agent = create_react_agent(model, tools)
        # show_graph(agent)
        # Add system message
        system_message = SystemMessage(content=(
            "You have access to multiple tools that can help answer queries. "
            "Use them dynamically and efficiently based on the user's request. "
        ))

        # Process the query
        agent_response = await agent.ainvoke({"messages": [system_message, HumanMessage(content=query)]})

        # Print each message for debugging
        for m in agent_response["messages"]:
            m.pretty_print()

        # Handle the final response
        final_message = agent_response["messages"][-1]
        response_content = final_message.content

        # Check if the response indicates audio file saved (from ElevenLabs)
        try:
            if isinstance(response_content, dict) and response_content.get("status") == "success" and "message" in response_content:
                return response_content["message"]  # e.g., "Audio saved on server as output_xxx.mp3"
            else:
                return response_content
        except Exception as e:
            return f"Error processing response: {str(e)}"

# Run the agent
if __name__ == "__main__":
    response = asyncio.run(run_agent())
    print("\nFinal Response:", response)
