"""
Executor Module

Handles task execution and implementation details.
"""

from typing import Dict, Any, Optional
import subprocess
import logging
from pathlib import Path

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