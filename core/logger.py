"""
Simple Logger Class
Provides easy-to-use logging functionality with different log levels and formatting
"""

import logging
import sys
from datetime import datetime
from typing import Optional, Dict, Any
import os
from pathlib import Path
from core.config import Config
# Predefined log formats
LOG_FORMATS = {
    'default': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'simple': '%(asctime)s - %(levelname)s - %(message)s',
    'detailed': '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    'json_like': '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    'minimal': '%(levelname)s - %(message)s',
    'timestamp_only': '%(asctime)s - %(message)s',
    'no_timestamp': '%(name)s - %(levelname)s - %(message)s'
}

class AppLogger:
    """
    Simple logger class for application logging
    Supports different log levels, file and console output, and custom formatting
    """
    
    def __init__(
        self,
        name: str = "app",
        log_level: str = "INFO",
        log_file: Optional[str] = None,
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        enable_console: bool = True,
        enable_file: bool = True
    ):
        """
        Initialize the logger
        
        Args:
            name: Logger name
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Path to log file (default: logs/app.log)
            max_bytes: Maximum size of log file before rotation
            backup_count: Number of backup files to keep
            enable_console: Whether to log to console
            enable_file: Whether to log to file
        """
        self.name = name
        # Create logs directory if it doesn't exist
        
        self.level = getattr(logging, log_level.upper(), logging.INFO)
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Set format
        formatter = logging.Formatter(LOG_FORMATS['default'])
        
        # Console handler
        if enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # File handler (if specified)
        if log_file is None:
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            log_file = log_dir / "app.log"

        if enable_file:    
            # Use RotatingFileHandler for log rotation
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count
            )
            file_handler.setLevel(self.level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self._log(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self._log(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self._log(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self._log(logging.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self._log(logging.CRITICAL, message, **kwargs)
    
    def _log(self, level: int, message: str, **kwargs):
        """Internal logging method"""
        if kwargs:
            # Format message with additional context
            context_str = " ".join([f"{k}={v}" for k, v in kwargs.items()])
            full_message = f"{message} | {context_str}"
        else:
            full_message = message
        
        self.logger.log(level, full_message)
    
    def log_dict(self, level: str, data: Dict[str, Any], prefix: str = ""):
        """Log dictionary data in a formatted way"""
        level_num = getattr(logging, level.upper(), logging.INFO)
        
        if prefix:
            message = f"{prefix}:"
        else:
            message = "Data:"
        
        for key, value in data.items():
            message += f"\n  {key}: {value}"
        
        self.logger.log(level_num, message)
    
    def log_exception(self, message: str, exc_info: bool = True, **kwargs):
        """Log exception with traceback"""
        self._log(logging.ERROR, message, **kwargs)
        if exc_info:
            self.logger.exception(message)
    
    def set_level(self, level: str):
        """Set log level"""
        level_num = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(level_num)
        for handler in self.logger.handlers:
            handler.setLevel(level_num)
    
    def get_level(self) -> str:
        """Get current log level"""
        return logging.getLevelName(self.logger.level)
    
    def is_debug_enabled(self) -> bool:
        """Check if debug logging is enabled"""
        return self.logger.isEnabledFor(logging.DEBUG)
    
    def is_info_enabled(self) -> bool:
        """Check if info logging is enabled"""
        return self.logger.isEnabledFor(logging.INFO)
    
    def set_format(self, format_string: str):
        """Change the log format for all handlers"""
        formatter = logging.Formatter(format_string)
        for handler in self.logger.handlers:
            handler.setFormatter(formatter)
    
    def set_format_by_name(self, format_name: str):
        """Set format using predefined format names"""
        if format_name in LOG_FORMATS:
            self.set_format(LOG_FORMATS[format_name])
        else:
            raise ValueError(f"Unknown format name: {format_name}. Available formats: {list(LOG_FORMATS.keys())}")
    
    def get_available_formats(self) -> Dict[str, str]:
        """Get all available predefined formats"""
        return LOG_FORMATS.copy()


# Global logger instances
def get_logger(name: str = "app", level: str = "INFO") -> AppLogger:
    """Get a logger instance"""
    return AppLogger(name, level)

# Default logger
default_logger = AppLogger("agent_data_extraction", **Config.get_logging_config())

# Convenience functions
def debug(message: str, **kwargs):
    """Log debug message using default logger"""
    default_logger.debug(message, **kwargs)

def info(message: str | dict, **kwargs):
    """Log info message using default logger"""
    if isinstance(message, dict):
        default_logger.log_dict(message, **kwargs)
    else:
        default_logger.info(message, **kwargs)

def warning(message: str, **kwargs):
    """Log warning message using default logger"""
    default_logger.warning(message, **kwargs)

def error(message: str, **kwargs):
    """Log error message using default logger"""
    default_logger.error(message, **kwargs)

def critical(message: str, **kwargs):
    """Log critical message using default logger"""
    default_logger.critical(message, **kwargs)

def log_exception(message: str, exc_info: bool = True, **kwargs):
    """Log exception using default logger"""
    default_logger.log_exception(message, exc_info, **kwargs)
