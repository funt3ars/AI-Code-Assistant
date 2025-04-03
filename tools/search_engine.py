#!/usr/bin/env python3
from googlesearch import search
import sys
import json

def search_web(query, max_results=5):
    try:
        results = []
        for url in search(query, num_results=max_results):
            results.append({
                'title': query,  # Google Search API doesn't provide titles
                'link': url,
                'snippet': ''  # Google Search API doesn't provide snippets
            })
        return results
    except Exception as e:
        print(f"Error performing search: {str(e)}", file=sys.stderr)
        return []

def main():
    if len(sys.argv) < 2:
        print("Usage: python search_engine.py <query> [max_results]")
        sys.exit(1)
    
    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    try:
        results = search_web(query, max_results)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 