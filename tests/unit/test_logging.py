"""
Unit tests for logging functionality.
"""
import pytest
import logging
from devin_integration.logging import setup_logging, get_logger

def test_setup_logging():
    """Test logging setup."""
    # Test that setup_logging doesn't raise any exceptions
    setup_logging()
    
    # Verify root logger has our handler
    root_logger = logging.getLogger()
    assert any(
        isinstance(h, logging.StreamHandler)
        for h in root_logger.handlers
    )

def test_get_logger():
    """Test logger retrieval."""
    logger = get_logger("test_module")
    
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_module"
    assert logger.level == logging.INFO

def test_logger_output(caplog):
    """Test logger output format."""
    logger = get_logger("test_module")
    
    # Test different log levels
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    
    # Verify log messages contain expected content
    assert "Debug message" not in caplog.text  # Debug not shown by default
    assert "Info message" in caplog.text
    assert "Warning message" in caplog.text
    assert "Error message" in caplog.text
    
    # Verify log format
    for record in caplog.records:
        assert "test_module" in record.name
        assert record.levelname in record.message

def test_logger_exception(caplog):
    """Test exception logging."""
    logger = get_logger("test_module")
    
    try:
        raise ValueError("Test error")
    except ValueError as e:
        logger.exception("Exception occurred")
    
    assert "Exception occurred" in caplog.text
    assert "Test error" in caplog.text
    assert "Traceback" in caplog.text

def test_logger_context(caplog):
    """Test logging with context information."""
    logger = get_logger("test_module")
    
    logger.info("Task started", extra={"task_id": "123", "status": "running"})
    
    assert "Task started" in caplog.text
    assert "task_id" in caplog.text
    assert "status" in caplog.text 