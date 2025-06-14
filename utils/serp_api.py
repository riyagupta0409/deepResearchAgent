import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPAPI_URL = "https://serpapi.com/search"
print(SERPER_API_KEY)
def search_web(query: str):
    """Searches the web for a given query using SerpApi.com API."""
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPER_API_KEY # Using the key from .env
    }

    try:
        # Use GET request with params for SerpApi.com
        response = requests.get(SERPAPI_URL, params=params)
        response.raise_for_status()
        # SerpApi.com uses 'organic_results' key for search results
        return response.json().get('organic_results', [])[:3]
    except requests.exceptions.RequestException as e:
        print(f"Error calling SerpApi: {e}")
        return []
