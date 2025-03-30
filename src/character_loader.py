"""
Character Loader Module for Call of Cthulhu Character Viewer

This module handles loading character data from JSON files with efficient
caching and validation. It provides functions for loading individual characters
and validating character data structure.

Author: Unknown
Version: 1.1
Last Updated: 2025-03-30
"""

import os
import json
from src.character_cache_core import CharacterCache
from src.constants import (
    REQUIRED_FIELDS,
    DEFAULT_DIRECTORY,
    JSON_EXTENSION,
    DEFAULT_ENCODING,
    JSON_INDENT,
    STATUS_CACHE_HIT,
    STATUS_LOADED_FROM_FILE,
    STATUS_VALIDATION_FAILED,
    STATUS_FILE_NOT_FOUND,
    STATUS_INVALID_JSON,
)

def validate_character_data(character_data):
    """
    Validate that character data contains all required fields.
    """
    return all(field in character_data for field in REQUIRED_FIELDS)


def load_character_from_json(filename, cache):
    """
    Load a premade character from a JSON file with intelligent caching.
    """
    try:
        character_data, status = cache.load_character(filename, validate_character_data)

        if status == STATUS_CACHE_HIT:
            return character_data
        elif status == STATUS_LOADED_FROM_FILE:
            return character_data
        elif status == STATUS_VALIDATION_FAILED:
            print(f"Error: Character data in '{filename}' is missing required fields.")
        elif status == STATUS_FILE_NOT_FOUND:
            print(f"Error: File '{filename}' not found.")
        elif status == STATUS_INVALID_JSON:
            print(f"Error: Invalid JSON format in '{filename}'.")
        else:
            print(f"Error loading character from '{filename}': {status}")
        return None

    except PermissionError:
        print(f"Error: No permission to access '{filename}'.")
        return None
    except OSError as e:
        print(f"Error accessing '{filename}': {e}")
        return None
    except Exception as e:
        print(f"Unexpected error loading character from '{filename}': {e}")
        return None


def load_all_characters(directory=DEFAULT_DIRECTORY, cache=None):
    """
    Load all characters from a directory with caching support.
    """
    characters = {}

    try:
        if not os.path.exists(directory):
            print(f"Error: Directory '{directory}' not found.")
            return characters

        if cache is None:
            cache = CharacterCache()

        for filename in os.listdir(directory):
            if filename.endswith(JSON_EXTENSION):
                full_path = os.path.join(directory, filename)
                try:
                    character_data = load_character_from_json(full_path, cache)
                    if character_data:
                        characters[full_path] = character_data
                except Exception as e:
                    print(f"Error loading character from '{full_path}': {e}")
                    continue

        return characters

    except PermissionError:
        print(f"Error: No permission to access directory '{directory}'.")
        return characters
    except Exception as e:
        print(f"Error loading characters from directory '{directory}': {e}")
        return characters


def save_character_to_json(character_data, filename, cache=None):
    """
    Save character data to a JSON file and update the cache if provided.
    """
    try:
        if not validate_character_data(character_data):
            print(f"Error: Cannot save invalid character data to '{filename}'.")
            return False

        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(filename, 'w', encoding=DEFAULT_ENCODING) as f:
            json.dump(character_data, f, indent=JSON_INDENT)

        if cache is not None:
            cache.put(filename, character_data)

        return True

    except PermissionError:
        print(f"Error: No permission to write to '{filename}'.")
        return False
    except OSError as e:
        print(f"Error writing to '{filename}': {e}")
        return False
    except Exception as e:
        print(f"Unexpected error saving character to '{filename}': {e}")
        return False


def get_character_field(character_data, field_path, default=None):
    """
    Safely get a field from character data using a dot-notation path.
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