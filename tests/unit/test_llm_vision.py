"""
Unit tests for LLM vision functionality.
"""
import pytest
import os
from unittest.mock import Mock, patch
from devin_integration.llm_vision import (
    LLMVisionClient,
    LLMVisionError,
    LLMVisionResponse
)

@pytest.fixture
def llm_vision_client():
    """Create an LLMVisionClient instance for testing."""
    return LLMVisionClient(api_key="test_key")

@pytest.fixture
def mock_image():
    """Create a mock image file."""
    with open("test_image.png", "wb") as f:
        f.write(b"mock image data")
    yield "test_image.png"
    if os.path.exists("test_image.png"):
        os.remove("test_image.png")

@pytest.fixture
def mock_vision_response():
    """Create a mock vision response."""
    return {
        "choices": [
            {
                "message": {
                    "content": "Test vision response",
                    "role": "assistant"
                }
            }
        ]
    }

def test_llm_vision_client_initialization(llm_vision_client):
    """Test LLMVisionClient initialization."""
    assert llm_vision_client.api_key == "test_key"
    assert llm_vision_client.model == "gpt-4-vision-preview"
    assert llm_vision_client.max_tokens == 1000

def test_analyze_image(llm_vision_client, mock_image, mock_vision_response):
    """Test image analysis functionality."""
    with patch('openai.ChatCompletion.create', return_value=mock_vision_response):
        response = llm_vision_client.analyze_image(
            mock_image,
            "What do you see in this image?"
        )
        
        assert isinstance(response, LLMVisionResponse)
        assert response.content == "Test vision response"
        assert response.role == "assistant"

def test_analyze_image_error(llm_vision_client, mock_image):
    """Test error handling in image analysis."""
    with patch('openai.ChatCompletion.create', side_effect=Exception("API error")):
        with pytest.raises(LLMVisionError):
            llm_vision_client.analyze_image(
                mock_image,
                "What do you see in this image?"
            )

def test_validate_image(llm_vision_client, mock_image):
    """Test image validation."""
    assert llm_vision_client._validate_image(mock_image) is True

def test_validate_invalid_image(llm_vision_client):
    """Test validation of invalid image."""
    assert llm_vision_client._validate_image("nonexistent.png") is False
    assert llm_vision_client._validate_image("test.txt") is False

def test_validate_response(llm_vision_client, mock_vision_response):
    """Test response validation."""
    assert llm_vision_client._validate_response(mock_vision_response) is True

def test_validate_invalid_response(llm_vision_client):
    """Test validation of invalid response."""
    invalid_response = {"invalid": "response"}
    assert llm_vision_client._validate_response(invalid_response) is False

def test_llm_vision_response_initialization():
    """Test LLMVisionResponse initialization."""
    response = LLMVisionResponse("Test content", "assistant")
    
    assert response.content == "Test content"
    assert response.role == "assistant"

def test_llm_vision_response_str():
    """Test LLMVisionResponse string representation."""
    response = LLMVisionResponse("Test content", "assistant")
    assert str(response) == "Test content"

def test_llm_vision_error():
    """Test LLMVisionError."""
    error = LLMVisionError("Test error")
    assert str(error) == "Test error"
    
    # Test with original exception
    original_error = Exception("Original error")
    error_with_cause = LLMVisionError("Test error", cause=original_error)
    assert error_with_cause.__cause__ == original_error

def test_analyze_image_with_options(llm_vision_client, mock_image, mock_vision_response):
    """Test image analysis with custom options."""
    options = {
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    with patch('openai.ChatCompletion.create', return_value=mock_vision_response) as mock_create:
        llm_vision_client.analyze_image(
            mock_image,
            "What do you see in this image?",
            **options
        )
        
        mock_create.assert_called_once()
        assert mock_create.call_args[1]["max_tokens"] == 500
        assert mock_create.call_args[1]["temperature"] == 0.7 