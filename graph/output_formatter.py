import json

def output_formatter_node(state):
    """Formats the final output into a JSON object."""
    print("---Formatting Final Output---")
    
    final_json = {
        "original_query": state["original_query"],
        "sub_queries": state["sub_queries"],
        "sources": [
            {
                "title": source.get("title"),
                "url": source.get("url"),
                "summary": source.get("content", "")[:500] + "..." 
            } for source in state["sources"]
        ],
        "final_answer": state["final_answer"]
    }
    
    formatted_output = json.dumps(final_json, indent=4)
    
    # Save the final output to a file
    with open("research_result.json", "w") as f:
        f.write(formatted_output)

    print("Final result saved to research_result.json")
    
    return {"final_output_json": formatted_output}
