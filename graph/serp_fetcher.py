from utils.serp_api import search_web

def serp_fetcher_node(state):
    """Performs web searches for each sub-query."""
    print("---Performing Web Searches---")
    sub_queries = state["sub_queries"]
    all_results = []
    for query in sub_queries:
        print(f"Searching for: {query}")
        results = search_web(query)
        all_results.extend(results)
    
    print(f"Found {len(all_results)} results.")
    return {"search_results": all_results}
