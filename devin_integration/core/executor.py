"""
Executor Module

Handles task execution and implementation details.
"""

from typing import Dict, Any, Optional, List
import subprocess
import logging
from pathlib import Path
from ..errors import ExecutionError

class ExecutionResult:
    """Class representing an execution result."""
    
    def __init__(
        self,
        status: str,
        steps_completed: List[Dict[str, Any]],
        total_time: str,
        error: Optional[Exception] = None
    ):
        """Initialize the result.
        
        Args:
            status: Execution status ("success" or "failure").
            steps_completed: List of completed steps with their results.
            total_time: Total execution time.
            error: Error that occurred during execution, if any.
        """
        self.status = status
        self.steps_completed = steps_completed
        self.total_time = total_time
        self.error = error
    
    def __str__(self) -> str:
        """Return a string representation of the result."""
        return (
            f"ExecutionResult(status={self.status}, "
            f"steps_completed={len(self.steps_completed)}, "
            f"total_time={self.total_time})"
        )

class Executor:
    """Handles task execution and implementation."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.logger = logging.getLogger(__name__)
        
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific task and return the results."""
        self.logger.info(f"Executing task: {task['description']}")
        
        try:
            # Execute the task based on its type
            if task['type'] == 'command':
                result = self._execute_command(task['command'])
            elif task['type'] == 'file_edit':
                result = self._edit_file(task['file_path'], task['changes'])
            elif task['type'] == 'test':
                result = self._run_tests(task['test_path'])
            else:
                raise ValueError(f"Unknown task type: {task['type']}")
            
            return {
                'status': 'success',
                'result': result,
                'task_id': task.get('id')
            }
            
        except Exception as e:
            self.logger.error(f"Task execution failed: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'task_id': task.get('id')
            }
    
    def _execute_command(self, command: str) -> Dict[str, Any]:
        """Execute a shell command."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                cwd=str(self.project_root)
            )
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command failed: {e.stderr}")
    
    def _edit_file(self, file_path: str, changes: Dict[str, Any]) -> Dict[str, Any]:
        """Edit a file with the specified changes."""
        target_file = self.project_root / file_path
        
        try:
            with open(target_file, 'r') as f:
                content = f.read()
            
            # Apply changes (this is a simple implementation)
            # In a real implementation, you'd want more sophisticated diff/patch handling
            for change in changes.get('edits', []):
                content = content.replace(change['old'], change['new'])
            
            with open(target_file, 'w') as f:
                f.write(content)
            
            return {
                'status': 'success',
                'file': str(target_file)
            }
        except Exception as e:
            raise RuntimeError(f"File edit failed: {str(e)}")
    
    def _run_tests(self, test_path: Optional[str] = None) -> Dict[str, Any]:
        """Run tests in the specified path."""
        try:
            if test_path:
                command = f"pytest {test_path}"
            else:
                command = "pytest"
            
            result = self._execute_command(command)
            
            return {
                'status': 'success' if result['returncode'] == 0 else 'failed',
                'test_results': result
            }
        except Exception as e:
            raise RuntimeError(f"Test execution failed: {str(e)}")
    
    def provide_feedback(self, task_id: str, feedback: Dict[str, Any]) -> None:
        """Provide feedback on a completed task."""
        self.logger.info(f"Feedback for task {task_id}: {feedback}")
        # In a real implementation, this would update the task status
        # and potentially trigger replanning if needed 

class CoreExecutor:
    """Core executor for handling task execution."""
    
    def __init__(self):
        """Initialize the executor."""
        self.logger = logging.getLogger(__name__)
        self.file_manager = None  # Will be initialized when needed
    
    def _validate_plan(self, plan: Dict[str, Any]) -> bool:
        """Validate an execution plan.
        
        Args:
            plan: The plan to validate.
            
        Returns:
            True if the plan is valid, False otherwise.
        """
        required_fields = ["steps", "dependencies"]
        
        if not isinstance(plan, dict):
            return False
            
        if not all(field in plan for field in required_fields):
            return False
            
        if not isinstance(plan["steps"], list):
            return False
            
        if not isinstance(plan["dependencies"], list):
            return False
            
        return True
    
    def _execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single step.
        
        Args:
            step: The step to execute.
            
        Returns:
            Dictionary containing step execution results.
            
        Raises:
            ExecutionError: If step execution fails.
        """
        try:
            action = step.get("action")
            params = step.get("params", {})
            
            if action == "create_file":
                return self._create_file(**params)
            elif action == "write_code":
                return self._write_code(**params)
            else:
                raise ExecutionError(f"Unknown action: {action}")
        except Exception as e:
            raise ExecutionError(f"Error executing step: {e}", cause=e)
    
    def _create_file(self, path: str) -> Dict[str, Any]:
        """Create a new file.
        
        Args:
            path: Path to the file.
            
        Returns:
            Dictionary containing creation results.
        """
        try:
            with open(path, 'w') as f:
                f.write('')
            return {"status": "success", "output": f"File created: {path}"}
        except Exception as e:
            raise ExecutionError(f"Error creating file: {e}", cause=e)
    
    def _write_code(self, content: str) -> Dict[str, Any]:
        """Write code to a file.
        
        Args:
            content: Code content to write.
            
        Returns:
            Dictionary containing writing results.
        """
        try:
            # Implementation would go here
            return {"status": "success", "output": "Code written successfully"}
        except Exception as e:
            raise ExecutionError(f"Error writing code: {e}", cause=e)
    
    def execute_plan(
        self,
        plan: Dict[str, Any],
        **options
    ) -> ExecutionResult:
        """Execute a plan.
        
        Args:
            plan: The plan to execute.
            **options: Additional execution options.
            
        Returns:
            Execution result.
            
        Raises:
            ExecutionError: If plan execution fails.
        """
        try:
            if not self._validate_plan(plan):
                raise ExecutionError("Invalid plan format")
            
            steps_completed = []
            for step in plan["steps"]:
                result = self._execute_step(step)
                steps_completed.append({
                    "id": step["id"],
                    "status": result["status"],
                    "output": result["output"]
                })
            
            return ExecutionResult(
                status="success",
                steps_completed=steps_completed,
                total_time="1h15m"  # This would be calculated in a real implementation
            )
        except Exception as e:
            raise ExecutionError(f"Error executing plan: {e}", cause=e) 