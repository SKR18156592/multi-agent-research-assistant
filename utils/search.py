import os
from langchain_community.tools.tavily_search import TavilySearchResults

def get_search_tool(max_results: int = 3):
    return TavilySearchResults(max_results=max_results)