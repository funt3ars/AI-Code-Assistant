"""
Unit tests for the Executor class.
"""
import pytest
from devin_integration.executor import Executor

@pytest.fixture
def executor():
    """Create an Executor instance for testing."""
    return Executor()

@pytest.fixture
def sample_task_analysis():
    """Create a sample task analysis for testing."""
    return {
        "description": "Implement new feature",
        "steps": [
            {"action": "create", "target": "file", "name": "test.py"},
            {"action": "write", "target": "code", "content": "print('Hello')"}
        ],
        "success_criteria": [
            "File is created",
            "Code is written correctly"
        ]
    }

def test_executor_initialization(executor):
    """Test that the Executor initializes correctly."""
    assert executor is not None
    assert hasattr(executor, 'logger')

def test_execute_basic(executor, sample_task_analysis):
    """Test basic task execution."""
    result = executor.execute(sample_task_analysis)
    
    assert isinstance(result, dict)
    assert "description" in result
    assert "status" in result
    assert "steps_completed" in result
    assert result["description"] == sample_task_analysis["description"]

def test_execute_empty_analysis(executor):
    """Test execution with empty task analysis."""
    with pytest.raises(ValueError):
        executor.execute({})

def test_execute_none_analysis(executor):
    """Test execution with None task analysis."""
    with pytest.raises(ValueError):
        executor.execute(None)

def test_execute_steps(executor, sample_task_analysis):
    """Test step execution functionality."""
    steps = sample_task_analysis["steps"]
    completed_steps = executor._execute_steps(steps)
    
    assert isinstance(completed_steps, list)
    assert len(completed_steps) == len(steps)
    for step in completed_steps:
        assert "status" in step
        assert "step" in step

def test_execute_single_step(executor):
    """Test single step execution."""
    step = {"action": "test", "target": "test"}
    result = executor._execute_single_step(step)
    
    assert isinstance(result, dict)
    assert "status" in result
    assert "step" in result
    assert result["step"] == step 