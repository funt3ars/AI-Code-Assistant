"""
Unit tests for core planner functionality.
"""
import pytest
from unittest.mock import Mock, patch
from devin_integration.core.planner import (
    CorePlanner,
    PlanningError,
    PlanningResult
)

@pytest.fixture
def core_planner():
    """Create a CorePlanner instance for testing."""
    return CorePlanner()

@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    return {
        "description": "Implement new feature",
        "requirements": [
            "Create new file",
            "Write test cases",
            "Implement functionality"
        ],
        "priority": "high"
    }

@pytest.fixture
def mock_planning_result():
    """Create a mock planning result."""
    return {
        "status": "success",
        "plan": {
            "steps": [
                {
                    "id": 1,
                    "description": "Create new file",
                    "estimated_time": "30m"
                },
                {
                    "id": 2,
                    "description": "Write test cases",
                    "estimated_time": "1h"
                }
            ],
            "estimated_total_time": "1h30m",
            "dependencies": [
                {"from": 1, "to": 2}
            ]
        }
    }

def test_core_planner_initialization(core_planner):
    """Test CorePlanner initialization."""
    assert core_planner is not None
    assert hasattr(core_planner, 'llm_client')
    assert hasattr(core_planner, 'logger')

def test_create_plan(core_planner, sample_task, mock_planning_result):
    """Test plan creation."""
    with patch('devin_integration.llm.LLMClient.generate_response', 
              return_value=Mock(content=str(mock_planning_result))):
        result = core_planner.create_plan(sample_task)
        
        assert isinstance(result, PlanningResult)
        assert result.status == "success"
        assert len(result.plan["steps"]) == 2
        assert result.plan["estimated_total_time"] == "1h30m"

def test_create_plan_error(core_planner, sample_task):
    """Test error handling in plan creation."""
    with patch('devin_integration.llm.LLMClient.generate_response', 
              side_effect=Exception("LLM error")):
        with pytest.raises(PlanningError):
            core_planner.create_plan(sample_task)

def test_validate_task(core_planner, sample_task):
    """Test task validation."""
    assert core_planner._validate_task(sample_task) is True

def test_validate_invalid_task(core_planner):
    """Test validation of invalid task."""
    invalid_task = {"invalid": "task"}
    assert core_planner._validate_task(invalid_task) is False

def test_validate_plan(core_planner, mock_planning_result):
    """Test plan validation."""
    assert core_planner._validate_plan(mock_planning_result) is True

def test_validate_invalid_plan(core_planner):
    """Test validation of invalid plan."""
    invalid_plan = {"invalid": "plan"}
    assert core_planner._validate_plan(invalid_plan) is False

def test_planning_result_initialization():
    """Test PlanningResult initialization."""
    plan = {
        "steps": [{"id": 1, "description": "Step 1"}],
        "estimated_total_time": "1h"
    }
    result = PlanningResult("success", plan)
    
    assert result.status == "success"
    assert result.plan == plan

def test_planning_result_str():
    """Test PlanningResult string representation."""
    plan = {
        "steps": [{"id": 1, "description": "Step 1"}],
        "estimated_total_time": "1h"
    }
    result = PlanningResult("success", plan)
    assert "success" in str(result)
    assert "Step 1" in str(result)

def test_planning_error():
    """Test PlanningError."""
    error = PlanningError("Test error")
    assert str(error) == "Test error"
    
    # Test with original exception
    original_error = Exception("Original error")
    error_with_cause = PlanningError("Test error", cause=original_error)
    assert error_with_cause.__cause__ == original_error

def test_create_plan_with_options(core_planner, sample_task, mock_planning_result):
    """Test plan creation with custom options."""
    options = {
        "max_steps": 5,
        "min_confidence": 0.8
    }
    
    with patch('devin_integration.llm.LLMClient.generate_response', 
              return_value=Mock(content=str(mock_planning_result))):
        result = core_planner.create_plan(sample_task, **options)
        
        assert result.status == "success"
        assert len(result.plan["steps"]) <= options["max_steps"] 