"""
Unit tests for LLM integration.
"""
import pytest
from unittest.mock import Mock, patch
from devin_integration.llm import (
    LLMClient,
    LLMError,
    LLMResponse
)

@pytest.fixture
def llm_client():
    """Create an LLMClient instance for testing."""
    return LLMClient(api_key="test_key")

@pytest.fixture
def mock_response():
    """Create a mock LLM response."""
    return {
        "choices": [
            {
                "message": {
                    "content": "Test response",
                    "role": "assistant"
                }
            }
        ]
    }

def test_llm_client_initialization(llm_client):
    """Test LLMClient initialization."""
    assert llm_client.api_key == "test_key"
    assert llm_client.model == "gpt-4"
    assert llm_client.max_tokens == 1000

def test_generate_response(llm_client, mock_response):
    """Test response generation."""
    with patch('openai.ChatCompletion.create', return_value=mock_response):
        response = llm_client.generate_response("Test prompt")
        
        assert isinstance(response, LLMResponse)
        assert response.content == "Test response"
        assert response.role == "assistant"

def test_generate_response_error(llm_client):
    """Test error handling in response generation."""
    with patch('openai.ChatCompletion.create', side_effect=Exception("API error")):
        with pytest.raises(LLMError):
            llm_client.generate_response("Test prompt")

def test_validate_response(llm_client, mock_response):
    """Test response validation."""
    assert llm_client._validate_response(mock_response) is True

def test_validate_invalid_response(llm_client):
    """Test validation of invalid response."""
    invalid_response = {"invalid": "response"}
    assert llm_client._validate_response(invalid_response) is False

def test_format_prompt(llm_client):
    """Test prompt formatting."""
    prompt = "Test prompt"
    formatted = llm_client._format_prompt(prompt)
    
    assert isinstance(formatted, list)
    assert len(formatted) == 1
    assert formatted[0]["role"] == "user"
    assert formatted[0]["content"] == prompt

def test_llm_response_initialization():
    """Test LLMResponse initialization."""
    response = LLMResponse("Test content", "assistant")
    
    assert response.content == "Test content"
    assert response.role == "assistant"

def test_llm_response_str():
    """Test LLMResponse string representation."""
    response = LLMResponse("Test content", "assistant")
    assert str(response) == "Test content"

def test_llm_error():
    """Test LLMError."""
    error = LLMError("Test error")
    assert str(error) == "Test error"
    
    # Test with original exception
    original_error = Exception("Original error")
    error_with_cause = LLMError("Test error", cause=original_error)
    assert error_with_cause.__cause__ == original_error 