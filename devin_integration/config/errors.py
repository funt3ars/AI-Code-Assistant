"""Settings-related errors."""

from typing import Dict, Optional

class ConfigError(Exception):
    """Base class for configuration errors."""
    def __init__(self, message: str, cause: Optional[Exception] = None):
        """Initialize the error.
        
        Args:
            message: Error message.
            cause: Original exception that caused this error.
        """
        super().__init__(message)
        self.cause = cause

class SettingsError(Exception):
    """Base class for settings-related errors."""
    def __init__(self, message: str, context: Optional[Dict] = None, cause: Optional[Exception] = None):
        """Initialize the error.
        
        Args:
            message: Error message.
            context: Additional context about the error.
            cause: Original exception that caused this error.
        """
        super().__init__(message)
        self.context = context or {}
        self.__cause__ = cause
        
    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.context:
            return f"{super().__str__()} (Context: {self.context})"
        return super().__str__()

class SettingsValidationError(SettingsError):
    """Error raised when settings validation fails."""
    pass

class SettingsLoadError(SettingsError):
    """Error raised when settings cannot be loaded."""
    pass

class SettingsSaveError(SettingsError):
    """Error raised when settings cannot be saved."""
    pass 