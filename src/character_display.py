"""Character Loader Module for Call of Cthulhu Character Viewer

Handles loading character data from JSON files with efficient caching and validation.
"""

import os
import json
from src.character_cache_core import CharacterCache

# Constants
REQUIRED_FIELDS = ['name', 'attributes']
JSON_EXTENSION = '.json'
DEFAULT_DIRECTORY = "characters"
DEFAULT_ENCODING = 'utf-8'
JSON_INDENT = 2

def validate_character_data(character_data):
    """Ensure character data has all required fields."""
    return all(field in character_data for field in REQUIRED_FIELDS)

def load_character_from_json(filename, cache):
    """Load a character from a JSON file, using cache if applicable."""
    try:
        character_data, status = cache.load_character(filename, validate_character_data)
        if status in ["cache_hit", "loaded_from_file"]:
            return character_data
        elif status == "validation_failed":
            print(f"Error: Missing required fields in '{filename}'.")
        elif status == "file_not_found":
            print(f"Error: File '{filename}' not found.")
        elif status == "invalid_json":
            print(f"Error: Invalid JSON format in '{filename}'.")
        else:
            print(f"Error loading character from '{filename}': {status}")
    except PermissionError:
        print(f"Error: No permission to access '{filename}'.")
    except OSError as e:
        print(f"Error accessing '{filename}': {e}")
    except Exception as e:
        print(f"Unexpected error loading character from '{filename}': {e}")
    return None

def load_all_characters(directory=DEFAULT_DIRECTORY, cache=None):
    """Load all characters from a directory of JSON files, using cache if provided."""
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
        return characters
    except PermissionError:
        print(f"Error: No permission to access directory '{directory}'.")
        return characters
    except Exception as e:
        print(f"Error loading characters from directory '{directory}': {e}")
        return characters

def save_character_to_json(character_data, filename, cache=None):
    """Save character data to JSON file and optionally update cache."""
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
    except OSError as e:
        print(f"Error writing to '{filename}': {e}")
    except Exception as e:
        print(f"Unexpected error saving character to '{filename}': {e}")
    return False
