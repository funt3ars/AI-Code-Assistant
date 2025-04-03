"""
Planner Module

Handles high-level analysis, task breakdown, and strategic planning.
"""

from typing import Dict, List, Any, Optional
import json
from pathlib import Path
import logging
from ..llm import LLMClient
from ..errors import PlanningError

class PlanningResult:
    """Class representing a planning result."""
    
    def __init__(
        self,
        status: str,
        plan: Dict[str, Any],
        error: Optional[Exception] = None
    ):
        """Initialize the result.
        
        Args:
            status: Planning status ("success" or "failure").
            plan: The generated plan.
            error: Error that occurred during planning, if any.
        """
        self.status = status
        self.plan = plan
        self.error = error
    
    def __str__(self) -> str:
        """Return a string representation of the result."""
        return (
            f"PlanningResult(status={self.status}, "
            f"steps={len(self.plan['steps'])}, "
            f"estimated_time={self.plan['estimated_total_time']})"
        )

class Planner:
    """Handles high-level analysis and task planning."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.lessons_file = self.project_root / ".cursorrules"
        self.current_status = {
            "background": "",
            "challenges": [],
            "success_criteria": [],
            "task_breakdown": [],
            "current_status": "",
            "next_steps": [],
            "feedback": []
        }
    
    def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """Analyze a task and break it down into manageable steps."""
        # Load existing lessons
        lessons = self._load_lessons()
        
        # Update background
        self.current_status["background"] = task_description
        
        # Perform analysis
        self.current_status["challenges"] = self._identify_challenges(task_description)
        self.current_status["success_criteria"] = self._define_success_criteria()
        self.current_status["task_breakdown"] = self._break_down_tasks()
        
        return self.current_status
    
    def update_status(self, status_update: Dict[str, Any]) -> None:
        """Update the current status with new information."""
        self.current_status.update(status_update)
        self._save_status()
    
    def _load_lessons(self) -> Dict[str, Any]:
        """Load lessons from the .cursorrules file."""
        if self.lessons_file.exists():
            with open(self.lessons_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_status(self) -> None:
        """Save current status to the .cursorrules file."""
        with open(self.lessons_file, 'w') as f:
            json.dump(self.current_status, f, indent=2)
    
    def _identify_challenges(self, task_description: str) -> List[str]:
        """Identify potential challenges in the task."""
        # This would be enhanced with actual AI analysis
        return [
            "Understanding project requirements",
            "Identifying dependencies",
            "Ensuring code quality",
            "Maintaining test coverage"
        ]
    
    def _define_success_criteria(self) -> List[str]:
        """Define success criteria for the task."""
        return [
            "All tests pass",
            "Code meets quality standards",
            "Documentation is updated",
            "Lessons are recorded"
        ]
    
    def _break_down_tasks(self) -> List[Dict[str, Any]]:
        """Break down the task into manageable steps."""
        return [
            {
                "step": 1,
                "description": "Analyze requirements",
                "status": "pending"
            },
            {
                "step": 2,
                "description": "Design solution",
                "status": "pending"
            },
            {
                "step": 3,
                "description": "Implement changes",
                "status": "pending"
            },
            {
                "step": 4,
                "description": "Run tests",
                "status": "pending"
            },
            {
                "step": 5,
                "description": "Update documentation",
                "status": "pending"
            }
        ]

class CorePlanner:
    """Core planner for handling task planning."""
    
    def __init__(self):
        """Initialize the planner."""
        self.logger = logging.getLogger(__name__)
        self.llm_client = LLMClient()
    
    def _validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate a task.
        
        Args:
            task: The task to validate.
            
        Returns:
            True if the task is valid, False otherwise.
        """
        required_fields = ["description", "requirements", "priority"]
        
        if not isinstance(task, dict):
            return False
            
        if not all(field in task for field in required_fields):
            return False
            
        if not isinstance(task["requirements"], list):
            return False
            
        return True
    
    def _validate_plan(self, plan: Dict[str, Any]) -> bool:
        """Validate a plan.
        
        Args:
            plan: The plan to validate.
            
        Returns:
            True if the plan is valid, False otherwise.
        """
        required_fields = ["steps", "estimated_total_time", "dependencies"]
        
        if not isinstance(plan, dict):
            return False
            
        if not all(field in plan for field in required_fields):
            return False
            
        if not isinstance(plan["steps"], list):
            return False
            
        if not isinstance(plan["dependencies"], list):
            return False
            
        return True
    
    def create_plan(
        self,
        task: Dict[str, Any],
        **options
    ) -> PlanningResult:
        """Create a plan for a task.
        
        Args:
            task: The task to plan for.
            **options: Additional planning options.
            
        Returns:
            Planning result.
            
        Raises:
            PlanningError: If planning fails.
        """
        try:
            if not self._validate_task(task):
                raise PlanningError("Invalid task format")
            
            # Create planning prompt
            prompt = (
                f"Please create a plan for the following task:\n\n"
                f"Task: {json.dumps(task, indent=2)}\n\n"
                f"Respond with a JSON object containing:\n"
                f"- steps: List of steps with id, description, and estimated_time\n"
                f"- estimated_total_time: Total estimated time\n"
                f"- dependencies: List of dependencies between steps\n"
            )
            
            # Get plan from LLM
            response = self.llm_client.generate_response(prompt)
            plan = json.loads(response.content)
            
            if not self._validate_plan(plan):
                raise PlanningError("Invalid plan format")
            
            return PlanningResult(status="success", plan=plan)
        except Exception as e:
            raise PlanningError(f"Error creating plan: {e}", cause=e) 