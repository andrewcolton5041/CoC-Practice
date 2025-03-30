"""Character Cache Utility Functions for Call of Cthulhu Character Viewer

This module provides additional utility functions related to character caching.

Author: Unknown
Version: 2.1
Last Updated: 2025-03-30
"""

# Constants for required fields
REQUIRED_FIELDS = ['name', 'attributes']

def validate_character_data(character_data):
    """
    Validate that character data contains all required fields.

    Args:
        character_data (dict): Character data to validate

    Returns:
        bool: True if valid, False otherwise
    """
    return all(field in character_data for field in REQUIRED_FIELDS)
