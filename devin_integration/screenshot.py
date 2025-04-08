"""Screenshot functionality for devin_integration."""

import os
import re
from pathlib import Path
from typing import Optional, Union
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .errors import ScreenshotError
from .utils import validate_url, validate_file_path

def take_screenshot(url: str, output_path: str, width: int = 1920, height: int = 1080) -> str:
    """Take a screenshot of a webpage.
    
    Args:
        url: URL of the webpage to screenshot.
        output_path: Path where to save the screenshot.
        width: Viewport width in pixels.
        height: Viewport height in pixels.
        
    Returns:
        Path to the saved screenshot.
        
    Raises:
        ScreenshotError: If the screenshot fails.
    """
    try:
        validate_url(url)
        validate_file_path(output_path)
        
        # TODO: Implement actual screenshot functionality
        # For now, just create an empty file
        Path(output_path).touch()
        return output_path
        
    except Exception as e:
        raise ScreenshotError(
            f"Failed to take screenshot: {e}",
            url=url,
            output_path=output_path,
            cause=e
        )

class ScreenshotClient:
    """Client for taking screenshots of web pages."""
    
    def __init__(
        self,
        timeout: int = 30,
        viewport_width: int = 1920,
        viewport_height: int = 1080
    ):
        """Initialize the screenshot client.
        
        Args:
            timeout: Timeout in seconds for page load.
            viewport_width: Width of the viewport in pixels.
            viewport_height: Height of the viewport in pixels.
        """
        self.timeout = timeout
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

    def _validate_url(self, url: str) -> bool:
        """Validate a URL.
        
        Args:
            url: The URL to validate.
            
        Returns:
            True if the URL is valid, False otherwise.
        """
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))

    def _validate_output_path(self, path: Union[str, Path]) -> bool:
        """Validate an output path.
        
        Args:
            path: The path to validate.
            
        Returns:
            True if the path is valid, False otherwise.
        """
        path = Path(path)
        if not path.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            return False
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False

    def capture_screenshot(
        self,
        url: str,
        output_path: Union[str, Path],
        **options
    ) -> str:
        """Capture a screenshot of a webpage.
        
        Args:
            url: The URL to capture.
            output_path: Where to save the screenshot.
            **options: Additional options:
                - viewport_width: Width of the viewport in pixels.
                - viewport_height: Height of the viewport in pixels.
                - timeout: Timeout in seconds for page load.
            
        Returns:
            Path to the saved screenshot.
            
        Raises:
            ScreenshotError: If there is an error taking the screenshot.
        """
        try:
            if not self._validate_url(url):
                raise ScreenshotError(f"Invalid URL: {url}")
                
            if not self._validate_output_path(output_path):
                raise ScreenshotError(f"Invalid output path: {output_path}")
            
            # Get options
            viewport_width = options.get('viewport_width', self.viewport_width)
            viewport_height = options.get('viewport_height', self.viewport_height)
            timeout = options.get('timeout', self.timeout)
            
            # Set up Chrome options
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            # Create driver
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_window_size(viewport_width, viewport_height)
            driver.set_page_load_timeout(timeout)
            
            try:
                # Navigate to URL and take screenshot
                driver.get(url)
                driver.get_screenshot_as_file(str(output_path))
                return str(output_path)
            finally:
                driver.quit()
        except Exception as e:
            raise ScreenshotError(f"Error taking screenshot: {e}", cause=e) 