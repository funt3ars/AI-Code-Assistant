"""
Unit tests for screenshot functionality.
"""
import pytest
import os
from unittest.mock import Mock, patch
from devin_integration.screenshot import (
    ScreenshotClient,
    ScreenshotError
)

@pytest.fixture
def screenshot_client():
    """Create a ScreenshotClient instance for testing."""
    return ScreenshotClient()

@pytest.fixture
def mock_screenshot():
    """Create a mock screenshot file."""
    with open("test_screenshot.png", "wb") as f:
        f.write(b"mock image data")
    yield "test_screenshot.png"
    if os.path.exists("test_screenshot.png"):
        os.remove("test_screenshot.png")

def test_screenshot_client_initialization(screenshot_client):
    """Test ScreenshotClient initialization."""
    assert screenshot_client.timeout == 30
    assert screenshot_client.viewport_width == 1920
    assert screenshot_client.viewport_height == 1080

def test_capture_screenshot(screenshot_client, mock_screenshot):
    """Test screenshot capture functionality."""
    with patch('selenium.webdriver.Chrome') as mock_driver:
        mock_driver.return_value.get_screenshot_as_file.return_value = True
        mock_driver.return_value.quit.return_value = None
        
        result = screenshot_client.capture_screenshot(
            "https://example.com",
            "test_screenshot.png"
        )
        
        assert result == "test_screenshot.png"
        assert os.path.exists("test_screenshot.png")

def test_capture_screenshot_error(screenshot_client):
    """Test error handling in screenshot capture."""
    with patch('selenium.webdriver.Chrome', side_effect=Exception("Browser error")):
        with pytest.raises(ScreenshotError):
            screenshot_client.capture_screenshot(
                "https://example.com",
                "test_screenshot.png"
            )

def test_validate_url(screenshot_client):
    """Test URL validation."""
    assert screenshot_client._validate_url("https://example.com") is True
    assert screenshot_client._validate_url("http://example.com") is True
    assert screenshot_client._validate_url("ftp://example.com") is False
    assert screenshot_client._validate_url("not-a-url") is False

def test_validate_output_path(screenshot_client):
    """Test output path validation."""
    assert screenshot_client._validate_output_path("test.png") is True
    assert screenshot_client._validate_output_path("test.jpg") is True
    assert screenshot_client._validate_output_path("test.txt") is False
    assert screenshot_client._validate_output_path("/invalid/path/test.png") is False

def test_screenshot_error():
    """Test ScreenshotError."""
    error = ScreenshotError("Test error")
    assert str(error) == "Test error"
    
    # Test with original exception
    original_error = Exception("Original error")
    error_with_cause = ScreenshotError("Test error", cause=original_error)
    assert error_with_cause.__cause__ == original_error

def test_capture_screenshot_with_options(screenshot_client, mock_screenshot):
    """Test screenshot capture with custom options."""
    options = {
        "viewport_width": 800,
        "viewport_height": 600,
        "timeout": 10
    }
    
    with patch('selenium.webdriver.Chrome') as mock_driver:
        mock_driver.return_value.get_screenshot_as_file.return_value = True
        mock_driver.return_value.quit.return_value = None
        
        result = screenshot_client.capture_screenshot(
            "https://example.com",
            "test_screenshot.png",
            **options
        )
        
        assert result == "test_screenshot.png"
        assert os.path.exists("test_screenshot.png")
        mock_driver.return_value.set_window_size.assert_called_with(800, 600) 