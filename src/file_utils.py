"""
File Utilities Module for Call of Cthulhu Character Viewer

This module provides centralized utilities for file operations,
including safe file reading/writing with proper error handling
and resource management.

Author: Unknown
Version: 1.0
Last Updated: 2025-03-30
"""

import os
import json
import contextlib
from typing import Dict, Any, Tuple, Optional, List, Union

from src.constants import (
    DEFAULT_ENCODING,
    JSON_EXTENSION,
    JSON_INDENT,
    STATUS_FILE_NOT_FOUND,
    STATUS_INVALID_JSON,
    MAX_PARTIAL_READ_BYTES
)


def read_json_file(filename: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """
    Safely read data from a JSON file with proper error handling.

    Args:
        filename (str): Path to the JSON file

    Returns:
        tuple: (data, status) where data is the parsed JSON (or None on error)
               and status is a string indicating success or error type
    """
    try:
        if not os.path.exists(filename):
            return None, STATUS_FILE_NOT_FOUND

        if not os.access(filename, os.R_OK):
            return None, "permission_denied"

        with open(filename, 'r', encoding=DEFAULT_ENCODING) as f:
            data = json.load(f)
            return data, "success"

    except json.JSONDecodeError:
        return None, STATUS_INVALID_JSON
    except UnicodeDecodeError:
        return None, "encoding_error"
    except OSError as e:
        return None, f"file_error: {str(e)}"
    except Exception as e:
        return None, f"unexpected_error: {str(e)}"


def write_json_file(filename: str, data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Safely write data to a JSON file with proper error handling.

    Args:
        filename (str): Path to the JSON file
        data (dict): Data to write to the file

    Returns:
        tuple: (success, status) where success is a boolean indicating success
               and status is a string providing additional information
    """
    try:
        # Create directory if needed
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(filename, 'w', encoding=DEFAULT_ENCODING) as f:
            json.dump(data, f, indent=JSON_INDENT)

        return True, "success"

    except PermissionError:
        return False, "permission_denied"
    except OSError as e:
        return False, f"file_error: {str(e)}"
    except Exception as e:
        return False, f"unexpected_error: {str(e)}"


def get_file_modification_time(filename: str) -> Optional[float]:
    """
    Get the last modification time of a file.

    Args:
        filename (str): Path to the file

    Returns:
        float or None: Modification time or None if file doesn't exist
    """
    try:
        return os.path.getmtime(filename)
    except OSError:
        return None


def list_json_files(directory: str) -> List[str]:
    """
    List all JSON files in a directory.

    Args:
        directory (str): Path to the directory

    Returns:
        list: List of full paths to JSON files
    """
    try:
        if not os.path.exists(directory):
            return []

        json_files = []
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith(JSON_EXTENSION):
                    if os.access(entry.path, os.R_OK):
                        json_files.append(entry.path)

        return json_files

    except PermissionError:
        return []
    except OSError:
        return []


def read_file_partial(filename: str, max_bytes: int = MAX_PARTIAL_READ_BYTES) -> Tuple[Optional[str], str]:
    """
    Safely read part of a file with proper error handling.
    Useful for large files or metadata extraction.

    Args:
        filename (str): Path to the file
        max_bytes (int): Maximum number of bytes to read

    Returns:
        tuple: (content, status) where content is the partial file content
               (or None on error) and status is a string
    """
    try:
        if not os.path.exists(filename):
            return None, STATUS_FILE_NOT_FOUND

        if not os.access(filename, os.R_OK):
            return None, "permission_denied"

        with open(filename, 'r', encoding=DEFAULT_ENCODING) as f:
            content = f.read(max_bytes)
            return content, "success"

    except UnicodeDecodeError:
        return None, "encoding_error"
    except OSError as e:
        return None, f"file_error: {str(e)}"
    except Exception as e:
        return None, f"unexpected_error: {str(e)}"


@contextlib.contextmanager
def safe_open_file(filename: str, mode: str = 'r'):
    """
    Context manager for safely opening and closing files.

    Args:
        filename (str): Path to the file
        mode (str): File open mode ('r', 'w', etc.)

    Yields:
        file object: The opened file object

    Raises:
        OSError: If the file cannot be opened
    """
    try:
        f = open(filename, mode, encoding=DEFAULT_ENCODING)
        try:
            yield f
        finally:
            f.close()
    except Exception as e:
        raise OSError(f"Error accessing file {filename}: {str(e)}")


def ensure_directory_exists(directory: str) -> bool:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        directory (str): Path to the directory

    Returns:
        bool: True if directory exists or was created, False on error
    """
    try:
        if not directory:
            return False

        if not os.path.exists(directory):
            os.makedirs(directory)

        return True

    except PermissionError:
        return False
    except OSError:
        return False