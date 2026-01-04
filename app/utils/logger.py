"""
Logging Configuration for PRAISA

Provides centralized logging setup with different levels for development and production.
Uses Python's built-in logging module with custom formatters.

Author: Senior Engineer
Date: 2026-01-04
"""

import logging
import sys
from app.config import settings


def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with appropriate configuration.
    
    Creates a logger with:
    - DEBUG level for development
    - INFO level for production
    - Colored console output
    - Timestamp and module name in format
    
    Args:
        name: Logger name (usually __name__ from calling module)
    
    Returns:
        logging.Logger: Configured logger instance
    
    Example:
        >>> from app.utils.logger import setup_logger
        >>> logger = setup_logger(__name__)
        >>> logger.info("Patient matched successfully")
    """
    # Create logger
    logger = logging.getLogger(name)
    
    # Set level based on environment
    if settings.env == "development":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers if logger already configured
    if logger.handlers:
        return logger
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    
    # Create formatter with timestamp, name, level, and message
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger


# Create a default logger for the application
app_logger = setup_logger("praisa")
