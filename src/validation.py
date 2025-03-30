"""
Validation Module for Call of Cthulhu Character Viewer

This module provides centralized validation functions for character data,
metadata, and other validation needs throughout the application.

Author: Unknown
Version: 1.0
Last Updated: 2025-03-30
"""

import os
import re
from typing import Dict, Any, Optional

from src.constants import (
    REQUIRED_FIELDS,
    REQUIRED_METADATA_FIELDS,
    DEFAULT_OCCUPATION,
    DEFAULT_NATIONALITY,
    CACHE_SIZE_MIN,
    CACHE_SIZE_MAX
)


def validate_character_data(character_data: Optional[Dict[str, Any]]) -> bool:
    """
    Validate that character data contains all required fields.

    Args:
        character_data (dict): Character data to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if not character_data or not isinstance(character_data, dict):
        return False

    return all(field in character_data for field in REQUIRED_FIELDS)


def validate_character_metadata(metadata: Optional[Dict[str, Any]]) -> bool:
    """
    Validate that character metadata contains all required fields and values.

    Args:
        metadata (dict): Character metadata to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if not metadata or not isinstance(metadata, dict):
        return False

    # Check that all required fields are present
    if not all(field in metadata for field in REQUIRED_METADATA_FIELDS):
        return False

    # Check that fields have valid values
    if (not metadata['name'] or 
        metadata['occupation'] == DEFAULT_OCCUPATION or 
        metadata['nationality'] == DEFAULT_NATIONALITY):
        return False

    return True


def validate_file_path(file_path: str, must_exist: bool = True) -> bool:
    """
    Validate a file path for existence and readability.

    Args:
        file_path (str): Path to validate
        must_exist (bool): Whether the file must exist

    Returns:
        bool: True if valid, False otherwise
    """
    if not file_path or not isinstance(file_path, str):
        return False

    if must_exist:
        # Check file exists and is readable
        if not os.path.isfile(file_path) or not os.access(file_path, os.R_OK):
            return False

    return True


def validate_dice_notation(dice_string: str) -> bool:
    """
    Validate that a dice notation string has proper format.

    Args:
        dice_string (str): Dice notation to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if not dice_string or not isinstance(dice_string, str):
        return False

    # Remove whitespace
    dice_string = dice_string.replace(' ', '')

    # Basic dice notation pattern like "3D6", "1D20+5", "(2D6+3)*2"
    basic_pattern = r'^(\d+)[dD](\d+)$'
    complex_pattern = r'^[0-9dD\+\-\*\/\(\)]+$'

    # Check for basic dice pattern
    if re.match(basic_pattern, dice_string):
        return True

    # For complex patterns, do additional validation
    if re.match(complex_pattern, dice_string):
        # Detect invalid sequences
        invalid_patterns = [
            r'[+\-*/]{2,}',  # Consecutive operators
            r'^[+\-*/]|[+\-*/]$',  # Starting/ending with operators
            r'\(\)',  # Empty parentheses
            r'0[dD]|[dD]0'  # Zero-sided dice or zero dice
        ]

        for pattern in invalid_patterns:
            if re.search(pattern, dice_string):
                return False

        # Check balanced parentheses
        parentheses_count = 0
        for char in dice_string:
            if char == '(':
                parentheses_count += 1
            elif char == ')':
                parentheses_count -= 1
                if parentheses_count < 0:
                    return False

        if parentheses_count != 0:
            return False

        return True

    return False


def validate_directory_path(directory_path: str, must_exist: bool = True) -> bool:
    """
    Validate a directory path for existence and permissions.

    Args:
        directory_path (str): Path to validate
        must_exist (bool): Whether the directory must exist

    Returns:
        bool: True if valid, False otherwise
    """
    if not directory_path or not isinstance(directory_path, str):
        return False

    if must_exist:
        if not os.path.isdir(directory_path) or not os.access(directory_path, os.R_OK):
            return False

    return True


def validate_cache_size(size: Any, min_size: int = CACHE_SIZE_MIN, max_size: int = CACHE_SIZE_MAX) -> bool:
    """
    Validate a cache size value.

    Args:
        size (int): Cache size to validate
        min_size (int): Minimum allowed size
        max_size (int): Maximum allowed size

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        size = int(size)
        return min_size <= size <= max_size
    except (ValueError, TypeError):
        return False