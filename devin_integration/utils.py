"""Utility functions for the Devin Integration package."""

import os
import json
import logging
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from .errors import ValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ensure_dir(path: Union[str, Path]) -> Path:
    """Ensure a directory exists.
    
    Args:
        path: Directory path.
        
    Returns:
        Path object for the directory.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def load_json(path: Union[str, Path]) -> Dict[str, Any]:
    """Load a JSON file.
    
    Args:
        path: The path to the JSON file.
        
    Returns:
        The loaded JSON data.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    with open(path, 'r') as f:
        return json.load(f)

def save_json(data: Dict[str, Any], path: Union[str, Path]) -> None:
    """Save data to a JSON file.
    
    Args:
        data: The data to save.
        path: The path to save to.
    """
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def get_env_var(name: str) -> str:
    """Get an environment variable.
    
    Args:
        name: Name of the environment variable.
        
    Returns:
        Value of the environment variable.
        
    Raises:
        ValueError: If the environment variable is not set.
    """
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable {name} is not set")
    return value

def validate_task_structure(task: Dict[str, Any]) -> bool:
    """Validate the structure of a task dictionary.
    
    Args:
        task: Task dictionary to validate.
        
    Returns:
        True if the task structure is valid.
        
    Raises:
        ValidationError: If the task structure is invalid.
    """
    if task is None:
        return False
        
    required_fields = ["description"]
    
    try:
        for field in required_fields:
            if field not in task:
                return False
                
        if not isinstance(task["description"], str):
            return False
            
        return True
    except Exception:
        return False

def validate_url(url: str) -> bool:
    """Validate a URL string.
    
    Args:
        url: URL to validate.
        
    Returns:
        True if the URL is valid.
        
    Raises:
        ValidationError: If the URL is invalid.
    """
    if not url:
        raise ValidationError("URL cannot be empty")
        
    # Basic URL validation - could be enhanced with regex
    if not url.startswith(("http://", "https://")):
        raise ValidationError("URL must start with http:// or https://")
        
    return True

def validate_file_path(path: str) -> bool:
    """Validate a file path.
    
    Args:
        path: File path to validate.
        
    Returns:
        True if the file path is valid.
        
    Raises:
        ValidationError: If the file path is invalid.
    """
    if not path:
        raise ValidationError("File path cannot be empty")
        
    # Basic path validation - could be enhanced
    if "/" not in path and "\\" not in path:
        raise ValidationError("Invalid file path format")
        
    return True

def format_task_result(task: Dict[str, Any], analysis: Dict[str, Any], execution: Dict[str, Any]) -> Dict[str, Any]:
    """Format a task execution result.
    
    Args:
        task: Task dictionary.
        analysis: Analysis results.
        execution: Execution results.
        
    Returns:
        Formatted task result dictionary.
    """
    return {
        "task": task,
        "analysis": analysis,
        "execution": execution
    }

def log_task_progress(task_id: str, message: str, level: str = "info", extra: Optional[Dict[str, Any]] = None) -> None:
    """Log task progress.
    
    Args:
        task_id: ID of the task.
        message: Progress message.
        level: Log level (debug, info, warning, error).
        extra: Optional extra data to include in the log.
    """
    log_data = {
        "task_id": task_id,
        "message": message
    }
    
    if extra:
        log_data.update(extra)
        
    log_func = getattr(logger, level.lower())
    log_func(message, extra={"task_data": log_data}) 