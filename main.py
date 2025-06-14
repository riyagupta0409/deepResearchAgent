import os
import json
import argparse
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

# Import node functions
from graph.input_node import input_node
from graph.query_generator import query_generator_node
from graph.serp_fetcher import serp_fetcher_node
from graph.scraper import scraper_node
from graph.filter_chunks import filter_chunks_node
from graph.summarizer import summarizer_node
from graph.output_formatter import output_formatter_node

# Load environment variables
load_dotenv()

# Define the state for the graph
class ResearchState(TypedDict):
    original_query: str
    sub_queries: List[str]
    search_results: List[dict]
    scraped_data: List[dict]
    filtered_chunks: List[str]
    final_answer: str
    sources: List[dict]
    final_output_json: str

def build_graph():
    """Builds the LangGraph research agent."""
    workflow = StateGraph(ResearchState)

    # Add nodes
    workflow.add_node("input", input_node)
    workflow.add_node("query_generator", query_generator_node)
    workflow.add_node("serp_fetcher", serp_fetcher_node)
    workflow.add_node("scraper", scraper_node)
    workflow.add_node("filter_chunks", filter_chunks_node)
    workflow.add_node("summarizer", summarizer_node)
    workflow.add_node("output_formatter", output_formatter_node)

    # Set entry point
    workflow.set_entry_point("input")

    # Add edges
    workflow.add_edge("input", "query_generator")
    workflow.add_edge("query_generator", "serp_fetcher")
    workflow.add_edge("serp_fetcher", "scraper")
    workflow.add_edge("scraper", "filter_chunks")
    workflow.add_edge("filter_chunks", "summarizer")
    workflow.add_edge("summarizer", "output_formatter")
    workflow.add_edge("output_formatter", END)

    # Compile the graph
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
            if node_name == "query_generator":
                yield {"type": "status", "data": "✅ Generated sub-queries..."}
            elif node_name == "serp_fetcher":
                yield {"type": "status", "data": "🔍 Searching the web..."}
            elif node_name == "scraper":
                yield {"type": "status", "data": "📄 Scraping web pages..."}
            elif node_name == "filter_chunks":
                yield {"type": "status", "data": "✂️ Filtering and chunking content..."}
            elif node_name == "summarizer":
                yield {"type": "status", "data": "✍️ Synthesizing the final answer..."}
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
