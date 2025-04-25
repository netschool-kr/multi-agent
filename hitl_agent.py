from dotenv import load_dotenv
load_dotenv()
import sqlite3
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver  # SQLite-based checkpoint
from utils import show_graph

# (For Postgres: from langgraph.checkpoint.postgres import PostgresSaver)

# 1. Define the state: using 'result' and 'approved' keys as example
from pydantic import BaseModel
from typing import Optional

class State(BaseModel):
    user_input: str                 # e.g. prompt or necessary input (no default means required)
    result: Optional[str] = None    # default None (no result yet)
    approved: bool = False          # default False (not approved yet)

# 2. Define step-by-step processing logic
def ai_decision(state: State) -> State:
    state.result = "Classification result: normal"
    state.approved = False
    print("AI decision completed:", state.result)
    return state


def human_review(state: State) -> State:
    """Human-in-the-loop step: present AI decision to the user for review and approval"""
    print(f"AI decision result: {state.result}")
    user_input = input("Do you approve this decision? (yes/no): ").strip().lower()
    if user_input == "yes":
        state.approved = True
        print(">> User approval completed")
    else:
        state.approved = False
        correction = input("Please enter the corrected result: ")
        state.result = correction
        state.approved = True
        print(">> User correction completed, result approved")
    return state


def final_step(state: State) -> State:
    if state.approved:
        print("Final result:", state.result)
    else:
        print("Final result not approved; terminating process.")
    return state

# 3. Construct the graph: add nodes and edges
builder = StateGraph(State)
builder.add_node("ai_decision", ai_decision)
builder.add_node("human_review", human_review)
builder.add_node("final_step", final_step)
builder.add_edge(START, "ai_decision")         # start -> AI decision
builder.add_edge("ai_decision", "human_review")  # AI decision -> human review
builder.add_edge("human_review", "final_step")   # human review -> final step
builder.add_edge("final_step", END)            # end

# 4. Configure checkpointer: using SQLite (':memory:' for in-memory DB, or specify file path)
conn = sqlite3.connect(":memory:", check_same_thread=False)  # connect to in-memory DB
checkpointer = SqliteSaver(conn)  # create SqliteSaver with the connection object
graph = builder.compile(checkpointer=checkpointer)
show_graph(graph)

# **Checkpoint initialization**: .setup() may be needed once for SQLite
try:
    checkpointer.setup()  # create tables when using PostgreSQL
except Exception:
    pass  # ignore if already initialized

# 5. Execute the graph with Human-in-the-loop (HITL)
thread_config = {"configurable": {"thread_id": "demo1"}}
print("=== Starting graph execution ===")
initial_state = {"user_input": "example user input", "result": None, "approved": False}

# Run up to human_review (expect pause at human_review)
for event in graph.stream(initial_state, thread_config, stream_mode="values"):
    print(event)
    # checkpoint is auto-saved after each node execution
    pass

# human_review step: waiting for user approval input

# Resume graph to execute remaining node(s) after human_review (final_step)
for event in graph.stream(None, thread_config, stream_mode="values"):
    pass  # execute final_step to output result
print("=== Graph execution finished ===")
