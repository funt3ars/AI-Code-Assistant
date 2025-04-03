"""Unit tests for the web scraper module."""

import pytest
import pytest_asyncio
import asyncio
import aiohttp
from unittest.mock import AsyncMock, patch, MagicMock, call
from tools.web_scraper import WebScraper

class TestWebScraperSessionManagement:
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test that the scraper properly manages its session."""
        scraper = None
        async with WebScraper() as s:
            scraper = s
            assert scraper.session is not None
            assert not scraper.session.closed
        assert scraper.session is None

    @pytest.mark.asyncio
    async def test_session_required(self):
        """Test that using the scraper outside a context manager raises an error."""
        scraper = WebScraper()
        with pytest.raises(RuntimeError):
            await scraper.fetch_url("https://example.com")

@pytest_asyncio.fixture
async def mock_session():
    """Create a mock aiohttp ClientSession."""
    mock = AsyncMock()
    mock.get = AsyncMock()
    return mock

@pytest.fixture
def mock_response():
    """Create a mock response with success status."""
    response = AsyncMock()
    response.status = 200
    response.text = AsyncMock(return_value="Success")
    response.headers = {'Content-Type': 'text/html'}
    response.__aenter__ = AsyncMock(return_value=response)
    response.__aexit__ = AsyncMock(return_value=None)
    return response

class TestWebScraperRateLimiting:
    @pytest.mark.asyncio
    async def test_rate_limiting(self, mock_session, mock_response):
        """Test that requests are rate limited."""
        # Track sleep calls for rate limiting
        sleep_calls = []

        async def mock_sleep(seconds):
            sleep_calls.append(seconds)

        mock_session.get.return_value = mock_response

        with patch('asyncio.sleep', mock_sleep):
            async with WebScraper(max_retries=1, rate_limit=2) as scraper:
                scraper.session = mock_session
                await scraper.fetch_url("https://test1.com")
                await scraper.fetch_url("https://test2.com")

        # Verify rate limiting
        assert len(sleep_calls) > 0

class TestWebScraperRetries:
    @pytest.mark.asyncio
    async def test_exponential_backoff(self, mock_session, mock_response):
        """Test that failed requests use exponential backoff."""
        # Track sleep calls for backoff
        sleep_calls = []

        async def mock_sleep(seconds):
            sleep_calls.append(seconds)

        # Set up response sequence: fail twice, succeed on third try
        error_response = AsyncMock()
        error_response.status = 500
        error_response.text = AsyncMock(return_value="Error")
        error_response.headers = {'Content-Type': 'text/html'}
        error_response.__aenter__ = AsyncMock(return_value=error_response)
        error_response.__aexit__ = AsyncMock(return_value=None)

        mock_session.get.side_effect = [
            error_response,
            error_response,
            mock_response
        ]

        with patch('asyncio.sleep', mock_sleep):
            async with WebScraper(max_retries=3) as scraper:
                scraper.session = mock_session
                result = await scraper.fetch_url("https://example.com")

        # Verify exponential backoff timing
        assert sleep_calls == [1, 2]  # 2^0=1, 2^1=2

    @pytest.mark.asyncio
    async def test_success_after_retry(self, mock_session, mock_response):
        """Test that successful request after retry returns correct response."""
        error_response = AsyncMock()
        error_response.status = 500
        error_response.text = AsyncMock(return_value="Error")
        error_response.headers = {'Content-Type': 'text/html'}
        error_response.__aenter__ = AsyncMock(return_value=error_response)
        error_response.__aexit__ = AsyncMock(return_value=None)

        mock_session.get.side_effect = [
            error_response,
            mock_response
        ]

        async with WebScraper(max_retries=3) as scraper:
            scraper.session = mock_session
            result = await scraper.fetch_url("https://example.com")

        assert result['status'] == 200
        assert result['content'] == "Success"

class TestWebScraperConcurrency:
    @pytest.mark.asyncio
    async def test_concurrent_scraping(self, mock_session, mock_response):
        """Test that multiple URLs can be scraped concurrently."""
        mock_session.get.return_value = mock_response

        urls = ["https://example1.com", "https://example2.com", "https://example3.com"]

        async with WebScraper(max_retries=1) as scraper:
            scraper.session = mock_session
            results = await scraper.scrape_urls(urls)

        assert len(results) == 3
        for result in results:
            assert result['status'] == 200
            assert result['content'] == "Success"

    @pytest.mark.asyncio
    async def test_mixed_success_failure(self, mock_session):
        """Test handling of mixed successes and failures in concurrent scraping."""
        success_response = AsyncMock()
        success_response.status = 200
        success_response.text = AsyncMock(return_value="Success")
        success_response.headers = {'Content-Type': 'text/html'}
        success_response.__aenter__ = AsyncMock(return_value=success_response)
        success_response.__aexit__ = AsyncMock(return_value=None)

        fail_response = AsyncMock()
        fail_response.status = 500
        fail_response.text = AsyncMock(return_value="Error")
        fail_response.headers = {'Content-Type': 'text/html'}
        fail_response.__aenter__ = AsyncMock(return_value=fail_response)
        fail_response.__aexit__ = AsyncMock(return_value=None)

        # Set up response sequence for each URL
        # We need enough responses for:
        # - success1.com (1 response)
        # - fail.com (2 attempts with max_retries=1)
        # - success2.com (1 response)
        mock_session.get.side_effect = [
            success_response,  # success1.com
            fail_response,    # fail.com first attempt
            fail_response,    # fail.com retry
            success_response, # success2.com
            fail_response,    # Extra response in case of unexpected retries
            fail_response     # Extra response in case of unexpected retries
        ]

        urls = ["https://success1.com", "https://fail.com", "https://success2.com"]

        async with WebScraper(max_retries=1) as scraper:
            scraper.session = mock_session
            results = await scraper.scrape_urls(urls)

        # Verify results
        assert len(results) == 3
        assert results[0]["status"] == 200
        assert results[0]["content"] == "Success"
        assert results[1]["status"] == 500
        assert results[1]["error"] == "HTTP 500"
        assert results[2]["status"] == 200
        assert results[2]["content"] == "Success"

class TestWebScraperErrorHandling:
    @pytest.mark.asyncio
    async def test_timeout_handling(self, mock_session):
        """Test handling of timeout errors."""
        mock_session.get.side_effect = asyncio.TimeoutError()

        async with WebScraper(max_retries=1) as scraper:
            scraper.session = mock_session
            result = await scraper.fetch_url("https://example.com")

        assert result['status'] == 500
        assert 'error' in result

    @pytest.mark.asyncio
    async def test_connection_error_handling(self, mock_session):
        """Test handling of connection errors."""
        mock_session.get.side_effect = aiohttp.ClientConnectionError("Connection refused")

        async with WebScraper(max_retries=1) as scraper:
            scraper.session = mock_session
            result = await scraper.fetch_url("https://example.com")

        assert result['status'] == 500
        assert 'error' in result

    @pytest.mark.asyncio
    async def test_invalid_url_handling(self, mock_session):
        """Test handling of invalid URLs."""
        mock_session.get.side_effect = aiohttp.InvalidURL("Invalid URL")

        async with WebScraper(max_retries=1) as scraper:
            scraper.session = mock_session
            result = await scraper.fetch_url("not-a-url")

        assert result['status'] == 500
        assert 'error' in result 