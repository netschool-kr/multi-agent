# ecommerce_service_server.py - MCP Server Setup (Product Recommendation & Inventory Check Service)
from mcp.server.fastmcp import FastMCP

# Create an MCP server named "ECommerceService"
mcp = FastMCP("ECommerceService")

# Simple product database (ID: {name, category, price, stock})
PRODUCT_DB = {
    1: {"name": "Gaming Laptop X", "category": "Laptop", "price": 950, "stock": 5},
    2: {"name": "Business Laptop Y", "category": "Laptop", "price": 850, "stock": 0},
    3: {"name": "Smartphone A",    "category": "Smartphone", "price": 700, "stock": 10},
    4: {"name": "Gaming Mouse Z",  "category": "Accessory",   "price": 50,  "stock": 100}
}

@mcp.tool()
def recommend_products(query: str) -> list:
    """Return a list of products recommended based on the user's query."""
    results = []
    query_lower = query.lower()
    # Example filtering: "laptop", "cheap", etc.
    for pid, info in PRODUCT_DB.items():
        name     = info["name"]
        price    = info["price"]
        category = info["category"].lower()
        # Match category keywords
        if ("laptop" in query_lower and category == "laptop") or \
           ("smartphone" in query_lower and category == "smartphone"):
            # Price condition: if "cheap" or "under" mentioned, filter by price <=1000
            if "cheap" in query_lower or "affordable" in query_lower or "under" in query_lower:
                if price <= 1000:
                    results.append({"id": pid, "name": name, "price": price})
            else:
                results.append({"id": pid, "name": name, "price": price})
    # Return up to 3 recommendations
    return results[:3]

@mcp.tool()
def check_inventory(product_id: int) -> str:
    """Return the inventory status for the given product ID."""
    product = PRODUCT_DB.get(product_id)
    if product is None:
        return f"Product ID {product_id} not found."
    stock = product["stock"]
    if stock > 0:
        return f"{stock} items in stock"
    else:
        return "Out of stock"

if __name__ == "__main__":
    # Run MCP server over stdio (prepare for client communication in the same process)
    mcp.run(transport="stdio")
