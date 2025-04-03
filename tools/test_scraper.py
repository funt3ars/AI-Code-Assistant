import asyncio
import logging
import socket
from pathlib import Path
from typing import Dict, Any
import pytest
import pytest_asyncio
from web_scraper import WebScraper
from html_parser import HTMLParser
from mock_server import MockServer

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('test_scraper')

def find_free_port():
    """Find a free port to use for testing."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

@pytest_asyncio.fixture
async def mock_server():
    """Fixture to start and stop the mock server."""
    port = find_free_port()
    server = MockServer(port=port)
    try:
        await server.start()
        yield server
    finally:
        await server.stop()

@pytest_asyncio.fixture
async def scraper(mock_server):
    """Fixture to create a web scraper instance."""
    async with WebScraper(
        max_concurrent=10,
        timeout=5,
        max_retries=2,
        rate_limit=5
    ) as scraper:
        yield scraper

@pytest.mark.asyncio
async def test_basic_scraping(mock_server, scraper):
    """Test basic scraping functionality."""
    url = f'http://localhost:{mock_server.port}/'
    result = await scraper.fetch_url(url)
    
    assert result['status'] == 200
    assert 'Welcome to the mock server' in result['content']
    
    # Parse the content
    parser = HTMLParser()
    parsed = parser.parse(result['content'], url)
    
    assert parsed['status'] == 'success'
    assert parsed['title'] == 'Home Page'
    assert 'Welcome to the mock server' in parsed['main_text']
    assert len(parsed['links']) == 3
    assert len(parsed['images']) == 1

@pytest.mark.asyncio
async def test_error_handling(mock_server, scraper):
    """Test error handling."""
    url = f'http://localhost:{mock_server.port}/error/404'
    result = await scraper.fetch_url(url)
    
    assert result['status'] == 404
    assert 'Mock error 404' in result['content']

@pytest.mark.asyncio
async def test_slow_response(mock_server, scraper):
    """Test handling of slow responses."""
    url = f'http://localhost:{mock_server.port}/slow/2'
    result = await scraper.fetch_url(url)
    
    assert result['status'] == 200
    assert 'Response delayed by 2.0s' in result['content']

@pytest.mark.asyncio
async def test_malformed_html(mock_server, scraper):
    """Test handling of malformed HTML."""
    url = f'http://localhost:{mock_server.port}/malformed'
    result = await scraper.fetch_url(url)
    
    assert result['status'] == 200
    
    # Parse the content
    parser = HTMLParser()
    parsed = parser.parse(result['content'], url)
    
    assert parsed['status'] == 'success'  # BeautifulSoup can handle some malformed HTML

@pytest.mark.asyncio
async def test_concurrent_scraping(mock_server, scraper):
    """Test concurrent scraping of multiple URLs."""
    urls = [
        f'http://localhost:{mock_server.port}/',
        f'http://localhost:{mock_server.port}/page1',
        f'http://localhost:{mock_server.port}/page2'
    ]
    
    results = await scraper.scrape_urls(urls)
    
    assert len(results) == 3
    for result in results:
        assert result['status'] == 200
        assert 'Page:' in result['content'] or 'Home Page' in result['content']

@pytest.mark.asyncio
async def test_rate_limiting(mock_server, scraper):
    """Test rate limiting functionality."""
    # Use more requests to ensure we hit the rate limit
    urls = [f'http://localhost:{mock_server.port}/'] * 20
    start_time = asyncio.get_event_loop().time()

    results = await scraper.scrape_urls(urls)
    end_time = asyncio.get_event_loop().time()
    time_taken = end_time - start_time

    # With rate limit of 5 requests per second, 20 requests should take at least 3.8 seconds
    # (allowing for some small timing variations)
    assert time_taken >= 3.8, f"Time taken ({time_taken:.2f}s) was less than expected minimum (3.8s)"
    
    # Verify all requests were successful
    assert all(result['status'] == 200 for result in results)
    assert len(results) == len(urls)
    
    # Verify we didn't exceed the rate limit too much
    # (allowing for some small timing variations)
    assert time_taken <= 5.0, f"Time taken ({time_taken:.2f}s) was more than expected maximum (5.0s)"

@pytest.mark.asyncio
async def test_context_manager_requirement():
    """Test that scraper must be used as a context manager."""
    scraper = WebScraper()
    with pytest.raises(RuntimeError) as exc_info:
        await scraper.fetch_url('http://example.com')
    assert str(exc_info.value) == "Scraper must be used as an async context manager"

@pytest.mark.asyncio
async def test_connection_error_handling(mock_server):
    """Test handling of connection errors."""
    # Use an invalid port to trigger connection error
    async with WebScraper(max_retries=2) as scraper:
        result = await scraper.fetch_url(f'http://localhost:1/')
        
        assert 'error' in result
        assert result['status'] == 500
        assert result['attempt'] == 2
        assert 'Cannot connect to host' in result['content']

@pytest.mark.asyncio
async def test_concurrent_error_handling(mock_server):
    """Test handling of errors in concurrent requests."""
    urls = [
        f'http://localhost:{mock_server.port}/',  # Valid URL
        f'http://localhost:1/',  # Invalid URL to trigger error
        f'http://localhost:{mock_server.port}/page1'  # Valid URL
    ]
    
    async with WebScraper(max_retries=1) as scraper:
        results = await scraper.scrape_urls(urls)
        
        assert len(results) == 3
        assert results[0]['status'] == 200  # First URL succeeds
        assert 'error' in results[1]  # Second URL fails
        assert results[2]['status'] == 200  # Third URL succeeds

@pytest.mark.asyncio
async def test_max_retries_exceeded(mock_server):
    """Test behavior when max retries is exceeded."""
    async with WebScraper(max_retries=2, timeout=1) as scraper:
        # Use the mock server's slow endpoint with a timeout to force retries
        result = await scraper.fetch_url(f'http://localhost:{mock_server.port}/slow/5')
        
        assert 'error' in result
        assert result['attempt'] == 2
        assert result['status'] == 500

if __name__ == '__main__':
    pytest.main(['-v', 'test_scraper.py']) 