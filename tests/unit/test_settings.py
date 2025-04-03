"""
Unit tests for settings functionality.
"""
import os
import tempfile
from pathlib import Path

import pytest

from devin_integration.config import (
    Settings,
    LLMSettings,
    WebSettings,
    LoggingSettings,
    SettingsError,
    load_settings,
    validate_settings
)

@pytest.fixture
def valid_settings_file():
    """Create a temporary valid settings file."""
    settings_content = """
    {
        "llm": {
            "provider": "openai",
            "model": "gpt-4",
            "max_tokens": 1000
        },
        "web": {
            "timeout": 30,
            "max_retries": 3
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }
    """
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(settings_content)
        return f.name

@pytest.fixture
def invalid_settings_file():
    """Create a temporary invalid settings file."""
    settings_content = """
    {
        "llm": {
            "provider": "invalid_provider"
        }
    }
    """
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(settings_content)
        return f.name

def test_load_settings(valid_settings_file):
    """Test loading valid settings."""
    settings = load_settings(valid_settings_file)
    
    assert isinstance(settings, Settings)
    assert settings.llm.provider == "openai"
    assert settings.llm.model == "gpt-4"
    assert settings.web.timeout == 30
    assert settings.logging.level == "INFO"

def test_load_nonexistent_settings():
    """Test loading nonexistent settings file."""
    with pytest.raises(SettingsError):
        load_settings("nonexistent.json")

def test_load_invalid_settings(invalid_settings_file):
    """Test loading invalid settings."""
    with pytest.raises(SettingsError):
        load_settings(invalid_settings_file)

def test_validate_settings(valid_settings_file):
    """Test settings validation."""
    settings = load_settings(valid_settings_file)
    assert validate_settings(settings) is True

def test_validate_invalid_settings(invalid_settings_file):
    """Test validation of invalid settings."""
    with pytest.raises(SettingsError):
        settings = load_settings(invalid_settings_file)
        validate_settings(settings)

def test_settings_environment_override(valid_settings_file, monkeypatch):
    """Test environment variable settings override."""
    monkeypatch.setenv("DEVIN_LLM_PROVIDER", "anthropic")
    monkeypatch.setenv("DEVIN_LLM_MODEL", "claude-3")
    
    settings = load_settings(valid_settings_file)
    assert settings.llm.provider == "anthropic"
    assert settings.llm.model == "claude-3"

def test_settings_defaults(valid_settings_file):
    """Test settings defaults."""
    settings = load_settings(valid_settings_file)
    
    # Test that unspecified values get defaults
    assert hasattr(settings.llm, "temperature")  # Should have default value
    assert hasattr(settings.web, "user_agent")  # Should have default value

def test_settings_immutability():
    """Test settings immutability."""
    settings = Settings(
        llm={"provider": "openai", "model": "gpt-4"},
        web={"timeout": 30},
        logging={"level": "INFO"}
    )
    
    with pytest.raises(AttributeError):
        settings.llm.provider = "anthropic"  # Should be immutable

def test_settings_serialization(valid_settings_file):
    """Test settings serialization."""
    settings = load_settings(valid_settings_file)
    serialized = settings.to_dict()
    
    assert isinstance(serialized, dict)
    assert "llm" in serialized
    assert "web" in serialized
    assert "logging" in serialized

def test_settings_error():
    """Test SettingsError."""
    error = SettingsError("Test error")
    assert str(error) == "Test error"
    
    # Test with original exception
    original_error = Exception("Original error")
    error_with_cause = SettingsError("Test error", cause=original_error)
    assert error_with_cause.__cause__ == original_error

def test_settings_with_custom_path(monkeypatch):
    """Test settings with custom config path."""
    custom_path = "/custom/path/settings.json"
    monkeypatch.setenv("DEVIN_CONFIG_PATH", custom_path)
    
    with pytest.raises(SettingsError) as exc_info:
        load_settings()  # Should try to load from custom path
    
    assert custom_path in str(exc_info.value)

@pytest.fixture
def valid_settings_path():
    """Return path to valid settings file."""
    return Path(__file__).parent.parent / "fixtures" / "valid_settings.json"

@pytest.fixture
def invalid_settings_path():
    """Return path to invalid settings file."""
    return Path(__file__).parent.parent / "fixtures" / "invalid_settings.json"

@pytest.fixture
def nonexistent_settings_path():
    """Return path to nonexistent settings file."""
    return Path(__file__).parent.parent / "fixtures" / "nonexistent.json"

def test_load_settings_valid(valid_settings_path):
    """Test loading valid settings."""
    settings = load_settings(str(valid_settings_path))
    
    assert isinstance(settings, Settings)
    assert isinstance(settings.llm, LLMSettings)
    assert isinstance(settings.web, WebSettings)
    assert isinstance(settings.logging, LoggingSettings)
    
    assert settings.llm.provider == "openai"
    assert settings.llm.model == "gpt-4"
    assert settings.llm.max_tokens == 1000
    assert settings.llm.temperature == 0.7
    assert settings.llm.api_key == "test-api-key"
    
    assert settings.web.timeout == 30
    assert settings.web.max_retries == 3
    assert settings.web.user_agent == "DevinIntegration/1.0"
    
    assert settings.logging.level == "INFO"
    assert settings.logging.format == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def test_load_settings_nonexistent(nonexistent_settings_path):
    """Test loading nonexistent settings."""
    with pytest.raises(SettingsError) as exc_info:
        load_settings(str(nonexistent_settings_path))
    assert "Settings file not found" in str(exc_info.value)

def test_load_settings_invalid(invalid_settings_path):
    """Test loading invalid settings."""
    with pytest.raises(SettingsError) as exc_info:
        load_settings(str(invalid_settings_path))
    assert "Invalid settings format" in str(exc_info.value)

def test_validate_settings_valid():
    """Test validating valid settings."""
    valid_settings = {
        "llm": {
            "provider": "openai",
            "model": "gpt-4"
        },
        "web": {
            "timeout": 30
        },
        "logging": {
            "level": "INFO"
        }
    }
    assert validate_settings(valid_settings) is True

def test_validate_settings_invalid():
    """Test validating invalid settings."""
    invalid_settings = {
        "llm": {
            "provider": "invalid-provider"
        },
        "web": {},
        "logging": {}
    }
    assert validate_settings(invalid_settings) is False

def test_settings_environment_variables(monkeypatch):
    """Test settings initialization with environment variables."""
    monkeypatch.setenv("DEVIN_LLM_PROVIDER", "anthropic")
    monkeypatch.setenv("DEVIN_LLM_MODEL", "claude-3")
    monkeypatch.setenv("DEVIN_LLM_MAX_TOKENS", "2000")
    monkeypatch.setenv("DEVIN_LLM_TEMPERATURE", "0.5")
    monkeypatch.setenv("DEVIN_LLM_API_KEY", "env-api-key")
    
    monkeypatch.setenv("DEVIN_WEB_TIMEOUT", "60")
    monkeypatch.setenv("DEVIN_WEB_MAX_RETRIES", "5")
    monkeypatch.setenv("DEVIN_WEB_USER_AGENT", "CustomAgent/1.0")
    
    monkeypatch.setenv("DEVIN_LOGGING_LEVEL", "DEBUG")
    monkeypatch.setenv("DEVIN_LOGGING_FORMAT", "custom format")
    
    settings = Settings()
    
    assert settings.llm.provider == "anthropic"
    assert settings.llm.model == "claude-3"
    assert settings.llm.max_tokens == 2000
    assert settings.llm.temperature == 0.5
    assert settings.llm.api_key == "env-api-key"
    
    assert settings.web.timeout == 60
    assert settings.web.max_retries == 5
    assert settings.web.user_agent == "CustomAgent/1.0"
    
    assert settings.logging.level == "DEBUG"
    assert settings.logging.format == "custom format" 