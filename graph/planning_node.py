import json
from utils.gemini_api import generate_research_plan

def planning_node(state):
    """Generates a research plan based on the original query."""
    print("---Generating Research Plan---")
    original_query = state["original_query"]
    
    plan_json_str = generate_research_plan(original_query)
    
    try:
        plan = json.loads(plan_json_str)
        print(f"Generated Plan: {json.dumps(plan, indent=2)}")
        return {
            "plan": plan.get("steps", []),
            "step_results": {},
            "current_step_index": 0
        }
    except (json.JSONDecodeError, TypeError):
        print("Error: Failed to decode JSON plan from Gemini.")
        # Fallback to a simple, single-step plan
        return {
            "plan": [{
                "id": "step_1",
                "action": "search_google",
                "input": original_query
            }],
            "step_results": {},
            "current_step_index": 0
        }
