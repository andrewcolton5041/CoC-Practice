"""
Character Loader Module for Call of Cthulhu Character Viewer

This module handles loading character data from JSON files with efficient
caching and validation. It provides functions for loading individual characters
and validating character data structure.

Author: Unknown
Version: 1.0
Last Updated: 2025-03-30
"""

import os
import json
from src.character_cache import CharacterCache


def validate_character_data(character_data):
    """
    Validate that character data contains all required fields.

    Args:
        character_data (dict): Character data to validate

    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = ['name', 'attributes']
    return all(field in character_data for field in required_fields)


def load_character_from_json(filename, cache):
    """
    Load a premade character from a JSON file with intelligent caching.

    Checks if the character is already in the cache and if the file hasn't changed.

    Args:
        filename (str): Path to the JSON file containing character data
        cache (CharacterCache): Cache instance for storing character data

    Returns:
        dict: Dictionary containing the character data or None if file cannot be loaded

    Raises:
        FileNotFoundError: If the file doesn't exist
        PermissionError: If the file cannot be accessed due to permissions
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        # Use the cache's load_character method to handle both cache retrieval and file loading
        character_data, status = cache.load_character(filename, validate_character_data)

        if status == "cache_hit":
            return character_data
        elif status == "loaded_from_file":
            return character_data
        elif status == "validation_failed":
            print(f"Error: Character data in '{filename}' is missing required fields.")
            return None
        elif status == "file_not_found":
            print(f"Error: File '{filename}' not found.")
            return None
        elif status == "invalid_json":
            print(f"Error: Invalid JSON format in '{filename}'.")
            return None
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


def load_all_characters(directory="characters", cache=None):
    """
    Load all characters from a directory with caching support.

    This function loads all character data from JSON files in the specified directory,
    using the cache if provided.

    Args:
        directory (str, optional): Directory containing character files. Defaults to "characters".
        cache (CharacterCache, optional): Cache instance for storing character data. 
            If None, no caching is used.

    Returns:
        dict: Dictionary mapping filenames to character data dictionaries,
            or an empty dictionary if no valid characters were found
    """
    characters = {}

    try:
        if not os.path.exists(directory):
            print(f"Error: Directory '{directory}' not found.")
            return characters

        # Create a new cache if none was provided
        if cache is None:
            cache = CharacterCache()

        # Get all JSON files in the directory
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
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

    Args:
        character_data (dict): Character data to save
        filename (str): Path to the JSON file to save to
        cache (CharacterCache, optional): Cache instance to update after saving.
            If None, no cache update is performed.

    Returns:
        bool: True if save was successful, False otherwise
    """
    try:
        # Validate character data before saving
        if not validate_character_data(character_data):
            print(f"Error: Cannot save invalid character data to '{filename}'.")
            return False

        # Ensure the directory exists
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Write the character data to the file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(character_data, f, indent=2)

        # Update the cache if provided
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

    This function can access nested fields using dot notation, e.g.,
    "attributes.Strength" would access character_data["attributes"]["Strength"].

    Args:
        character_data (dict): Character data dictionary
        field_path (str): Path to the field using dot notation
        default: Value to return if the field doesn't exist. Defaults to None.

    Returns:
        The field value or the default if not found
    """
    if not character_data:
        return default

    try:
        # Split the path into components
        components = field_path.split('.')

        # Start with the character data
        value = character_data

        # Traverse the path
        for component in components:
            if isinstance(value, dict) and component in value:
                value = value[component]
            else:
                return default

        return value

    except Exception:
        return default