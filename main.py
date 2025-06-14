import os
import json
import argparse
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

# Import node functions
from graph.input_node import input_node
from graph.planning_node import planning_node
from graph.plan_validation_node import plan_validation_node
from graph.execution_node import execute_node
from graph.output_formatter import output_formatter_node

# Load environment variables
load_dotenv()

# Define the state for the graph
class ResearchState(TypedDict):
    original_query: str
    plan: List[dict]
    step_results: dict
    current_step_index: int
    final_answer: str
    final_output_json: str

def should_continue(state: ResearchState) -> str:
    """Determines whether to continue the research loop or finish."""
    plan = state.get("plan", [])
    step_index = state.get("current_step_index", 0)
    if step_index >= len(plan):
        return "end"
    
    # Check if the last executed step was a 'finish' action
    if state.get("final_answer"):
        return "end"
        
    return "continue"

def build_graph():
    """Builds the LangGraph workflow with planning and execution loop."""
    workflow = StateGraph(ResearchState)

    # Add nodes
    workflow.add_node("input_node", input_node)
    workflow.add_node("planning_node", planning_node)
    workflow.add_node("plan_validation_node", plan_validation_node)
    workflow.add_node("execution_node", execute_node)
    workflow.add_node("output_formatter", output_formatter_node)

    # Set entry point
    workflow.set_entry_point("input_node")

    # Add edges
    workflow.add_edge("input_node", "planning_node")
    workflow.add_edge("planning_node", "plan_validation_node")
    workflow.add_edge("plan_validation_node", "execution_node")

    # Conditional edge for the execution loop
    workflow.add_conditional_edges(
        "execution_node",
        should_continue,
        {
            "continue": "execution_node",
            "end": "output_formatter"
        }
    )
    workflow.add_edge("output_formatter", END)

    return workflow.compile()

def run_research_agent(query: str):
    """Runs the research agent for a given query and yields status updates."""
    if not all([os.getenv("GEMINI_API_KEY"), os.getenv("SERPER_API_KEY"), os.getenv("FIRECRAWL_API_KEY")]):
        yield {"type": "error", "data": "API keys for Gemini, Serper, and Firecrawl must be set in the .env file."}
        return

    app = build_graph()
    initial_state = {"original_query": query}

    for event in app.stream(initial_state):
        for node_name, output in event.items():
            if node_name == "planning_node":
                yield {"type": "status", "data": "🤔 Generating research plan..."}
            elif node_name == "plan_validation_node":
                yield {"type": "status", "data": "✅ Validating and correcting plan..."}
            elif node_name == "execution_node":
                plan = output.get("plan", [])
                step_index = output.get("current_step_index", 1) -1 # -1 because it's the index of the step just completed
                if step_index < len(plan):
                    action = plan[step_index].get('action', 'Unknown')
                    yield {"type": "status", "data": f"⚙️ Executing: {action}..."}
            elif node_name == "output_formatter":
                yield {"type": "result", "data": output.get('final_output_json')}

def main():
    """Main function to run the research agent from the command line."""
    parser = argparse.ArgumentParser(description="Deep Research Agent")
    parser.add_argument("query", type=str, help="The research query.")
    args = parser.parse_args()
    query = args.query

    if not query:
        print("Error: Query cannot be empty.")
        return

    final_result = None
    for event in run_research_agent(query):
        if event.get("type") == "status":
            print(event["data"])  # Print status to console
        elif event.get("type") == "result":
            final_result = event["data"]
            break
        elif event.get("type") == "error":
            print(f"Error: {event['data']}")
            break

    if final_result:
        print("\n--- Research Complete ---")
        print(json.dumps(json.loads(final_result), indent=4))
    else:
        print("\nCould not complete research.")

if __name__ == "__main__":
    main()
