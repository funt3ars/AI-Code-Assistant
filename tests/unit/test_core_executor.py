"""
Unit tests for core executor functionality.
"""
import pytest
from unittest.mock import Mock, patch
from devin_integration.core.executor import (
    CoreExecutor,
    ExecutionError,
    ExecutionResult
)

@pytest.fixture
def core_executor():
    """Create a CoreExecutor instance for testing."""
    return CoreExecutor()

@pytest.fixture
def sample_plan():
    """Create a sample execution plan for testing."""
    return {
        "steps": [
            {
                "id": 1,
                "description": "Create new file",
                "action": "create_file",
                "params": {"path": "test.py"}
            },
            {
                "id": 2,
                "description": "Write test cases",
                "action": "write_code",
                "params": {"content": "def test_func(): pass"}
            }
        ],
        "dependencies": [
            {"from": 1, "to": 2}
        ]
    }

@pytest.fixture
def mock_execution_result():
    """Create a mock execution result."""
    return {
        "status": "success",
        "steps_completed": [
            {
                "id": 1,
                "status": "success",
                "output": "File created: test.py"
            },
            {
                "id": 2,
                "status": "success",
                "output": "Code written successfully"
            }
        ],
        "total_time": "1h15m"
    }

def test_core_executor_initialization(core_executor):
    """Test CoreExecutor initialization."""
    assert core_executor is not None
    assert hasattr(core_executor, 'logger')
    assert hasattr(core_executor, 'file_manager')

def test_execute_plan(core_executor, sample_plan, mock_execution_result):
    """Test plan execution."""
    with patch('devin_integration.core.executor.CoreExecutor._execute_step', 
              return_value={"status": "success", "output": "Step completed"}):
        result = core_executor.execute_plan(sample_plan)
        
        assert isinstance(result, ExecutionResult)
        assert result.status == "success"
        assert len(result.steps_completed) == 2
        assert all(step["status"] == "success" for step in result.steps_completed)

def test_execute_plan_error(core_executor, sample_plan):
    """Test error handling in plan execution."""
    with patch('devin_integration.core.executor.CoreExecutor._execute_step', 
              side_effect=Exception("Execution error")):
        with pytest.raises(ExecutionError):
            core_executor.execute_plan(sample_plan)

def test_validate_plan(core_executor, sample_plan):
    """Test plan validation."""
    assert core_executor._validate_plan(sample_plan) is True

def test_validate_invalid_plan(core_executor):
    """Test validation of invalid plan."""
    invalid_plan = {"invalid": "plan"}
    assert core_executor._validate_plan(invalid_plan) is False

def test_execute_step(core_executor):
    """Test single step execution."""
    step = {
        "id": 1,
        "description": "Test step",
        "action": "test_action",
        "params": {"param1": "value1"}
    }
    
    with patch('devin_integration.core.executor.CoreExecutor._execute_action', 
              return_value={"status": "success", "output": "Action completed"}):
        result = core_executor._execute_step(step)
        
        assert isinstance(result, dict)
        assert result["status"] == "success"
        assert result["output"] == "Action completed"

def test_execute_step_error(core_executor):
    """Test error handling in step execution."""
    step = {
        "id": 1,
        "description": "Test step",
        "action": "test_action",
        "params": {"param1": "value1"}
    }
    
    with patch('devin_integration.core.executor.CoreExecutor._execute_action', 
              side_effect=Exception("Action error")):
        with pytest.raises(ExecutionError):
            core_executor._execute_step(step)

def test_execution_result_initialization():
    """Test ExecutionResult initialization."""
    steps = [
        {"id": 1, "status": "success", "output": "Step 1 completed"}
    ]
    result = ExecutionResult("success", steps, "1h")
    
    assert result.status == "success"
    assert result.steps_completed == steps
    assert result.total_time == "1h"

def test_execution_result_str():
    """Test ExecutionResult string representation."""
    steps = [
        {"id": 1, "status": "success", "output": "Step 1 completed"}
    ]
    result = ExecutionResult("success", steps, "1h")
    assert "success" in str(result)
    assert "Step 1" in str(result)
    assert "1h" in str(result)

def test_execution_error():
    """Test ExecutionError."""
    error = ExecutionError("Test error")
    assert str(error) == "Test error"
    
    # Test with original exception
    original_error = Exception("Original error")
    error_with_cause = ExecutionError("Test error", cause=original_error)
    assert error_with_cause.__cause__ == original_error

def test_execute_plan_with_options(core_executor, sample_plan, mock_execution_result):
    """Test plan execution with custom options."""
    options = {
        "timeout": 60,
        "max_retries": 3
    }
    
    with patch('devin_integration.core.executor.CoreExecutor._execute_step', 
              return_value={"status": "success", "output": "Step completed"}):
        result = core_executor.execute_plan(sample_plan, **options)
        
        assert result.status == "success"
        assert len(result.steps_completed) == len(sample_plan["steps"]) 