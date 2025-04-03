"""Coordinator functionality for devin_integration."""

from typing import Dict, List, Optional, Union
from .planner import Planner
from .executor import Executor
from .errors import WorkflowError

class Coordinator:
    """Class for coordinating planning and execution."""
    
    def __init__(self, provider: str = "openai"):
        """Initialize the coordinator.
        
        Args:
            provider: The LLM provider to use.
        """
        self.planner = Planner(provider)
        self.executor = Executor(provider)

    async def run_workflow(
        self,
        task: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """Run a complete workflow for a task.
        
        Args:
            task: The task to execute.
            context: Optional context for the task.
            
        Returns:
            Dictionary containing workflow results.
            
        Raises:
            WorkflowError: If there is an error during the workflow.
        """
        try:
            # Plan the task
            plan = await self.planner.create_plan(task, context)
            
            # Execute the plan
            results = await self.executor.execute_plan(plan)
            
            return {
                "plan": plan,
                "results": results
            }
        except Exception as e:
            raise WorkflowError(f"Error running workflow: {e}")

    async def run_batch_workflow(
        self,
        tasks: List[str],
        context: Optional[Dict] = None
    ) -> Dict[str, Dict]:
        """Run workflows for multiple tasks.
        
        Args:
            tasks: List of tasks to execute.
            context: Optional context for the tasks.
            
        Returns:
            Dictionary mapping tasks to workflow results.
            
        Raises:
            WorkflowError: If there is an error during the batch workflow.
        """
        try:
            results = {}
            for task in tasks:
                results[task] = await self.run_workflow(task, context)
            return results
        except Exception as e:
            raise WorkflowError(f"Error running batch workflow: {e}") 