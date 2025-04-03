"""
Unit tests for web functionality.
"""
import pytest
from unittest.mock import Mock, patch
from devin_integration.web import (
    WebClient,
    WebError,
    WebResponse
)

@pytest.fixture
def web_client():
    """Create a WebClient instance for testing."""
    return WebClient()

@pytest.fixture
def mock_response():
    """Create a mock web response."""
    return Mock(
        status_code=200,
        text="Test response",
        headers={"Content-Type": "text/plain"}
    )

def test_web_client_initialization(web_client):
    """Test WebClient initialization."""
    assert web_client.timeout == 30
    assert web_client.max_retries == 3

def test_make_request(web_client, mock_response):
    """Test making HTTP requests."""
    with patch('requests.Session.request', return_value=mock_response):
        response = web_client.make_request("GET", "https://example.com")
        
        assert isinstance(response, WebResponse)
        assert response.status_code == 200
        assert response.text == "Test response"
        assert response.headers["Content-Type"] == "text/plain"

def test_make_request_error(web_client):
    """Test error handling in HTTP requests."""
    with patch('requests.Session.request', side_effect=Exception("Network error")):
        with pytest.raises(WebError):
            web_client.make_request("GET", "https://example.com")

def test_validate_response(web_client, mock_response):
    """Test response validation."""
    assert web_client._validate_response(mock_response) is True

def test_validate_invalid_response(web_client):
    """Test validation of invalid response."""
    invalid_response = Mock(status_code=500)
    assert web_client._validate_response(invalid_response) is False

def test_retry_logic(web_client):
    """Test request retry logic."""
    mock_responses = [
        Mock(status_code=500),
        Mock(status_code=500),
        Mock(status_code=200, text="Success")
    ]
    
    with patch('requests.Session.request', side_effect=mock_responses):
        response = web_client.make_request("GET", "https://example.com")
        
        assert response.status_code == 200
        assert response.text == "Success"

def test_web_response_initialization():
    """Test WebResponse initialization."""
    response = WebResponse(200, "Test content", {"Content-Type": "text/plain"})
    
    assert response.status_code == 200
    assert response.text == "Test content"
    assert response.headers["Content-Type"] == "text/plain"

def test_web_response_str():
    """Test WebResponse string representation."""
    response = WebResponse(200, "Test content")
    assert str(response) == "Test content"

def test_web_error():
    """Test WebError."""
    error = WebError("Test error")
    assert str(error) == "Test error"
    
    # Test with original exception
    original_error = Exception("Original error")
    error_with_cause = WebError("Test error", cause=original_error)
    assert error_with_cause.__cause__ == original_error

def test_request_headers(web_client):
    """Test request headers."""
    headers = {"Authorization": "Bearer token"}
    web_client.set_headers(headers)
    
    with patch('requests.Session.request') as mock_request:
        web_client.make_request("GET", "https://example.com")
        mock_request.assert_called_once()
        assert mock_request.call_args[1]["headers"] == headers 