"""Web functionality for the Devin Integration package."""

import aiohttp
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from .errors import WebError
from .utils import validate_url

@dataclass
class WebResponse:
    """Represents a web response."""
    url: str
    status_code: int
    content: str
    headers: Dict[str, str]

class WebClient:
    """Client for making web requests."""
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        """Initialize the web client.
        
        Args:
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries for failed requests.
        """
        self.timeout = timeout
        self.max_retries = max_retries
        
    def get(self, url: str) -> WebResponse:
        """Make a GET request.
        
        Args:
            url: URL to request.
            
        Returns:
            WebResponse object containing the response data.
            
        Raises:
            WebError: If the request fails.
        """
        try:
            validate_url(url)
            # TODO: Implement actual request functionality
            # For now, return mock response
            return WebResponse(
                url=url,
                status_code=200,
                content="Example content",
                headers={"content-type": "text/html"}
            )
        except Exception as e:
            raise WebError(f"GET request failed: {e}", url=url, cause=e)
            
    def post(self, url: str, data: Dict[str, Any]) -> WebResponse:
        """Make a POST request.
        
        Args:
            url: URL to request.
            data: Data to send in the request body.
            
        Returns:
            WebResponse object containing the response data.
            
        Raises:
            WebError: If the request fails.
        """
        try:
            validate_url(url)
            # TODO: Implement actual request functionality
            # For now, return mock response
            return WebResponse(
                url=url,
                status_code=200,
                content="Example response",
                headers={"content-type": "application/json"}
            )
        except Exception as e:
            raise WebError(f"POST request failed: {e}", url=url, data=data, cause=e)

async def fetch_url(url: str, headers: Optional[Dict[str, str]] = None) -> str:
    """Fetch content from a URL.
    
    Args:
        url: The URL to fetch.
        headers: Optional headers to include in the request.
        
    Returns:
        The content of the URL.
        
    Raises:
        WebError: If there is an error fetching the URL.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        raise WebError(f"Error fetching URL {url}: {e}")

async def post_json(url: str, data: Dict, headers: Optional[Dict[str, str]] = None) -> Dict:
    """Post JSON data to a URL.
    
    Args:
        url: The URL to post to.
        data: The data to post.
        headers: Optional headers to include in the request.
        
    Returns:
        The response from the server.
        
    Raises:
        WebError: If there is an error posting to the URL.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        raise WebError(f"Error posting to URL {url}: {e}") 