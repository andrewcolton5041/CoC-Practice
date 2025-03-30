"""
Error Handling Module for Call of Cthulhu Character Viewer

This module provides centralized error handling functions and utilities
to maintain consistent error reporting across the application.

Author: Unknown
Version: 1.0
Last Updated: 2025-03-30
"""

import logging
import sys
import traceback
from typing import Optional, Dict, Any, Callable, Tuple

from src.constants import (
    LOG_FILE_NAME
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE_NAME),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("coc_character_viewer")

# Error type constants
ERROR_FILE_NOT_FOUND = "file_not_found"
ERROR_PERMISSION_DENIED = "permission_denied"
ERROR_INVALID_JSON = "invalid_json"
ERROR_INVALID_DATA = "invalid_data"
ERROR_CACHE_ERROR = "cache_error"
ERROR_UNEXPECTED = "unexpected_error"


def log_error(error_type: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
    """
    Log an error with consistent formatting.

    Args:
        error_type (str): Type of error
        message (str): Error message
        details (dict, optional): Additional error details
    """
    log_message = f"{error_type}: {message}"
    if details:
        log_message += f" - Details: {details}"

    logger.error(log_message)


def handle_file_error(error: Exception, filename: str) -> str:
    """
    Handle file-related errors with consistent messaging.

    Args:
        error (Exception): The exception that occurred
        filename (str): The file being accessed

    Returns:
        str: A consistent error code
    """
    if isinstance(error, FileNotFoundError):
        log_error(ERROR_FILE_NOT_FOUND, f"File not found: {filename}")
        return ERROR_FILE_NOT_FOUND

    if isinstance(error, PermissionError):
        log_error(ERROR_PERMISSION_DENIED, f"Permission denied: {filename}")
        return ERROR_PERMISSION_DENIED

    # Handle other OSError types
    if isinstance(error, OSError):
        log_error("file_error", f"OS error accessing {filename}: {str(error)}")
        return "file_error"

    # Unexpected errors
    log_error(ERROR_UNEXPECTED, f"Unexpected error with file {filename}: {str(error)}")
    return ERROR_UNEXPECTED


def handle_json_error(error: Exception, filename: str) -> str:
    """
    Handle JSON parsing errors with consistent messaging.

    Args:
        error (Exception): The exception that occurred
        filename (str): The JSON file being parsed

    Returns:
        str: A consistent error code
    """
    if isinstance(error, (ValueError, TypeError)):
        log_error(ERROR_INVALID_JSON, f"Invalid JSON in file: {filename}")
        return ERROR_INVALID_JSON

    # For other errors, use the file error handler
    return handle_file_error(error, filename)


def safe_operation(operation: Callable, 
                   error_handler: Callable, 
                   *args, 
                   **kwargs) -> Tuple[Optional[Any], Optional[str]]:
    """
    Execute an operation with consistent error handling.

    Args:
        operation (callable): The operation to execute
        error_handler (callable): Error handling function
        *args: Arguments to pass to the operation
        **kwargs: Keyword arguments to pass to the operation

    Returns:
        tuple: (result, error_code) where result is the operation result
               or None on error, and error_code is None on success or
               a string error code on failure
    """
    try:
        result = operation(*args, **kwargs)
        return result, None
    except Exception as e:
        error_code = error_handler(e, *args)
        return None, error_code


def display_user_error(error_type: str, message: str) -> None:
    """
    Display an error message to the user in a consistent format.

    Args:
        error_type (str): Type of error
        message (str): Error message to display
    """
    # Log the error first
    log_error(error_type, message)

    # Format error for display
    formatted_message = f"Error: {message}"

    # Print to console
    print(f"\n{formatted_message}\n")


def get_exception_details(exc: Exception) -> Dict[str, Any]:
    """
    Extract useful details from an exception.

    Args:
        exc (Exception): The exception to analyze

    Returns:
        dict: Exception details including type, message, and traceback
    """
    return {
        "type": type(exc).__name__,
        "message": str(exc),
        "traceback": traceback.format_exc(),
    }