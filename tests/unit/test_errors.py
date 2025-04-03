"""
Unit tests for error handling.
"""
import pytest
from devin_integration.errors import (
    TaskValidationError,
    TaskExecutionError,
    TaskAnalysisError
)

def test_task_validation_error():
    """Test TaskValidationError."""
    error = TaskValidationError("Invalid task structure")
    
    assert isinstance(error, Exception)
    assert str(error) == "Invalid task structure"
    assert error.task is None
    
    # Test with task context
    task = {"description": "Test task"}
    error_with_task = TaskValidationError("Invalid task", task=task)
    
    assert error_with_task.task == task

def test_task_execution_error():
    """Test TaskExecutionError."""
    error = TaskExecutionError("Execution failed")
    
    assert isinstance(error, Exception)
    assert str(error) == "Execution failed"
    assert error.step is None
    assert error.task is None
    
    # Test with step and task context
    step = {"action": "test"}
    task = {"description": "Test task"}
    error_with_context = TaskExecutionError(
        "Step failed",
        step=step,
        task=task
    )
    
    assert error_with_context.step == step
    assert error_with_context.task == task

def test_task_analysis_error():
    """Test TaskAnalysisError."""
    error = TaskAnalysisError("Analysis failed")
    
    assert isinstance(error, Exception)
    assert str(error) == "Analysis failed"
    assert error.task is None
    
    # Test with task context
    task = {"description": "Test task"}
    error_with_task = TaskAnalysisError("Analysis failed", task=task)
    
    assert error_with_task.task == task

def test_error_chain():
    """Test error chaining."""
    try:
        try:
            raise ValueError("Original error")
        except ValueError as e:
            raise TaskExecutionError("Execution failed") from e
    except TaskExecutionError as e:
        assert isinstance(e.__cause__, ValueError)
        assert str(e.__cause__) == "Original error"

def test_error_context():
    """Test error context preservation."""
    task = {"description": "Test task"}
    step = {"action": "test"}
    
    try:
        raise TaskExecutionError("Failed", task=task, step=step)
    except TaskExecutionError as e:
        assert e.task == task
        assert e.step == step
        assert "task" in str(e)
        assert "step" in str(e) 