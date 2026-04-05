"""
Structured logging utility for the framework.
Supports console and file logging with consistent formatting.
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class JsonFormatter(logging.Formatter):
    """Custom formatter that outputs structured JSON logs."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add any extra fields
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)
        
        return json.dumps(log_data)


class Logger:
    """Wrapper around Python's logging module."""
    
    def __init__(self, name: str = "framework", log_dir: Optional[Path] = None):
        """Initialize logger."""
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        if log_dir:
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / f"{name}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(console_formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message: str, **extra) -> None:
        """Log info level message."""
        record = self.logger.makeRecord(
            self.name, logging.INFO, "", 0, message, (), None
        )
        if extra:
            record.extra_fields = extra
        self.logger.handle(record)
    
    def debug(self, message: str, **extra) -> None:
        """Log debug level message."""
        record = self.logger.makeRecord(
            self.name, logging.DEBUG, "", 0, message, (), None
        )
        if extra:
            record.extra_fields = extra
        self.logger.handle(record)
    
    def warning(self, message: str, **extra) -> None:
        """Log warning level message."""
        record = self.logger.makeRecord(
            self.name, logging.WARNING, "", 0, message, (), None
        )
        if extra:
            record.extra_fields = extra
        self.logger.handle(record)
    
    def error(self, message: str, **extra) -> None:
        """Log error level message."""
        record = self.logger.makeRecord(
            self.name, logging.ERROR, "", 0, message, (), None
        )
        if extra:
            record.extra_fields = extra
        self.logger.handle(record)


def get_logger(name: str = "framework", log_dir: Optional[Path] = None) -> Logger:
    """Get a logger instance."""
    return Logger(name, log_dir)
