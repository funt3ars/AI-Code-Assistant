"""
Planner module for high-level analysis and task breakdown.
"""
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class Planner:
    """
    Planner class responsible for high-level analysis and task breakdown.
    """
    
    def __init__(self):
        """Initialize the Planner."""
        self.logger = logger

    def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """
        Analyze a task and break it down into manageable steps.
        
        Args:
            task_description: A string describing the task to analyze
            
        Returns:
            A dictionary containing the analysis results
        """
        self.logger.info(f"Analyzing task: {task_description}")
        
        # Perform task analysis
        analysis = {
            "description": task_description,
            "steps": self._break_down_task(task_description),
            "success_criteria": self._define_success_criteria(task_description),
        }
        
        self.logger.info("Task analysis completed")
        return analysis
    
    def _break_down_task(self, task_description: str) -> List[Dict[str, Any]]:
        """
        Break down a task into smaller steps.
        
        Args:
            task_description: A string describing the task to analyze
            
        Returns:
            A list of dictionaries, each containing:
                - description: Step description
                - type: Type of step (analysis/implementation/testing)
                - estimated_complexity: Low/Medium/High
        """
        # Initial analysis step
        steps = [{
            "description": "Analyze requirements and constraints",
            "type": "analysis",
            "estimated_complexity": "Low"
        }]
        
        # Implementation steps - break down based on common patterns
        if "create" in task_description.lower():
            steps.extend([
                {
                    "description": "Design component structure",
                    "type": "implementation",
                    "estimated_complexity": "Medium"
                },
                {
                    "description": "Implement core functionality",
                    "type": "implementation",
                    "estimated_complexity": "High"
                }
            ])
        elif "fix" in task_description.lower() or "debug" in task_description.lower():
            steps.extend([
                {
                    "description": "Identify root cause",
                    "type": "analysis",
                    "estimated_complexity": "Medium"
                },
                {
                    "description": "Implement fix",
                    "type": "implementation",
                    "estimated_complexity": "Medium"
                }
            ])
        elif "test" in task_description.lower():
            steps.extend([
                {
                    "description": "Design test cases",
                    "type": "testing",
                    "estimated_complexity": "Medium"
                },
                {
                    "description": "Implement test suite",
                    "type": "testing",
                    "estimated_complexity": "Medium"
                }
            ])
        
        # Always add verification steps
        steps.extend([
            {
                "description": "Verify implementation",
                "type": "testing",
                "estimated_complexity": "Medium"
            },
            {
                "description": "Document changes",
                "type": "implementation",
                "estimated_complexity": "Low"
            }
        ])
        
        return steps
    
    def _define_success_criteria(self, task_description: str) -> List[str]:
        """
        Define success criteria for the task.
        
        Args:
            task_description: A string describing the task to analyze
            
        Returns:
            A list of success criteria strings
        """
        # Base criteria that apply to all tasks
        criteria = [
            "All specified functionality is implemented correctly",
            "Code follows project's style guidelines and best practices",
            "No regression in existing functionality"
        ]
        
        # Add specific criteria based on task type
        if "create" in task_description.lower():
            criteria.extend([
                "New component/feature is properly integrated with existing system",
                "Documentation is updated to reflect new additions",
                "Unit tests cover new functionality"
            ])
        elif "fix" in task_description.lower() or "debug" in task_description.lower():
            criteria.extend([
                "Issue is resolved without introducing new problems",
                "Root cause is documented",
                "Test case added to prevent regression"
            ])
        elif "test" in task_description.lower():
            criteria.extend([
                "Test coverage meets project requirements",
                "Edge cases are properly handled",
                "Tests are documented and maintainable"
            ])
        elif "optimize" in task_description.lower() or "performance" in task_description.lower():
            criteria.extend([
                "Performance metrics show measurable improvement",
                "Resource usage is within acceptable limits",
                "No degradation in system stability"
            ])
            
        return criteria 