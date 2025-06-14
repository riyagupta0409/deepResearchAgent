from utils.serp_api import search_web
from utils.firecrawl_api import scrape_url
from utils.gemini_api import call_gemini
from utils.helpers import get_value_from_path

def execute_node(state):
    """Executes the current step in the research plan."""
    plan = state.get("plan", [])
    step_index = state.get("current_step_index", 0)
    step_results = state.get("step_results", {})

    if step_index >= len(plan):
        return {"final_answer": step_results.get("step_" + str(len(plan)), {}).get("summary", "Research complete.")}

    current_step = plan[step_index]
    action = current_step["action"]
    step_input_ref = current_step["input"]
    step_id = current_step["id"]

    # Resolve input from previous steps
    resolved_input = None
    if isinstance(step_input_ref, list):
        # Handle multiple inputs by resolving each, filtering failures, and joining them
        resolved_parts = []
        for ref in step_input_ref:
            part = get_value_from_path(step_results, ref)
            # Only include content that is not None and not a scrape failure message
            if part and isinstance(part, str) and not part.startswith("SCRAPE_FAILED:"):
                resolved_parts.append(part)
        resolved_input = "\n\n---\n\n".join(resolved_parts)
    elif isinstance(step_input_ref, str) and step_input_ref.startswith("step_"):
        # Handle single input reference
        resolved_input = get_value_from_path(step_results, step_input_ref)
    else:
        # Handle literal input
        resolved_input = step_input_ref

    if resolved_input is None and action not in ["search_google"]: # search_google can have literal input
        print(f"Info: Could not resolve input for step '{step_input_ref}'. This can happen if a search returns fewer results than planned. Skipping step.")
        step_results[step_id] = {"content": f"SKIPPED: Could not resolve input {step_input_ref}"}
        return {"current_step_index": step_index + 1, "step_results": step_results}

    result = None
    if action == "search_google":
        result = search_web(resolved_input or state['original_query'])
        step_results[step_id] = {"urls": result}
    elif action == "scrape_url":
        if isinstance(resolved_input, str):
            scraped_data = scrape_url(resolved_input)
            if scraped_data and scraped_data.get('markdown'):
                result = scraped_data['markdown']
                step_results[step_id] = {"content": result}
            else:
                error_message = f"Failed to scrape or get content from URL: {resolved_input}"
                print(f"ERROR: {error_message}")
                step_results[step_id] = {"content": f"SCRAPE_FAILED: {error_message}"}
                result = None
        else:
            print(f"Warning: Scrape URL expects a single URL string, but got {type(resolved_input)}. Skipping.")
            result = None
    elif action == "summarize":
        if not resolved_input or not resolved_input.strip():
            print("ERROR: Summarizer received no content to process. Skipping.")
            result = "Error: Could not summarize because no content was found from previous steps."
        else:
            summarization_prompt = f"""You are a professional research analyst. Your task is to produce a comprehensive, detailed, and well-structured research report based on the provided text content. The report should be objective and synthesize information from all provided sources.

**Instructions:**
1.  **Do not invent information.** Base your entire report on the text provided below.
2.  **Structure the report** with the following sections: Executive Summary, Key Findings (in bullet points), Detailed Analysis, and Conclusion.
3.  **Write in a clear, professional tone.**
4.  **Ensure the report is detailed and thorough.**

**Provided Content to Synthesize:**
---
{resolved_input}
---

**Begin Research Report:**
"""
            summary = call_gemini(summarization_prompt)
            result = summary
        step_results[step_id] = {"summary": result}
    elif action == "finish":
        result = resolved_input
        step_results[step_id] = {"summary": result}
        return {"final_answer": result, "step_results": step_results}

    return {
        "step_results": step_results,
        "current_step_index": step_index + 1
    }
