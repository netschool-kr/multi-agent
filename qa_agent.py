from pydantic import BaseModel
from utils import show_graph

# Define the shared state model for the entire agent system
class QAState(BaseModel):
    query: str        # user's query
    info: str = ""    # intermediate information (e.g., summary of search results)
    answer: str = ""  # final answer

# 1. Information Retrieval Agent Node
def research_agent(state: QAState):
    """Agent that receives the user's query and retrieves relevant information"""
    query = state.query
    # (Here, we assume an external search and hardcode the result)
    result = f"Relevant data for '{query}'"
    # Save the search result in the state's info field and return it
    return {"info": result}

# 2. Answer Generation Agent Node
def answer_agent(state: QAState):
    """Agent that generates the final answer based on the collected information"""
    info_text = state.info
    if info_text:
        answer_text = f"Answer to '{state.query}': {info_text}"
    else:
        answer_text = "Sorry, I could not find any relevant information."
    # Save the generated answer in the state's answer field and return it
    return {"answer": answer_text}

from langgraph.graph import StateGraph, START, END

# Create a graph builder with QAState as the state model
builder = StateGraph(QAState)
# Add nodes (register function and name)
builder.add_node("research_agent", research_agent)
builder.add_node("answer_agent", answer_agent)
# Add edges: start -> research agent -> answer agent -> end
builder.add_edge(START, "research_agent")
builder.add_edge("research_agent", "answer_agent")
builder.add_edge("answer_agent", END)

# Compile the graph
graph = builder.compile()
show_graph(graph)

# Example graph execution
initial_state = {"query": "Advantages of LangGraph"}  # initial state dictionary
final_state = graph.invoke(initial_state)             # invoke the graph
print(final_state["answer"])                          # print the answer from the final state
