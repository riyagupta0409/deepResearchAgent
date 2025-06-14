from utils.firecrawl_api import scrape_url
import json

def scraper_node(state):
    """Scrapes content from the search result URLs."""
    print("---Scraping Web Pages---")
    search_results = state["search_results"]
    scraped_data = []
    for result in search_results:
        url = result.get('link')
        if url:
            print(f"Scraping: {url}")
            data = scrape_url(url)
            if data and 'markdown' in data:
                scraped_data.append({
                    "url": url,
                    "title": result.get('title'),
                    "content": data['markdown']
                })
    
    print(f"Scraped {len(scraped_data)} pages.")
    return {"scraped_data": scraped_data}
