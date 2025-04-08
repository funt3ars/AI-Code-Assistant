"""Error classes for the devin_integration package."""

from typing import Any, Dict, Optional

class DevinError(Exception):
    """Base class for all Devin Integration errors."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None, cause: Optional[Exception] = None):
        """Initialize the error.
        
        Args:
            message: Error message.
            context: Optional context dictionary.
            cause: Optional cause exception.
        """
        super().__init__(message)
        self.context = context
        self.__cause__ = cause

class ValidationError(DevinError):
    """Error raised when validation fails."""
    pass

class ConfigError(DevinError):
    """Error raised when configuration fails."""
    pass

class SettingsError(DevinError):
    """Error raised when settings validation or loading fails."""
    pass

class ExecutionError(DevinError):
    """Error raised when task execution fails."""
    pass

class PlanningError(DevinError):
    """Error raised when task planning fails."""
    pass

class LLMError(DevinError):
    """Error raised when LLM operations fail."""
    pass

class LLMVisionError(DevinError):
    """Error raised when LLM vision operations fail."""
    pass

class WebError(DevinError):
    """Error raised when web operations fail."""
    pass

class SearchError(DevinError):
    """Error raised when search operations fail."""
    pass

class ScreenshotError(DevinError):
    """Error raised when screenshot operations fail."""
    pass

class WorkflowError(DevinError):
    """Error raised when workflow operations fail."""
    pass

class DevinIntegrationError(Exception):
    """Base error class for devin_integration."""
    pass

class TaskValidationError(DevinIntegrationError):
    """Error raised when a task fails validation."""
    
    def __init__(self, message: str, task: Optional[dict] = None):
        """Initialize the error.
        
        Args:
            message: The error message.
            task: Optional task that failed validation.
        """
        super().__init__(message)
        self.task = task

class TaskExecutionError(DevinIntegrationError):
    """Error raised when a task fails during execution."""
    
    def __init__(self, message: str, step: Optional[dict] = None, task: Optional[dict] = None):
        """Initialize the error.
        
        Args:
            message: The error message.
            step: Optional step that failed.
            task: Optional task that failed.
        """
        super().__init__(message)
        self.step = step
        self.task = task
        
    def __str__(self) -> str:
        """Return a string representation of the error."""
        parts = [super().__str__()]
        if self.task:
            parts.append(f"Task: {self.task}")
        if self.step:
            parts.append(f"Step: {self.step}")
        return "\n".join(parts)

class TaskAnalysisError(DevinIntegrationError):
    """Error raised when a task fails during analysis."""
    
    def __init__(self, message: str, task: Optional[dict] = None):
        """Initialize the error.
        
        Args:
            message: The error message.
            task: Optional task that failed analysis.
        """
        super().__init__(message)
        self.task = task

class VerificationError(DevinError):
    """Error raised when verification fails."""
    pass

class SettingsValidationError(SettingsError):
    """Error raised when settings validation fails."""
    pass

class SettingsLoadError(SettingsError):
    """Error raised when settings cannot be loaded."""
    pass

class SettingsSaveError(SettingsError):
    """Error raised when settings cannot be saved."""
    pass

class ExecutionError(Exception):
    """Error raised during task execution."""
    def __init__(self, message: str, task_id: Optional[str] = None, cause: Optional[Exception] = None):
        """Initialize the error.
        
        Args:
            message: Error message.
            task_id: ID of the task that failed.
            cause: Original exception that caused this error.
        """
        super().__init__(message)
        self.task_id = task_id
        self.__cause__ = cause

class PlanningError(Exception):
    """Error raised during task planning."""
    def __init__(self, message: str, task_id: Optional[str] = None, cause: Optional[Exception] = None):
        """Initialize the error.
        
        Args:
            message: Error message.
            task_id: ID of the task that failed.
            cause: Original exception that caused this error.
        """
        super().__init__(message)
        self.task_id = task_id
        self.__cause__ = cause

class LLMVisionError(Exception):
    """Error raised during LLM vision operations."""
    def __init__(self, message: str, image_path: Optional[str] = None, cause: Optional[Exception] = None):
        """Initialize the error.
        
        Args:
            message: Error message.
            image_path: Path to the image that caused the error.
            cause: Original exception that caused this error.
        """
        super().__init__(message)
        self.image_path = image_path
        self.__cause__ = cause

class WebError(DevinIntegrationError):
    """Error raised when there is an issue with web operations."""
    def __init__(self, message: str, url: Optional[str] = None, cause: Optional[Exception] = None):
        """Initialize the error.
        
        Args:
            message: Error message.
            url: URL that caused the error.
            cause: Original exception that caused this error.
        """
        super().__init__(message)
        self.url = url
        self.__cause__ = cause

class SearchError(Exception):
    """Error raised during search operations."""
    def __init__(self, message: str, query: Optional[str] = None, cause: Optional[Exception] = None):
        """Initialize the error.
        
        Args:
            message: Error message.
            query: Search query that caused the error.
            cause: Original exception that caused this error.
        """
        super().__init__(message)
        self.query = query
        self.__cause__ = cause

class WorkflowError(DevinIntegrationError):
    """Error raised when there is an issue with workflow operations."""
    def __init__(self, message: str, workflow_id: Optional[str] = None, cause: Optional[Exception] = None):
        """Initialize the error.
        
        Args:
            message: Error message.
            workflow_id: ID of the workflow that failed.
            cause: Original exception that caused this error.
        """
        super().__init__(message)
        self.workflow_id = workflow_id
        self.__cause__ = cause 