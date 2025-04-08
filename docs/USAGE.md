# Devin Integration Usage Guide

This guide demonstrates how to use the Devin integration components effectively.

## Setup

1. Install the environment:
```bash
./setup-devin.sh
```

2. Activate the virtual environment:
```bash
source devin-venv/bin/activate
```

## Web Scraping Tool

The web scraping tool extracts structured information from web pages.

### Basic Usage

```python
from tools.web_scrape import WebScraper

# Initialize scraper
scraper = WebScraper()

# Scrape a documentation page
result = scraper.scrape("https://python.org/docs")

# Access different components
print(f"Title: {result['title']}")
print(f"Main headings: {result['headings']}")
print(f"Documentation links: {result['links']}")
```

### Command Line Usage

```bash
python tools/web_scrape.py https://python.org/docs
```

Example output:
```json
{
  "title": "Python Documentation",
  "headings": ["Python Documentation", "Getting Started", "API Reference"],
  "content": "...",
  "links": [
    {
      "text": "Library Reference",
      "url": "/docs/library"
    }
  ]
}
```

## Search Engine Tool

The search tool uses DuckDuckGo to find relevant information.

### Basic Usage

```python
from tools.search_ddg import SearchEngine

# Initialize search engine
search = SearchEngine(max_results=5)

# Perform search
results = search.search("Python asyncio tutorial")

# Process results
for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['link']}")
    print(f"Summary: {result['snippet']}\n")
```

### Command Line Usage

```bash
python tools/search_ddg.py "Python asyncio tutorial"
```

Example output:
```json
[
  {
    "title": "AsyncIO in Python: A Complete Walkthrough",
    "link": "https://realpython.com/async-io-python/",
    "snippet": "A comprehensive guide to asynchronous programming..."
  }
]
```

## Multi-Agent System

The Planner and Executor work together to handle complex tasks.

### Basic Usage

```python
from devin_integration import Planner, Executor

# Initialize components
planner = Planner()
executor = Executor()

# Define a task
task = "Create a new REST API endpoint"

# Get task analysis
analysis = planner.analyze_task(task)

# Execute the task
result = executor.execute(analysis)

# Check results
print(f"Task status: {result['status']}")
for step in result['steps_completed']:
    print(f"Step: {step['description']}")
    print(f"Status: {step['status']}")
    print(f"Completed at: {step['timestamp']}\n")
```

## Best Practices

1. **Error Handling**
   - Always check for errors in results
   - Log errors appropriately
   - Handle network timeouts gracefully

2. **Performance**
   - Use appropriate timeouts for web requests
   - Cache results when possible
   - Limit search results to necessary amount

3. **Security**
   - Validate all URLs before scraping
   - Don't expose sensitive information in logs
   - Follow rate limiting guidelines

## Troubleshooting

Common issues and solutions:

1. **Web Scraping Fails**
   - Check URL validity
   - Verify network connection
   - Check for rate limiting

2. **Search Returns No Results**
   - Verify query syntax
   - Try different search terms
   - Check network connection

3. **Planner/Executor Issues**
   - Verify task description clarity
   - Check for proper initialization
   - Review error logs 