"""Configuration package for Devin Integration."""

import json
import os
from typing import Dict, Any, Optional
from .settings import (
    Settings,
    LLMSettings,
    WebSettings,
    LoggingSettings,
    load_settings,
    validate_settings
)
from .errors import (
    ConfigError,
    SettingsError,
    SettingsValidationError,
    SettingsLoadError,
    SettingsSaveError
)

__all__ = [
    'Settings',
    'LLMSettings',
    'WebSettings',
    'LoggingSettings',
    'load_settings',
    'validate_settings',
    'SettingsError',
    'SettingsValidationError',
    'SettingsLoadError',
    'SettingsSaveError',
    'load_config',
    'validate_config',
    'get_config_value'
]

def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from a file.
    
    Args:
        config_path: Path to the configuration file.
        
    Returns:
        Dictionary containing the configuration.
        
    Raises:
        ConfigError: If the file doesn't exist or is invalid.
    """
    try:
        if not os.path.exists(config_path):
            raise ConfigError(f"Configuration file not found: {config_path}")
            
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        if not validate_config(config):
            raise ConfigError("Invalid configuration format")
            
        return config
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in configuration file: {e}")
    except Exception as e:
        raise ConfigError(f"Error loading configuration: {e}")

def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration structure.
    
    Args:
        config: Configuration dictionary to validate.
        
    Returns:
        True if the configuration is valid, False otherwise.
    """
    required_sections = ["logging", "planner", "executor"]
    
    # Check required sections
    if not all(section in config for section in required_sections):
        return False
        
    # Validate logging section
    if not isinstance(config["logging"], dict):
        return False
    if "level" not in config["logging"]:
        return False
        
    # Validate planner section
    if not isinstance(config["planner"], dict):
        return False
    if "max_tasks" not in config["planner"]:
        return False
        
    # Validate executor section
    if not isinstance(config["executor"], dict):
        return False
    if "max_retries" not in config["executor"]:
        return False
        
    return True

def get_config_value(
    config: Dict[str, Any],
    path: str,
    default: Optional[Any] = None
) -> Any:
    """Get a configuration value by path.
    
    Args:
        config: Configuration dictionary.
        path: Dot-separated path to the value.
        default: Default value if the path doesn't exist.
        
    Returns:
        The configuration value or default if not found.
    """
    try:
        value = config
        for key in path.split('.'):
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default 