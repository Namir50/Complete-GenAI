from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient

# Load TAVILY_API_KEY from .env
load_dotenv()

mcp = FastMCP("Weather")
tavily_search = TavilyClient()

@mcp.tool()
def get_weather(location: str) -> str:
    """Get the current weather for a given location"""
    return tavily_search.qna_search(query=f"current weather in {location}") #here we are doing qna_search as it returns clean string instead of dict with metadata

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
