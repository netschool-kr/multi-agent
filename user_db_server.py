# Translated from user_db_server.py citeturn1file0
from mcp.server.fastmcp import FastMCP

# Create an MCP server named "UserDBService"
mcp = FastMCP("UserDBService")

# Register a tool that maps user ID to name
@mcp.tool()
def get_user_name(user_id: int) -> str:
    """Return the name corresponding to the given user ID."""
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id, f"Unknown user (ID: {user_id})")

if __name__ == "__main__":
    # Run the MCP server over standard IO for inter-process communication on the same machine
    mcp.run(transport="stdio")
