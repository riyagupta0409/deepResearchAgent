from typing import TypedDict, List

class ResearchState(TypedDict):
    original_query: str
    sub_queries: List[str]
    search_results: List[dict]
    scraped_data: List[dict]
    filtered_chunks: List[str]
    final_answer: str
    sources: List[dict]

def input_node(state: ResearchState):
    """Accepts the initial user query."""
    print("---Starting with Input Node---")
    return {"original_query": state["original_query"]}
