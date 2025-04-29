from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

import os

# Configure server script path and Python command based on execution environment
if os.environ.get("EXEC_ENV") == "vscode":
    # If running in VSCode (relative to src folder)
    server_script = "./forex_server.py"
    python_command = "C:\\Users\\user\\anaconda3\\envs\\langgraph-mcp\\python.exe"
else:
    # If running in a DOS terminal (root directory)
    server_script = "./forex_server.py"
    python_command = "python"

# 1. Define the state structure
class ForexState(TypedDict):
    pair: str
    prices: list[float]
    short_window: int
    long_window: int
    short_ma: float
    long_ma: float
    signal: str  # "BUY", "SELL", or "HOLD"

# 2. Implement node functions
def fetch_rate_node(state: ForexState) -> ForexState:
    """Fetch the current exchange rate via MCP tool and update the state."""
    pair = state["pair"]
    try:
        # Invoke the MCP get_rate tool synchronously
        result = asyncio.run(fetch_rate_via_mcp(pair))
        state["prices"].append(result)
        # Maintain rolling window
        if len(state["prices"]) > state["long_window"]:
            state["prices"].pop(0)
    except Exception as e:
        print(f"MCP fetch error: {e}")
    return state

def compute_ma_node(state: ForexState) -> ForexState:
    """Compute short-term and long-term moving averages."""
    prices = state["prices"]
    sw, lw = state["short_window"], state["long_window"]
    # Short moving average
    if len(prices) >= sw:
        state["short_ma"] = sum(prices[-sw:]) / sw
    else:
        state["short_ma"] = sum(prices) / len(prices) if prices else 0.0
    # Long moving average
    if len(prices) >= lw:
        state["long_ma"] = sum(prices[-lw:]) / lw
    else:
        state["long_ma"] = sum(prices) / len(prices) if prices else 0.0
    return state

def signal_check_node(state: ForexState) -> ForexState:
    """Determine BUY, SELL, or HOLD signal based on MA crossover."""
    short_ma = state["short_ma"]
    long_ma = state["long_ma"]
    if short_ma > long_ma:
        state["signal"] = "BUY"
    elif short_ma < long_ma:
        state["signal"] = "SELL"
    else:
        state["signal"] = "HOLD"
    return state

def send_email_node(state: ForexState) -> ForexState:
    """Send an email alert when a BUY or SELL signal is generated."""
    import smtplib
    from email.message import EmailMessage

    # Load SMTP credentials and alert address from environment
    smtp_user = os.getenv("GMAIL_USER")
    smtp_pass = os.getenv("GMAIL_PASS")
    alert_to  = os.getenv("ALERT_EMAIL", smtp_user)  # Default to self if not set
    if not smtp_user or not smtp_pass:
        print("⚠️ SMTP credentials for sending email are not configured.")
        return state

    # Compose email
    msg = EmailMessage()
    pair  = state["pair"]
    price = state["prices"][-1] if state["prices"] else None
    signal = state["signal"]

    msg["Subject"] = f"[Forex Signal] {pair} - {signal}"
    msg["From"]    = smtp_user
    msg["To"]      = alert_to
    body = (
        f"Trading signal for {pair}: {signal}\n"
        f"Latest price = {price}\n"
        f"Short MA = {state['short_ma']}, Long MA = {state['long_ma']}"
    )
    msg.set_content(body)

    # Send via Gmail SMTP
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email alert sent: {signal} @ price {price}")
    except Exception as e:
        print(f"❌ Email send failed: {e}")
    return state

# 3. Build the workflow graph and configure edges
workflow = StateGraph(ForexState)
workflow.add_node("fetch_rate",    fetch_rate_node)
workflow.add_node("compute_ma",    compute_ma_node)
workflow.add_node("signal_check",  signal_check_node)
workflow.add_node("send_email",    send_email_node)

# Sequence: START → fetch_rate → compute_ma → signal_check
workflow.add_edge(START, "fetch_rate")
workflow.add_edge("fetch_rate", "compute_ma")
workflow.add_edge("compute_ma", "signal_check")

# Conditional routing after signal_check
def route_signal_edge(state: ForexState) -> str:
    """Return 'ALERT' if the signal is BUY or SELL, otherwise 'NO_ALERT'."""
    return "ALERT" if state["signal"] in ("BUY", "SELL") else "NO_ALERT"

workflow.add_conditional_edges(
    "signal_check",
    route_signal_edge,
    {"ALERT": "send_email", "NO_ALERT": END}
)
workflow.add_edge("send_email", END)

# Compile the graph into an executable agent
agent = workflow.compile()

# MCP connection parameters for forex_server.py subprocess
server_params = StdioServerParameters(
    command=python_command,
    args=[server_script],
)

async def fetch_rate_via_mcp(pair: str) -> float:
    """Helper to invoke the get_rate MCP tool and return its result."""
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            get_rate = next(t for t in tools if t.name == "get_rate")
            return await get_rate.ainvoke({"pair": pair})

# Example execution
pair = "EUR/USD"
rate = asyncio.run(fetch_rate_via_mcp(pair))
print(f"Current exchange rate for {pair}: {rate}")

import random
random.seed(42)  # Fix seed for reproducibility

# Initialize agent state
state: ForexState = {
    "pair": "EUR/USD",
    "prices": [],
    "short_window": 3,
    "long_window": 5,
    "short_ma": 0.0,
    "long_ma": 0.0,
    "signal": "HOLD"
}

# Run the workflow for 10 iterations
for i in range(1, 11):
    print(f"\n=== Iteration {i} ===")
    state = agent.invoke(state)  # Execute graph
    latest_price = state["prices"][-1]
    print(f"New price = {latest_price}")
    print(f"Short MA (window={state['short_window']}) = {state['short_ma']}")
    print(f"Long  MA (window={state['long_window']}) = {state['long_ma']}")
    print(f"Signal = {state['signal']}")
