"""
Character Cache Module for Call of Cthulhu Character Viewer

This module provides a caching mechanism for character data, improving
performance by reducing the need to repeatedly read character files from disk.

The main class is CharacterCache, which handles:
- Storing character data with modification timestamps
- Validating whether cached data is still current
- Providing statistics about cache usage and memory consumption

Author: Unknown
Version: 1.1
Last Updated: 2025-03-30
"""

import os
import json
import time


class CharacterCache:
    """
    A class to manage caching of character data with intelligent invalidation.

    This cache stores character data along with the file modification time,
    allowing it to determine when a cached entry is stale and needs to be reloaded.
    """

    def __init__(self):
        """
        Initialize an empty character cache.
        """
        self._cache = {}  # Dictionary to store cached character data

    def get(self, filename):
        """
        Retrieve character data from the cache if available and current.

        Args:
            filename (str): Path to the character file

        Returns:
            dict or None: The cached character data if available and current, None otherwise
        """
        # Check if file is in cache
        if filename not in self._cache:
            return None

        # Check if the cached version is still current using context manager
        try:
            current_mod_time = os.path.getmtime(filename)
            if current_mod_time != self._cache[filename]["mod_time"]:
                # File has been modified since it was cached
                return None
            return self._cache[filename]["data"]
        except OSError:
            # If file can't be accessed, return None
            return None

    def put(self, filename, data):
        """
        Add or update character data in the cache.

        Args:
            filename (str): Path to the character file
            data (dict): Character data to cache

        Returns:
            bool: True if caching was successful, False otherwise
        """
        try:
            mod_time = os.path.getmtime(filename)
            self._cache[filename] = {
                "data": data,
                "mod_time": mod_time,
                "cached_time": time.time()
            }
            return True
        except OSError:
            return False

    def invalidate(self, filename=None):
        """
        Invalidate entries in the cache.

        Args:
            filename (str, optional): Specific file to remove from cache.
                If None, clears the entire cache.

        Returns:
            bool: True if invalidation was successful, False if file not in cache
        """
        if filename is None:
            # Clear the entire cache
            self._cache = {}
            return True
        elif filename in self._cache:
            # Remove specific file from cache
            del self._cache[filename]
            return True
        else:
            # File not in cache
            return False

    def contains(self, filename):
        """
        Check if a file is currently in the cache.

        Args:
            filename (str): Path to the character file

        Returns:
            bool: True if file is in the cache, False otherwise
        """
        return filename in self._cache

    def get_stats(self):
        """
        Get statistics about the current state of the cache.

        Returns:
            dict: Dictionary with cache statistics including:
                - size: Number of entries in the cache
                - files: List of filenames in the cache
                - memory_usage: Approximate memory usage in bytes
                - oldest_entry_age: Age of the oldest cache entry in seconds
                - newest_entry_age: Age of the newest cache entry in seconds
        """
        stats = {
            "size": len(self._cache),
            "files": list(self._cache.keys()),
            "memory_usage": sum(len(str(item)) for item in self._cache.values())
        }

        # Calculate age of entries if cache is not empty
        if self._cache:
            current_time = time.time()
            cache_times = [entry["cached_time"] for entry in self._cache.values()]
            stats["oldest_entry_age"] = current_time - min(cache_times)
            stats["newest_entry_age"] = current_time - max(cache_times)

        return stats

    def load_character(self, filename, validation_function=None):
        """
        Load a character from the cache or from disk if not cached.

        This method combines cache retrieval and file loading in one operation.
        If the character is not in the cache or is stale, it will be loaded from disk
        and added to the cache.

        Args:
            filename (str): Path to the character file
            validation_function (callable, optional): Function to validate character data
                before caching. Should take character data as input and return bool.

        Returns:
            tuple: (character_data, str) where str is a status message
                ("cache_hit", "loaded_from_file", or error message)

        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        # Try to get from cache first
        cached_data = self.get(filename)
        if cached_data:
            return cached_data, "cache_hit"

        # Not in cache or stale, load from file
        try:
            # Use context manager to ensure file is properly closed after operations
            with open(filename, 'r', encoding='utf-8') as f:
                character_data = json.load(f)

            # Validate data if validation function provided
            if validation_function and not validation_function(character_data):
                return None, "validation_failed"

            # Add to cache and return
            self.put(filename, character_data)
            return character_data, "loaded_from_file"

        except FileNotFoundError:
            return None, "file_not_found"
        except json.JSONDecodeError:
            return None, "invalid_json"
        except Exception as e:
            return None, str(e)