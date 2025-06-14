import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

def call_gemini(prompt: str):
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        content = response.json()['candidates'][0]['content']['parts'][0]['text']
        return content
    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return None

def generate_sub_queries(query: str) -> list:
    """Generates sub-queries using Gemini API."""
    prompt = f"""Given the following user query, please generate 1-2 sub-queries that are more specific and focused for web research. The sub-queries should be diverse and cover different aspects of the main query. Return the sub-queries as a JSON list of strings.

User Query: {query}

Sub-queries (JSON list of strings):"""

    response_text = call_gemini(prompt)
    if response_text:
        try:
            # Clean the response to extract only the JSON part
            json_str = response_text.strip().replace('```json', '').replace('```', '').strip()
            return json.loads(json_str)
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from Gemini response.")
            return []
    return []

def filter_relevant_chunks(chunks: list, query: str):
    """Filters relevant chunks using Gemini API."""
    # This function will be implemented later
    pass

def synthesize_answer(chunks: list, query: str):
    """Synthesizes the final answer using Gemini API."""
    # This function will be implemented later
    pass
