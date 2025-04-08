"""
Unit tests for the Planner class.
"""
import pytest
from devin_integration.planner import Planner

@pytest.fixture
def planner():
    """Create a Planner instance for testing."""
    return Planner()

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

def test_planner_initialization(planner):
    """Test that the Planner initializes correctly."""
    assert planner is not None
    assert hasattr(planner, 'logger')

def test_analyze_task(planner, sample_task):
    """Test task analysis functionality."""
    analysis = planner.analyze_task(sample_task)
    
    assert isinstance(analysis, dict)
    assert "description" in analysis
    assert "steps" in analysis
    assert "success_criteria" in analysis
    assert analysis["description"] == sample_task["description"]

def test_analyze_empty_task(planner):
    """Test analysis with empty task."""
    with pytest.raises(ValueError):
        planner.analyze_task({})

def test_analyze_none_task(planner):
    """Test analysis with None task."""
    with pytest.raises(ValueError):
        planner.analyze_task(None)

def test_break_down_task(planner, sample_task):
    """Test task breakdown functionality."""
    steps = planner._break_down_task(sample_task)
    
    assert isinstance(steps, list)
    assert len(steps) > 0
    for step in steps:
        assert "action" in step
        assert "target" in step

def test_define_success_criteria(planner, sample_task):
    """Test success criteria definition."""
    criteria = planner._define_success_criteria(sample_task)
    
    assert isinstance(criteria, list)
    assert len(criteria) > 0
    for criterion in criteria:
        assert isinstance(criterion, str) 