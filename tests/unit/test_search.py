"""
Unit tests for search functionality.
"""
import pytest
from unittest.mock import Mock, patch
from devin_integration.search import (
    SearchClient,
    SearchError,
    SearchResult
)

@pytest.fixture
def search_client():
    """Create a SearchClient instance for testing."""
    return SearchClient(api_key="test_key")

@pytest.fixture
def mock_search_results():
    """Create mock search results."""
    return {
        "items": [
            {
                "title": "Test Result 1",
                "link": "https://example.com/1",
                "snippet": "Test snippet 1"
            },
            {
                "title": "Test Result 2",
                "link": "https://example.com/2",
                "snippet": "Test snippet 2"
            }
        ]
    }

def test_search_client_initialization(search_client):
    """Test SearchClient initialization."""
    assert search_client.api_key == "test_key"
    assert search_client.max_results == 10
    assert search_client.timeout == 30

def test_search(search_client, mock_search_results):
    """Test search functionality."""
    with patch('requests.get', return_value=Mock(json=lambda: mock_search_results)):
        results = search_client.search("test query")
        
        assert isinstance(results, list)
        assert len(results) == 2
        assert all(isinstance(r, SearchResult) for r in results)
        assert results[0].title == "Test Result 1"
        assert results[1].title == "Test Result 2"

def test_search_error(search_client):
    """Test error handling in search."""
    with patch('requests.get', side_effect=Exception("API error")):
        with pytest.raises(SearchError):
            search_client.search("test query")

def test_validate_results(search_client, mock_search_results):
    """Test search results validation."""
    assert search_client._validate_results(mock_search_results) is True

def test_validate_invalid_results(search_client):
    """Test validation of invalid search results."""
    invalid_results = {"invalid": "results"}
    assert search_client._validate_results(invalid_results) is False

def test_search_result_initialization():
    """Test SearchResult initialization."""
    result = SearchResult(
        title="Test Title",
        url="https://example.com",
        snippet="Test snippet"
    )
    
    assert result.title == "Test Title"
    assert result.url == "https://example.com"
    assert result.snippet == "Test snippet"

def test_search_result_str():
    """Test SearchResult string representation."""
    result = SearchResult(
        title="Test Title",
        url="https://example.com",
        snippet="Test snippet"
    )
    assert str(result) == "Test Title (https://example.com)"

def test_search_error():
    """Test SearchError."""
    error = SearchError("Test error")
    assert str(error) == "Test error"
    
    # Test with original exception
    original_error = Exception("Original error")
    error_with_cause = SearchError("Test error", cause=original_error)
    assert error_with_cause.__cause__ == original_error

def test_search_with_filters(search_client, mock_search_results):
    """Test search with filters."""
    filters = {
        "site": "example.com",
        "date": "last month"
    }
    
    with patch('requests.get', return_value=Mock(json=lambda: mock_search_results)) as mock_get:
        search_client.search("test query", filters=filters)
        
        mock_get.assert_called_once()
        assert "site:example.com" in mock_get.call_args[1]["params"]["q"]
        assert "date:last month" in mock_get.call_args[1]["params"]["q"] 