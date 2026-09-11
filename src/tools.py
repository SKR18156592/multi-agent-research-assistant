import wikipedia
from langchain_community.document_loaders import WikipediaLoader
from langchain_tavily import TavilySearch



wikipedia.set_user_agent("research-assistant/0.1 (you@example.com)")

tavily_search = TavilySearch(max_results=3)

def fetch_web_search(query: str) -> str:
    search_docs = tavily_search.invoke({"query": query})
    return "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )

def fetch_wikipedia_search(query: str) -> str:
    search_docs = WikipediaLoader(query=query, load_max_docs=2).load()
    return "\n\n---\n\n".join(
        [
            f'<Document source="{doc.metadata.get("source", "")}" page="{doc.metadata.get("page", "")}"/>\n{doc.page_content}\n</Document>'
            for doc in search_docs
        ]
    )