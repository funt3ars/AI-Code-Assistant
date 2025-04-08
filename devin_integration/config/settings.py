"""
Settings Module

Handles configuration loading and management.
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, Union
from .errors import SettingsError

@dataclass
class LLMSettings:
    """LLM-related settings."""
    provider: str = "openai"
    model: str = "gpt-4"
    max_tokens: int = 1000
    temperature: float = 0.7
    api_key: Optional[str] = None

@dataclass
class WebSettings:
    """Web-related settings."""
    timeout: int = 30
    max_retries: int = 3
    user_agent: str = "DevinIntegration/1.0"

@dataclass
class LoggingSettings:
    """Logging-related settings."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

@dataclass
class Settings:
    """Main settings class."""
    llm: LLMSettings = field(default_factory=LLMSettings)
    web: WebSettings = field(default_factory=WebSettings)
    logging: LoggingSettings = field(default_factory=LoggingSettings)
    
    def __post_init__(self):
        """Initialize settings with environment variables."""
        # LLM settings
        if os.getenv("DEVIN_LLM_PROVIDER"):
            self.llm.provider = os.getenv("DEVIN_LLM_PROVIDER")
        if os.getenv("DEVIN_LLM_MODEL"):
            self.llm.model = os.getenv("DEVIN_LLM_MODEL")
        if os.getenv("DEVIN_LLM_MAX_TOKENS"):
            self.llm.max_tokens = int(os.getenv("DEVIN_LLM_MAX_TOKENS"))
        if os.getenv("DEVIN_LLM_TEMPERATURE"):
            self.llm.temperature = float(os.getenv("DEVIN_LLM_TEMPERATURE"))
        if os.getenv("DEVIN_LLM_API_KEY"):
            self.llm.api_key = os.getenv("DEVIN_LLM_API_KEY")
        
        # Web settings
        if os.getenv("DEVIN_WEB_TIMEOUT"):
            self.web.timeout = int(os.getenv("DEVIN_WEB_TIMEOUT"))
        if os.getenv("DEVIN_WEB_MAX_RETRIES"):
            self.web.max_retries = int(os.getenv("DEVIN_WEB_MAX_RETRIES"))
        if os.getenv("DEVIN_WEB_USER_AGENT"):
            self.web.user_agent = os.getenv("DEVIN_WEB_USER_AGENT")
        
        # Logging settings
        if os.getenv("DEVIN_LOGGING_LEVEL"):
            self.logging.level = os.getenv("DEVIN_LOGGING_LEVEL")
        if os.getenv("DEVIN_LOGGING_FORMAT"):
            self.logging.format = os.getenv("DEVIN_LOGGING_FORMAT")
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary.
        
        Returns:
            Dictionary representation of settings.
        """
        return {
            "llm": {
                "provider": self.llm.provider,
                "model": self.llm.model,
                "max_tokens": self.llm.max_tokens,
                "temperature": self.llm.temperature,
                "api_key": self.llm.api_key
            },
            "web": {
                "timeout": self.web.timeout,
                "max_retries": self.web.max_retries,
                "user_agent": self.web.user_agent
            },
            "logging": {
                "level": self.logging.level,
                "format": self.logging.format
            }
        }

def load_settings(settings_path: Optional[str] = None) -> Settings:
    """Load settings from a file.
    
    Args:
        settings_path: Path to the settings file. If not provided, uses DEVIN_CONFIG_PATH env var.
        
    Returns:
        Settings object.
        
    Raises:
        SettingsError: If the file doesn't exist or is invalid.
    """
    if settings_path is None:
        settings_path = os.getenv("DEVIN_CONFIG_PATH")
        if not settings_path:
            raise SettingsError("No settings path provided and DEVIN_CONFIG_PATH not set")
    
    try:
        if not os.path.exists(settings_path):
            raise SettingsError(f"Settings file not found: {settings_path}")
            
        with open(settings_path, 'r') as f:
            settings_dict = json.load(f)
            
        if not validate_settings(settings_dict):
            raise SettingsError("Invalid settings format")
            
        return Settings(
            llm=LLMSettings(**settings_dict.get("llm", {})),
            web=WebSettings(**settings_dict.get("web", {})),
            logging=LoggingSettings(**settings_dict.get("logging", {}))
        )
    except json.JSONDecodeError as e:
        raise SettingsError(f"Invalid JSON in settings file: {e}", cause=e)
    except Exception as e:
        raise SettingsError(f"Error loading settings: {e}", cause=e)

def validate_settings(settings: Union[Dict, Settings]) -> bool:
    """Validate settings structure.
    
    Args:
        settings: Settings dictionary or Settings object to validate.
        
    Returns:
        True if the settings are valid, False otherwise.
    """
    if isinstance(settings, Settings):
        settings = settings.to_dict()
    
    required_sections = ["llm", "web", "logging"]
    
    # Check required sections
    if not isinstance(settings, dict):
        return False
        
    if not all(section in settings for section in required_sections):
        return False
        
    # Validate LLM settings
    if not isinstance(settings["llm"], dict):
        return False
    if "provider" not in settings["llm"]:
        return False
    if settings["llm"]["provider"] not in ["openai", "anthropic"]:
        return False
        
    # Validate web settings
    if not isinstance(settings["web"], dict):
        return False
    if "timeout" not in settings["web"]:
        return False
        
    # Validate logging settings
    if not isinstance(settings["logging"], dict):
        return False
    if "level" not in settings["logging"]:
        return False
        
    return True

def save_settings(project_root: str, settings: Dict[str, Any]) -> None:
    """Save settings to the project configuration."""
    config_path = Path(project_root) / ".devin_config.json"
    
    with open(config_path, 'w') as f:
        json.dump(settings, f, indent=2)

def get_tool_config(tool_name: str, settings: Dict[str, Any]) -> Dict[str, Any]:
    """Get configuration for a specific tool."""
    return settings.get("tools", {}).get(tool_name, {}) 