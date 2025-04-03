"""
Settings Module

Handles configuration loading and management.
"""

import os
from typing import Dict, Any
from pathlib import Path
import json

def load_settings(project_root: str) -> Dict[str, Any]:
    """Load settings from the project configuration."""
    config_path = Path(project_root) / ".devin_config.json"
    
    # Default settings
    settings = {
        "project_root": str(project_root),
        "tools": {
            "web_scraper": {
                "enabled": True,
                "max_concurrent": 3
            },
            "search_engine": {
                "enabled": True,
                "provider": "duckduckgo"
            }
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }
    
    # Load custom settings if they exist
    if config_path.exists():
        with open(config_path, 'r') as f:
            custom_settings = json.load(f)
            settings.update(custom_settings)
    
    return settings

def save_settings(project_root: str, settings: Dict[str, Any]) -> None:
    """Save settings to the project configuration."""
    config_path = Path(project_root) / ".devin_config.json"
    
    with open(config_path, 'w') as f:
        json.dump(settings, f, indent=2)

def get_tool_config(tool_name: str, settings: Dict[str, Any]) -> Dict[str, Any]:
    """Get configuration for a specific tool."""
    return settings.get("tools", {}).get(tool_name, {}) 