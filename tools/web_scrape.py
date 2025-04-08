#!/usr/bin/env python3
"""
Web scraping tool for gathering data and documentation from websites.
"""
import sys
import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebScraper:
    """Web scraping utility for gathering documentation and data."""
    
    def __init__(self):
        """Initialize the web scraper with default headers."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; DevinAI/1.0; +http://example.com)'
        }
    
    def scrape(self, url: str) -> Dict[str, Any]:
        """
        Scrape content from a given URL.
        
        Args:
            url: The URL to scrape
            
        Returns:
            Dictionary containing:
                - title: Page title
                - headings: List of headings
                - content: Main content text
                - links: List of relevant links
        """
        try:
            # Fetch the page
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract relevant information
            result = {
                'title': self._get_title(soup),
                'headings': self._get_headings(soup),
                'content': self._get_main_content(soup),
                'links': self._get_relevant_links(soup)
            }
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return {
                'error': str(e),
                'url': url
            }
    
    def _get_title(self, soup: BeautifulSoup) -> str:
        """Extract page title."""
        return soup.title.string if soup.title else ""
    
    def _get_headings(self, soup: BeautifulSoup) -> list:
        """Extract all headings."""
        headings = []
        for tag in ['h1', 'h2', 'h3']:
            headings.extend([h.text.strip() for h in soup.find_all(tag)])
        return headings
    
    def _get_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content, focusing on article or main tags."""
        main_content = soup.find('article') or soup.find('main') or soup.find('div', class_='content')
        if main_content:
            return main_content.get_text(separator='\n', strip=True)
        return soup.get_text(separator='\n', strip=True)
    
    def _get_relevant_links(self, soup: BeautifulSoup) -> list:
        """Extract relevant links (documentation, API, etc)."""
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.text.strip()
            if any(keyword in href.lower() or keyword in text.lower() 
                  for keyword in ['doc', 'api', 'guide', 'reference']):
                links.append({
                    'text': text,
                    'url': href
                })
        return links

def main():
    """Main entry point for the script."""
    if len(sys.argv) != 2:
        print("Usage: python web_scrape.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    scraper = WebScraper()
    result = scraper.scrape(url)
    
    # Print results in JSON format
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main() 