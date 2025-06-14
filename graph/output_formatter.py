import json
from utils.helpers import get_value_from_path

def output_formatter_node(state):
    """Formats the final answer and extracts metadata for the UI."""
    print("---Formatting Final Output---")
    original_query = state["original_query"]
    final_answer = state.get("final_answer", "No final answer could be generated.")
    plan = state.get("plan", [])
    step_results = state.get("step_results", {})

    # Extract Sub-Queries (search queries)
    sub_queries = [
        step["input"] for step in plan if step.get("action") == "search_google"
    ]

    # Extract Sources Used (successfully scraped URLs)
    sources_used = []
    for step in plan:
        if step.get("action") == "scrape_url":
            step_id = step["id"]
            result = step_results.get(step_id, {}).get("content", "")
            # Check if scrape was successful
            if result and not str(result).startswith("SKIPPED:") and not str(result).startswith("SCRAPE_FAILED:"):
                # Resolve the input path to get the URL
                url = get_value_from_path(step_results, step["input"])
                if url:
                    sources_used.append(url)

    output_data = {
        "original_query": original_query,
        "final_answer": final_answer,
        "sub_queries": sub_queries,
        "sources_used": sources_used,
        "plan_executed": plan
    }

    # Convert to JSON string
    output_json = json.dumps(output_data, indent=4)

    # Save to file
    with open("research_result.json", "w") as f:
        f.write(output_json)

    print("Final result saved to research_result.json")
    
    return {"final_output_json": output_json}
