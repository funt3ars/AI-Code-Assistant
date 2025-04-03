"""
Unit tests for configuration handling.
"""
import pytest
import os
import tempfile
from devin_integration.config import (
    load_config,
    validate_config,
    get_config_value,
    ConfigError
)

@pytest.fixture
def valid_config_file():
    """Create a temporary valid config file."""
    config_content = """
    {
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "planner": {
            "max_tasks": 10,
            "timeout": 30
        },
        "executor": {
            "max_retries": 3,
            "retry_delay": 5
        }
    }
    """
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(config_content)
        return f.name

@pytest.fixture
def invalid_config_file():
    """Create a temporary invalid config file."""
    config_content = """
    {
        "logging": {
            "level": "INVALID_LEVEL"
        }
    }
    """
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(config_content)
        return f.name

def test_load_config(valid_config_file):
    """Test loading valid configuration."""
    config = load_config(valid_config_file)
    
    assert isinstance(config, dict)
    assert "logging" in config
    assert "planner" in config
    assert "executor" in config
    assert config["logging"]["level"] == "INFO"

def test_load_nonexistent_config():
    """Test loading nonexistent configuration file."""
    with pytest.raises(ConfigError):
        load_config("nonexistent.json")

def test_load_invalid_config(invalid_config_file):
    """Test loading invalid configuration."""
    with pytest.raises(ConfigError):
        load_config(invalid_config_file)

def test_validate_config(valid_config_file):
    """Test configuration validation."""
    config = load_config(valid_config_file)
    assert validate_config(config) is True

def test_validate_invalid_config(invalid_config_file):
    """Test validation of invalid configuration."""
    config = load_config(invalid_config_file)
    assert validate_config(config) is False

def test_get_config_value(valid_config_file):
    """Test getting configuration values."""
    config = load_config(valid_config_file)
    
    # Test existing values
    assert get_config_value(config, "logging.level") == "INFO"
    assert get_config_value(config, "planner.max_tasks") == 10
    
    # Test default values
    assert get_config_value(config, "nonexistent.key", default="default") == "default"
    
    # Test nested values
    assert get_config_value(config, "logging.format") is not None

def test_get_config_value_invalid_path(valid_config_file):
    """Test getting configuration values with invalid path."""
    config = load_config(valid_config_file)
    
    with pytest.raises(ConfigError):
        get_config_value(config, "invalid.path")

def test_environment_variable_override(valid_config_file, monkeypatch):
    """Test environment variable configuration override."""
    monkeypatch.setenv("DEVIN_LOG_LEVEL", "DEBUG")
    
    config = load_config(valid_config_file)
    assert get_config_value(config, "logging.level") == "DEBUG" 