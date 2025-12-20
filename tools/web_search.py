import os
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Check if TAVILY_API_KEY exists
if not os.environ.get("TAVILY_API_KEY"):
    raise ValueError("TAVILY_API_KEY is missing. Please set it in your .env file.")

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def internet_search(query: str, max_results: int = 5):
    """Run a web search with improved query understanding"""
    return tavily_client.search(query, max_results=max_results)
