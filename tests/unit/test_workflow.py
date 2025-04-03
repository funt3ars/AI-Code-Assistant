"""
Unit tests for workflow functionality.
"""
import pytest
from unittest.mock import Mock, patch
from devin_integration.workflow import (
    Workflow,
    WorkflowError,
    WorkflowResult
)

@pytest.fixture
def workflow():
    """Create a Workflow instance for testing."""
    return Workflow()

@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    return {
        "description": "Test task",
        "requirements": ["requirement1", "requirement2"]
    }

@pytest.fixture
def mock_workflow_result():
    """Create a mock workflow result."""
    return {
        "status": "completed",
        "steps": [
            {"name": "step1", "status": "success"},
            {"name": "step2", "status": "success"}
        ],
        "output": "Task completed successfully"
    }

def test_workflow_initialization(workflow):
    """Test Workflow initialization."""
    assert workflow is not None
    assert hasattr(workflow, 'coordinator')
    assert hasattr(workflow, 'verifier')

def test_execute_workflow(workflow, sample_task, mock_workflow_result):
    """Test workflow execution."""
    with patch('devin_integration.coordinator.Coordinator.process_task', 
              return_value=mock_workflow_result):
        result = workflow.execute(sample_task)
        
        assert isinstance(result, WorkflowResult)
        assert result.status == "completed"
        assert len(result.steps) == 2
        assert result.output == "Task completed successfully"

def test_execute_workflow_error(workflow, sample_task):
    """Test error handling in workflow execution."""
    with patch('devin_integration.coordinator.Coordinator.process_task', 
              side_effect=Exception("Processing error")):
        with pytest.raises(WorkflowError):
            workflow.execute(sample_task)

def test_validate_task(workflow, sample_task):
    """Test task validation."""
    assert workflow._validate_task(sample_task) is True

def test_validate_invalid_task(workflow):
    """Test validation of invalid task."""
    invalid_task = {"invalid": "task"}
    assert workflow._validate_task(invalid_task) is False

def test_workflow_result_initialization():
    """Test WorkflowResult initialization."""
    result = WorkflowResult(
        status="completed",
        steps=[{"name": "step1", "status": "success"}],
        output="Task completed"
    )
    
    assert result.status == "completed"
    assert len(result.steps) == 1
    assert result.output == "Task completed"

def test_workflow_result_str():
    """Test WorkflowResult string representation."""
    result = WorkflowResult(
        status="completed",
        steps=[{"name": "step1", "status": "success"}],
        output="Task completed"
    )
    assert "completed" in str(result)
    assert "step1" in str(result)

def test_workflow_error():
    """Test WorkflowError."""
    error = WorkflowError("Test error")
    assert str(error) == "Test error"
    
    # Test with original exception
    original_error = Exception("Original error")
    error_with_cause = WorkflowError("Test error", cause=original_error)
    assert error_with_cause.__cause__ == original_error

def test_execute_workflow_with_verification(workflow, sample_task, mock_workflow_result):
    """Test workflow execution with verification."""
    with patch('devin_integration.coordinator.Coordinator.process_task', 
              return_value=mock_workflow_result), \
         patch('devin_integration.verification.VerificationClient.verify_task', 
              return_value=Mock(status="success", confidence=0.9)):
        result = workflow.execute(sample_task, verify=True)
        
        assert result.status == "completed"
        assert result.verified is True

def test_execute_workflow_with_options(workflow, sample_task, mock_workflow_result):
    """Test workflow execution with custom options."""
    options = {
        "timeout": 60,
        "max_retries": 3
    }
    
    with patch('devin_integration.coordinator.Coordinator.process_task', 
              return_value=mock_workflow_result):
        result = workflow.execute(sample_task, **options)
        
        assert result.status == "completed" 