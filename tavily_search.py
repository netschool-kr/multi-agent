# tavily_search.py
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
from dotenv import load_dotenv, find_dotenv

# Load TAVILY_API_KEY, SERPAPI_API_KEY, etc. from .env file
load_dotenv(find_dotenv())
# Set Tavily API key (via environment variables or .env)
api_key = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=api_key)

# Create a FastMCP server instance (service name: "WebSearchService")
mcp = FastMCP("WebSearchService")

# Define and register the web search tool
@mcp.tool()
def search_web(query: str) -> str:
    """Summarize and return the latest web search results for the given query."""
    try:
        response = tavily_client.search(query)  # Execute web search via Tavily API
        # Use direct answer from Tavily response if available, otherwise use result content
        if isinstance(response, dict):
            if "answer" in response and response["answer"]:
                return response["answer"]
            if "results" in response and response["results"]:
                top = response["results"][0]  # Use the first result
                return f"{top.get('title')}: {top.get('content')}"
        # If the response isn't a dict or has no processable content, convert to string
        return str(response)
    except Exception as e:
        return f"(Search error: {e})"

if __name__ == "__main__":
    mcp.run(transport="stdio")
