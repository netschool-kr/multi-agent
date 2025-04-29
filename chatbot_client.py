# chatbot_client.py - LangGraph Client: Integrating MCP Tools with Conversational Agent
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated
import operator

# Define the structure of the state data
class State(TypedDict):
    user_input: str                                      # User's question
    search_results: Annotated[List[str], operator.add]   # List of search results (accumulatable)
    final_answer: str                                    # Final answer

def decide_next_step(state: State) -> dict:
    """Analyze the user's question to decide the next step between 'search' and 'answer'."""
    query = state["user_input"].lower()
    # Prioritize search if specific keywords are included in the query
    NEED_SEARCH_KEYWORDS = ["weather", "today", "tomorrow", "yesterday", "current", "search"]
    if any(keyword in query for keyword in NEED_SEARCH_KEYWORDS):
        return {"route": "search"}   # Branch to search node
    else:
        return {"route": "answer"}   # Branch directly to answer generation node

import os

if os.environ.get("EXEC_ENV") == "vscode":
    # When running inside VSCode (based on src folder)
    server_script = "./chatbot_server.py"
    python_command = "C:\\Users\\user\\anaconda3\\envs\\langgraph-mcp\\python.exe"
else:
    # When running in a DOS terminal (based on root directory)
    server_script = "./chatbot_server.py"
    python_command = "python"

async def main():
    # 1. Start MCP server process in STDIO mode (specify server script path)
    server_params = StdioServerParameters(command=python_command, args=[server_script])
    # 2. Connect to the MCP server and start a session
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # 3. Load the list of available tools from the server
            tools = await load_mcp_tools(session)
            #    Select necessary tools from the loaded list
            search_tool = next(t for t in tools if t.name == "search_web")
            answer_tool = next(t for t in tools if t.name == "generate_answer")
            # 4. Define graph node functions (implement remote MCP tool calls)
            async def search_node(state: State) -> dict:
                query = state["user_input"]
                try:
                    result_str = await search_tool.ainvoke({"query": query})
                except Exception as e:
                    result_str = f"(Error occurred during search: {e})"
                return {"search_results": [result_str]}
            
            async def answer_node(state: State) -> dict:
                query = state["user_input"]
                # Combine previous search results into a single string
                search_info = "\n".join(state.get("search_results", []))
                try:
                    answer_text = await answer_tool.ainvoke({
                        "query": query,
                        "search_results": search_info
                    })
                except Exception as e:
                    answer_text = f"An error occurred while generating the answer: {e}"
                return {"final_answer": answer_text}
            
            # 5. Create the state graph and add nodes
            graph = StateGraph(State)
            graph.add_node("router", decide_next_step)    # Router node
            graph.add_node("search_node", search_node)     # Search node
            graph.add_node("answer_node", answer_node)     # Answer generation node
            # 6. Set up edges between nodes (conditional branching and sequential flow)
            graph.add_edge(START, "router")
            graph.add_conditional_edges(
                "router",
                lambda state: state["route"],
                {"search": "search_node", "answer": "answer_node"}
            )
            graph.add_edge("search_node", "answer_node")
            graph.add_edge("answer_node", END)
            graph = graph.compile()
            # 7. Example graph execution
            user_question = "What will the weather be like in Seoul tomorrow?"
            initial_state = {"user_input": user_question}
            result_state = await graph.ainvoke(initial_state)
            # 8. Output the results
            print("Question:", user_question)
            print("Search results summary:", result_state.get("search_results"))
            print("Answer:", result_state.get("final_answer"))

# Execute the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())
