"""
Unit tests for verification functionality.
"""
import pytest
from unittest.mock import Mock, patch
from devin_integration.verification import (
    VerificationClient,
    VerificationError,
    VerificationResult
)

@pytest.fixture
def verification_client():
    """Create a VerificationClient instance for testing."""
    return VerificationClient()

@pytest.fixture
def mock_verification_result():
    """Create a mock verification result."""
    return {
        "status": "success",
        "confidence": 0.95,
        "details": {
            "matches": ["criteria1", "criteria2"],
            "mismatches": ["criteria3"]
        }
    }

def test_verification_client_initialization(verification_client):
    """Test VerificationClient initialization."""
    assert verification_client.min_confidence == 0.8
    assert verification_client.timeout == 30

def test_verify_task(verification_client, mock_verification_result):
    """Test task verification functionality."""
    task = {"description": "Test task"}
    criteria = ["criteria1", "criteria2", "criteria3"]
    
    with patch('devin_integration.llm.LLMClient.generate_response', 
              return_value=Mock(content=str(mock_verification_result))):
        result = verification_client.verify_task(task, criteria)
        
        assert isinstance(result, VerificationResult)
        assert result.status == "success"
        assert result.confidence == 0.95
        assert len(result.matches) == 2
        assert len(result.mismatches) == 1

def test_verify_task_error(verification_client):
    """Test error handling in task verification."""
    task = {"description": "Test task"}
    criteria = ["criteria1"]
    
    with patch('devin_integration.llm.LLMClient.generate_response', 
              side_effect=Exception("LLM error")):
        with pytest.raises(VerificationError):
            verification_client.verify_task(task, criteria)

def test_validate_verification_result(verification_client, mock_verification_result):
    """Test verification result validation."""
    assert verification_client._validate_verification_result(mock_verification_result) is True

def test_validate_invalid_result(verification_client):
    """Test validation of invalid verification result."""
    invalid_result = {"invalid": "result"}
    assert verification_client._validate_verification_result(invalid_result) is False

def test_verification_result_initialization():
    """Test VerificationResult initialization."""
    result = VerificationResult(
        status="success",
        confidence=0.9,
        matches=["criteria1"],
        mismatches=["criteria2"]
    )
    
    assert result.status == "success"
    assert result.confidence == 0.9
    assert result.matches == ["criteria1"]
    assert result.mismatches == ["criteria2"]

def test_verification_result_str():
    """Test VerificationResult string representation."""
    result = VerificationResult(
        status="success",
        confidence=0.9,
        matches=["criteria1"],
        mismatches=["criteria2"]
    )
    assert "success" in str(result)
    assert "0.9" in str(result)

def test_verification_error():
    """Test VerificationError."""
    error = VerificationError("Test error")
    assert str(error) == "Test error"
    
    # Test with original exception
    original_error = Exception("Original error")
    error_with_cause = VerificationError("Test error", cause=original_error)
    assert error_with_cause.__cause__ == original_error

def test_verify_task_with_options(verification_client, mock_verification_result):
    """Test task verification with custom options."""
    task = {"description": "Test task"}
    criteria = ["criteria1"]
    options = {
        "min_confidence": 0.7,
        "timeout": 10
    }
    
    with patch('devin_integration.llm.LLMClient.generate_response', 
              return_value=Mock(content=str(mock_verification_result))):
        result = verification_client.verify_task(task, criteria, **options)
        
        assert result.confidence >= 0.7 