# chatbot_server.py - MCP Server: Define Web Search and Answer Generation Tools
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file (should include OPENAI_API_KEY, SERPAPI_API_KEY, etc.)
load_dotenv(find_dotenv())
openai_api_key = os.getenv('OPENAI_API_KEY')
serpapi_api_key = os.getenv('SERPAPI_API_KEY')

# Set OpenAI API key
import openai
openai.api_key = openai_api_key

# Import MCP server and tool decorator
from mcp.server.fastmcp import FastMCP

# Import SerpAPI wrapper for search (using LangChain)
from langchain_community.utilities import SerpAPIWrapper

# Initialize SerpAPI search tool (uses SERPAPI_API_KEY from env)
search_tool_api = SerpAPIWrapper()

# Create MCP server instance (service name: "ChatbotService")
mcp = FastMCP("ChatbotService")

# Tool definition: web search functionality
@mcp.tool()
def search_web(query: str) -> str:
    """Perform a web search for the given query and return results as a string."""
    try:
        result = search_tool_api.run(query)
    except Exception as e:
        result = f"(Error occurred during search: {e})"
    return result

# Tool definition: answer generation functionality
@mcp.tool()
def generate_answer(query: str, search_results: str) -> str:
    """Generate an answer using the user’s query and search information."""
    # Construct user prompt
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
        # Call OpenAI ChatCompletion API to generate the answer (default model: gpt-3.5-turbo)
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        answer_text = completion.choices[0].message.content
    except Exception as e:
        answer_text = f"An error occurred while generating the answer: {e}"
    return answer_text

if __name__ == "__main__":
    # Run MCP server (using stdio transport)
    mcp.run(transport="stdio")
