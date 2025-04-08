"""
Unit tests for the Coordinator class.
"""
import pytest
from devin_integration.coordinator import Coordinator

@pytest.fixture
def coordinator():
    """Create a Coordinator instance for testing."""
    return Coordinator()

@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    return {
        "description": "Implement new feature",
        "requirements": [
            "Create new file",
            "Write test cases",
            "Implement functionality"
        ]
    }

def test_coordinator_initialization(coordinator):
    """Test that the Coordinator initializes correctly."""
    assert coordinator is not None
    assert hasattr(coordinator, 'logger')
    assert hasattr(coordinator, 'planner')
    assert hasattr(coordinator, 'executor')

def test_process_task(coordinator, sample_task):
    """Test task processing functionality."""
    result = coordinator.process_task(sample_task)
    
    assert isinstance(result, dict)
    assert "task" in result
    assert "analysis" in result
    assert "execution" in result
    assert result["task"] == sample_task

def test_process_empty_task(coordinator):
    """Test processing with empty task."""
    with pytest.raises(ValueError):
        coordinator.process_task({})

def test_process_none_task(coordinator):
    """Test processing with None task."""
    with pytest.raises(ValueError):
        coordinator.process_task(None)

def test_validate_task(coordinator, sample_task):
    """Test task validation functionality."""
    assert coordinator._validate_task(sample_task) is True

def test_validate_empty_task(coordinator):
    """Test validation of empty task."""
    assert coordinator._validate_task({}) is False

def test_validate_none_task(coordinator):
    """Test validation of None task."""
    assert coordinator._validate_task(None) is False

def test_validate_invalid_task(coordinator):
    """Test validation of invalid task."""
    invalid_task = {
        "description": "Invalid task",
        "requirements": "Not a list"  # Should be a list
    }
    assert coordinator._validate_task(invalid_task) is False 