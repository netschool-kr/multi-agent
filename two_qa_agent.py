from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from utils import show_graph

# Define the state model
class QAState(BaseModel):
    query: str
    info: str = ""
    answer: str = ""

# Define node functions
def research_agent(state: QAState):
    """Agent that retrieves information for the given query"""
    # (Here, respond with simple hardcoded values)
    state_query = state.query
    # For example, assume returning pre-prepared information based on the query
    if "LangGraph" in state_query and "LangChain" in state_query:
        found = "LangGraph is an agent workflow extension framework for LangChain."
    else:
        found = "No relevant information found."
    return {"info": found}

def answer_agent(state: QAState):
    """Agent that generates the final answer based on the collected information"""
    info_text = state.info
    if "No relevant information found." in info_text:
        answer_text = f"Unable to find an answer for the
