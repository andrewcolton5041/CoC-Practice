"""
Character Loader Module for Call of Cthulhu Character Viewer

This module handles loading character data from JSON files with efficient
caching and validation. It provides functions for loading individual characters
and validating character data structure.

Author: Unknown
Version: 1.2
Last Updated: 2025-03-30
"""

import os
from typing import Dict, Any, Optional, Tuple, List

from src.character_cache_core import CharacterCache
from src.constants import (
    DEFAULT_DIRECTORY,
    JSON_EXTENSION,
    STATUS_CACHE_HIT,
    STATUS_LOADED_FROM_FILE,
    STATUS_VALIDATION_FAILED,
    STATUS_FILE_NOT_FOUND,
    STATUS_INVALID_JSON
)
from src.validation import validate_character_data, validate_file_path
from src.file_utils import read_json_file, write_json_file, list_json_files
from src.error_handling import log_error, display_user_error


def load_character_from_json(filename: str, cache: CharacterCache) -> Optional[Dict[str, Any]]:
    """
    Load a premade character from a JSON file with intelligent caching.

    Args:
        filename (str): Path to the character JSON file
        cache (CharacterCache): Cache instance to use for caching

    Returns:
        dict or None: Character data or None if loading failed
    """
    try:
        if not validate_file_path(filename, must_exist=False):
            log_error("invalid_path", f"Invalid file path: '{filename}'")
            return None

        character_data, status = cache.load_character(filename, validate_character_data)

        if status == STATUS_CACHE_HIT:
            return character_data
        elif status == STATUS_LOADED_FROM_FILE:
            return character_data
        elif status == STATUS_VALIDATION_FAILED:
            display_user_error("validation_error", f"Character data in '{filename}' is missing required fields.")
        elif status == STATUS_FILE_NOT_FOUND:
            display_user_error("file_not_found", f"File '{filename}' not found.")
        elif status == STATUS_INVALID_JSON:
            display_user_error("invalid_json", f"Invalid JSON format in '{filename}'.")
        else:
            display_user_error("unknown_error", f"Error loading character from '{filename}': {status}")

        return None

    except Exception as e:
        log_error("unexpected_error", f"Unexpected error loading character from '{filename}'", 
                 {"error": str(e)})
        return None


def load_all_characters(directory: str = DEFAULT_DIRECTORY, cache: Optional[CharacterCache] = None) -> Dict[str, Dict[str, Any]]:
    """
    Load all characters from a directory with caching support.

    Args:
        directory (str): Directory containing character files
        cache (CharacterCache, optional): Cache instance to use for caching

    Returns:
        dict: Dictionary mapping filenames to character data
    """
    characters = {}

    try:
        if not os.path.exists(directory):
            display_user_error("directory_not_found", f"Directory '{directory}' not found.")
            return characters

        if cache is None:
            cache = CharacterCache()

        json_files = list_json_files(directory)
        for filename in json_files:
            try:
                character_data = load_character_from_json(filename, cache)
                if character_data:
                    characters[filename] = character_data
            except Exception as e:
                log_error("character_loading_error", f"Error loading character from '{filename}'", 
                         {"error": str(e)})
                continue

        return characters

    except Exception as e:
        log_error("directory_error", f"Error loading characters from directory '{directory}'", 
                 {"error": str(e)})
        return characters


def save_character_to_json(character_data: Dict[str, Any], filename: str, 
                          cache: Optional[CharacterCache] = None) -> bool:
    """
    Save character data to a JSON file and update the cache if provided.

    Args:
        character_data (dict): Character data to save
        filename (str): Path to save the character file
        cache (CharacterCache, optional): Cache instance to update

    Returns:
        bool: True if saving was successful, False otherwise
    """
    try:
        if not validate_character_data(character_data):
            display_user_error("invalid_character", f"Cannot save invalid character data to '{filename}'.")
            return False

        success, status = write_json_file(filename, character_data)
        if not success:
            display_user_error("file_write_error", f"Error writing to '{filename}': {status}")
            return False

        if cache is not None:
            cache.put(filename, character_data)

        return True

    except Exception as e:
        log_error("save_error", f"Unexpected error saving character to '{filename}'", 
                 {"error": str(e)})
        return False


def get_character_field(character_data: Optional[Dict[str, Any]], field_path: str, 
                       default: Any = None) -> Any:
    """
    Safely get a field from character data using a dot-notation path.

    Args:
        character_data (dict): Character data
        field_path (str): Path to the field using dot notation (e.g., "attributes.Strength")
        default: Default value to return if field is not found

    Returns:
        The field value or default if not found
    """
    if not character_data:
        return default

    try:
        components = field_path.split('.')
        value = character_data

        for component in components:
            if isinstance(value, dict) and component in value:
                value = value[component]
            else:
                return default

        return value

    except Exception:
        return default