# chatbot_server_sse.py - MCP Server: Define Web Search and Answer Generation Tools via SSE
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables (OPENAI_API_KEY, SERPAPI_API_KEY, etc.) from .env file
load_dotenv(find_dotenv())
openai_api_key = os.getenv('OPENAI_API_KEY')
serpapi_api_key = os.getenv('SERPAPI_API_KEY')

# Set OpenAI API key
import openai
openai.api_key = openai_api_key

# Import FastMCP and SerpAPIWrapper
from mcp.server.fastmcp import FastMCP
from langchain_community.utilities import SerpAPIWrapper

# Initialize SerpAPI search wrapper
search_tool_api = SerpAPIWrapper()

# Create MCP server instance (service name: ChatbotService)
mcp = FastMCP("ChatbotService")

# [1] Register web search tool
@mcp.tool()
def search_web(query: str) -> str:
    """Perform a web search for the given query and return the results as a string."""
    try:
        result = search_tool_api.run(query)
    except Exception as e:
        result = f"(Error occurred during search: {e})"
    return result

# [2] Register answer generation tool
@mcp.tool()
def generate_answer(query: str, search_results: str) -> str:
    """Generate an answer using the user's query and search data."""
    if search_results and search_results.strip():
        user_content = (
            f"User question: {query}\n\n"
            f"Here are the web search results:\n{search_results}\n\n"
            "Please use this information to answer the question."
        )
    else:
        user_content = f"User question: {query}"
    system_content = (
        "You are an intelligent assistant that answers questions through multiple steps. "
        "Please respond as accurately and concisely as possible."
    )
    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]
    try:
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        answer_text = completion.choices[0].message.content
    except Exception as e:
        answer_text = f"An error occurred while generating the answer: {e}"
    return answer_text

# --- Configure SSE server (using FastAPI) ---
from fastapi import FastAPI, Request, HTTPException
from sse_starlette.sse import EventSourceResponse
import asyncio

app = FastAPI()

@app.post("/sse")
async def sse_invoke(request: Request):
    """
    Receive a JSON POST from the client containing the tool name and parameters,
    invoke the corresponding MCP tool, and send the result as an SSE event.
    """
    payload = await request.json()
    tool_name = payload.get("tool")
    params = payload.get("params", {})
    if not tool_name:
        raise HTTPException(status_code=400, detail="tool parameter is required")
    
    # Invoke MCP tool based on tool_name (additional tools can be registered as needed)
    if tool_name == "search_web":
        result = search_web(**params)
    elif tool_name == "generate_answer":
        result = generate_answer(**params)
    else:
        result = f"Unknown tool: {tool_name}"
    
    async def event_generator():
        # Send one line in 'data: <content>' format according to SSE protocol, then end
        yield f"data: {result}\n\n"
        await asyncio.sleep(0.1)
    
    return EventSourceResponse(event_generator())

# Run FastAPI server (using uvicorn)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
