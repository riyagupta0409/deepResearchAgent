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
    prompt = f"""Given the following user query, please generate 3-4 sub-queries that are more specific and focused for web research. The sub-queries should be diverse and cover different aspects of the main query. Return the sub-queries as a JSON list of strings.

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

def generate_research_plan(query: str) -> str:
    """Generates a step-by-step research plan in JSON format."""
    prompt = f"""You are an expert research assistant. Your task is to create a step-by-step plan to answer a user's query.

You have the following tools available:
- `search_google(query: str)`: Searches Google and returns a list of URLs and titles.
- `scrape_url(url: str)`: Scrapes the content of a single URL. The result is accessed via `.content`.
- `summarize(contents: list[str], query: str)`: **Takes a list of content strings** and synthesizes a comprehensive answer.
- `finish(answer: str)`: Finishes the research and provides the final answer.

**CRITICAL INSTRUCTIONS:**
1. The final step in any plan MUST be the `finish` action.
2. The input for the `summarize` action MUST be a JSON array of references to the `.content` of ALL previous `scrape_url` steps.
3. The input for the `finish` action MUST be a reference to the `.summary` of the `summarize` step.

User Query: "{query}"

Respond with ONLY the JSON plan, without any markdown formatting or other text.

Example Plan for a multi-step query:
{{
  "steps": [
    {{
      "id": "step_1",
      "action": "search_google",
      "input": "LangGraph vs CrewAI"
    }},
    {{
      "id": "step_2",
      "action": "scrape_url",
      "input": "step_1.urls[0]"
    }},
    {{
      "id": "step_3",
      "action": "scrape_url",
      "input": "step_1.urls[1]"
    }},
    {{
      "id": "step_4",
      "action": "summarize",
      "input": ["step_2.content", "step_3.content"]
    }},
    {{
      "id": "step_5",
      "action": "finish",
      "input": "step_4.summary"
    }}
  ]
}}
"""

    response_text = call_gemini(prompt)
    if response_text:
        # Clean the response to extract only the JSON part
        json_str = response_text.strip().replace('```json', '').replace('```', '').strip()
        return json_str
    return "{}" # Return empty JSON if something goes wrong
