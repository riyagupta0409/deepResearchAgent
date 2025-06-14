from utils.gemini_api import call_gemini

def summarizer_node(state):
    """Synthesizes the final answer from filtered chunks."""
    print("---Synthesizing Final Answer---")
    filtered_chunks = state["filtered_chunks"]
    original_query = state["original_query"]
    sources = state["sources"]

    source_citations = "\n".join([f"[{i+1}] {source['title']}: {source['url']}" for i, source in enumerate(sources)])

    prompt = f"""Based on the following content and the original query, synthesize a deep, research-backed answer. The answer should be comprehensive and well-structured. Make sure to cite the sources using the format [1], [2], etc., corresponding to the provided source list.

Original Query: {original_query}

Content:
{'\n\n'.join(filtered_chunks)}

Sources:
{source_citations}

Final Answer:"""

    final_answer = call_gemini(prompt)
    if not final_answer:
        final_answer = "Could not generate a final answer based on the provided content."

    print("Final answer generated.")
    
    return {"final_answer": final_answer}
