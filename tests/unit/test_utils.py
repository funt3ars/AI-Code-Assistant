"""
Unit tests for utility functions.
"""
import pytest
from devin_integration.utils import (
    validate_task_structure,
    format_task_result,
    log_task_progress
)

@pytest.fixture
def valid_task():
    """Create a valid task structure for testing."""
    return {
        "description": "Test task",
        "requirements": ["Requirement 1", "Requirement 2"],
        "priority": "high"
    }

@pytest.fixture
def invalid_task():
    """Create an invalid task structure for testing."""
    return {
        "description": "Invalid task",
        "requirements": "Not a list"  # Should be a list
    }

def test_validate_task_structure_valid(valid_task):
    """Test validation of valid task structure."""
    assert validate_task_structure(valid_task) is True

def test_validate_task_structure_invalid(invalid_task):
    """Test validation of invalid task structure."""
    assert validate_task_structure(invalid_task) is False

def test_validate_task_structure_empty():
    """Test validation of empty task structure."""
    assert validate_task_structure({}) is False

def test_validate_task_structure_none():
    """Test validation of None task structure."""
    assert validate_task_structure(None) is False

def test_format_task_result():
    """Test task result formatting."""
    task = {"description": "Test task"}
    analysis = {"steps": ["Step 1", "Step 2"]}
    execution = {"status": "completed"}
    
    result = format_task_result(task, analysis, execution)
    
    assert isinstance(result, dict)
    assert "task" in result
    assert "analysis" in result
    assert "execution" in result
    assert result["task"] == task
    assert result["analysis"] == analysis
    assert result["execution"] == execution

def test_log_task_progress(caplog):
    """Test task progress logging."""
    task_id = "test-123"
    status = "in_progress"
    message = "Processing step 1"
    
    log_task_progress(task_id, status, message)
    
    assert f"Task {task_id}" in caplog.text
    assert status in caplog.text
    assert message in caplog.text 