from utils.gemini_api import generate_sub_queries

def query_generator_node(state):
    """Generates sub-queries based on the original query."""
    print("---Generating Sub-Queries---")
    original_query = state["original_query"]
    sub_queries = generate_sub_queries(original_query)
    if not sub_queries:
        # Fallback if API fails
        sub_queries = [original_query]
    print(f"Generated sub-queries: {sub_queries}")
    return {"sub_queries": sub_queries}
