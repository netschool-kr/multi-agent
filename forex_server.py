# forex_server.py - Mock Forex MCP Server using FastMCP
from mcp.server.fastmcp import FastMCP

# Create an MCP server instance
mcp = FastMCP("ForexServer")

# Define an MCP tool for fetching exchange rates (mock implementation)
@mcp.tool()
def get_rate(pair: str = "EUR/USD") -> float:
    """Return the current exchange rate for the given currency pair (mock data)."""
    import random
    # Generate a mock EUR/USD rate between 0.95 and 1.05
    rate = round(random.uniform(0.95, 1.05), 4)
    print(f"[MCP] {pair} rate = {rate}")
    return rate

if __name__ == "__main__":
    # Run the MCP server over stdio transport
    mcp.run(transport="stdio")
