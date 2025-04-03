#!/usr/bin/env python3

import asyncio
import json
import sys
from datetime import datetime
from typing import List, Dict, Any
import aiohttp
from playwright.async_api import async_playwright

class WebScraper:
    """A web scraper with rate limiting and retries."""

    def __init__(self, max_retries: int = 3, rate_limit: float = 1.0, max_concurrent: int = 5, timeout: int = 30, disable_rate_limit: bool = False):
        """Initialize the scraper.

        Args:
            max_retries: Maximum number of retries per request
            rate_limit: Maximum requests per second
            max_concurrent: Maximum concurrent requests
            timeout: Request timeout in seconds
            disable_rate_limit: Whether to disable rate limiting (for testing)
        """
        self.max_retries = max_retries
        self.rate_limit = rate_limit
        self._min_request_interval = 1.0 / rate_limit
        self._last_request_time = asyncio.get_event_loop().time()
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self.timeout = timeout
        self.disable_rate_limit = disable_rate_limit
        self.session = None

    async def __aenter__(self):
        """Set up the session."""
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up the session."""
        if self.session:
            await self.session.close()
            self.session = None

    async def _wait_for_rate_limit(self):
        """Wait for rate limiting if needed."""
        if self.disable_rate_limit:
            return
        now = asyncio.get_event_loop().time()
        elapsed = now - self._last_request_time
        if elapsed < self._min_request_interval:
            await asyncio.sleep(self._min_request_interval - elapsed)
        self._last_request_time = now

    async def fetch_url(self, url: str) -> Dict[str, Any]:
        """Fetch content from a URL with retries and rate limiting.

        Args:
            url: URL to fetch

        Returns:
            Dict containing response data and metadata

        Raises:
            RuntimeError: If not used as an async context manager
            aiohttp.ClientError: If all retry attempts fail
        """
        if not self.session:
            raise RuntimeError("Scraper must be used as an async context manager")

        async with self._semaphore:
            for attempt in range(self.max_retries):
                try:
                    # Only wait for rate limit on first attempt
                    if attempt == 0:
                        await self._wait_for_rate_limit()
                    
                    response = await self.session.get(url)
                    # Update last request time after the request
                    if attempt == 0:
                        self._last_request_time = asyncio.get_event_loop().time()
                    
                    async with response:
                        content = await response.text()
                        if response.status == 200:
                            return {
                                'url': url,
                                'status': response.status,
                                'content': content,
                                'headers': dict(response.headers),
                                'attempt': attempt + 1
                            }
                        elif attempt < self.max_retries - 1:
                            await asyncio.sleep(2 ** attempt)  # Exponential backoff
                            continue
                        else:
                            return {
                                'url': url,
                                'status': response.status,
                                'content': content,
                                'headers': dict(response.headers),
                                'attempt': attempt + 1,
                                'error': f"HTTP {response.status}"
                            }
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    if attempt == self.max_retries - 1:
                        return {
                            'url': url,
                            'status': 500,
                            'content': str(e),
                            'headers': {},
                            'attempt': attempt + 1,
                            'error': str(e)
                        }
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff

    async def scrape_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Scrape multiple URLs concurrently.

        Args:
            urls: List of URLs to scrape

        Returns:
            List of response data dictionaries
        """
        # Create tasks with rate limiting
        tasks = []
        for url in urls:
            task = self.fetch_url(url)
            tasks.append(task)
            if not self.disable_rate_limit:
                await asyncio.sleep(self._min_request_interval)
        return await asyncio.gather(*tasks)

async def scrape_webpage(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto(url)
            title = await page.title()
            meta_description = await page.evaluate('''() => {
                const meta = document.querySelector('meta[name="description"]');
                return meta ? meta.content : '';
            }''')
            main_text = await page.evaluate('''() => {
                const main = document.querySelector('main') || document.body;
                return main.innerText;
            }''')
            return {
                'url': url,
                'title': title,
                'meta_description': meta_description,
                'main_text': main_text
            }
        except (playwright._impl._api_types.Error, playwright._impl._api_types.TimeoutError) as e:
            print(f"Error scraping webpage: {str(e)}", file=sys.stderr)
            return None
        finally:
            await browser.close()

def main():
    if len(sys.argv) != 2:
        print("Usage: python web_scraper.py <url>", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    result = asyncio.run(scrape_webpage(url))
    if result:
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main() 