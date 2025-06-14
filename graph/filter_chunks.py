import tiktoken
from utils.gemini_api import call_gemini
import json

def chunk_text(text, max_tokens=2000):
    """Splits text into chunks of a specified max token size."""
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)
    return chunks

def filter_chunks_node(state):
    """Chunks and filters the scraped content."""
    print("---Chunking and Filtering Content---")
    scraped_data = state["scraped_data"]
    original_query = state["original_query"]
    
    all_chunks_with_source = []
    for data in scraped_data:
        chunks = chunk_text(data['content'])
        for chunk in chunks:
            all_chunks_with_source.append({"chunk": chunk, "source": data['url']})
    
    print(f"Created {len(all_chunks_with_source)} chunks.")

    prompt = f"""Given the following chunks of text and the original research query, identify the most relevant chunks. Return a JSON list of the selected chunks. 

Original Query: {original_query}

Chunks: {json.dumps(all_chunks_with_source)}

Relevant Chunks (JSON list of strings):"""

    response_text = call_gemini(prompt)
    relevant_chunks = []
    if response_text:
        try:
            json_str = response_text.strip().replace('```json', '').replace('```', '').strip()
            relevant_chunks = json.loads(json_str)
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from Gemini for filtering. Using all chunks.")
            relevant_chunks = [item['chunk'] for item in all_chunks_with_source]
    else:
        relevant_chunks = [item['chunk'] for item in all_chunks_with_source]

    print(f"Filtered down to {len(relevant_chunks)} relevant chunks.")
    
    return {"filtered_chunks": relevant_chunks, "sources": scraped_data}
