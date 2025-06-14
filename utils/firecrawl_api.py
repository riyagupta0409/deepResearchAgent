import os
import requests
from dotenv import load_dotenv

load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
FIRECRAWL_API_URL = "https://api.firecrawl.dev/v0/scrape"

def scrape_url(url: str):
    """Scrapes a URL using Firecrawl.dev API."""
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "url": url
    }

    try:
        response = requests.post(FIRECRAWL_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get('data', {})
    except requests.exceptions.RequestException as e:
        print(f"Error calling Firecrawl API: {e}")
        return None
