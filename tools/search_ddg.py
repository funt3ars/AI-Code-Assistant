#!/usr/bin/env python3
"""
Search tool using DuckDuckGo to find relevant information.
"""
import sys
import json
from typing import List, Dict, Any
import logging
from duckduckgo_search import ddg

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchEngine:
    """Search engine utility using DuckDuckGo."""
    
    def __init__(self, max_results: int = 10):
        """
        Initialize the search engine.
        
        Args:
            max_results: Maximum number of results to return
        """
        self.max_results = max_results
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for information using DuckDuckGo.
        
        Args:
            query: Search query string
            
        Returns:
            List of dictionaries containing:
                - title: Result title
                - link: Result URL
                - snippet: Text snippet from the result
        """
        try:
            # Perform the search
            results = ddg(query, max_results=self.max_results)
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'title': result['title'],
                    'link': result['link'],
                    'snippet': result['snippet']
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error performing search: {str(e)}")
            return [{
                'error': str(e),
                'query': query
            }]

def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python search_ddg.py <search query>")
        sys.exit(1)
    
    # Combine all arguments into the search query
    query = ' '.join(sys.argv[1:])
    
    search_engine = SearchEngine()
    results = search_engine.search(query)
    
    # Print results in JSON format
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
