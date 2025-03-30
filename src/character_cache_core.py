"""
Character Cache Core Module for Call of Cthulhu Character Viewer

This module provides the core caching mechanism for character data,
focusing on the fundamental caching operations and least recently used (LRU) policy.

Author: Unknown
Version: 2.1
Last Updated: 2025-03-30
"""

import os
import json
import time
from collections import OrderedDict

# Constants
DEFAULT_CACHE_SIZE = 15
KEY_DATA = "data"
KEY_MOD_TIME = "mod_time"
KEY_CACHE_TIME = "cache_time"

class CharacterCache:
    """
    A class to manage caching of character data with intelligent invalidation and
    memory optimization using an LRU eviction policy.

    This cache stores character data and implements an LRU policy to limit cache size,
    automatically removing the least recently used entries when needed.
    """

    def __init__(self, max_size=DEFAULT_CACHE_SIZE):
        """
        Initialize a character cache with memory optimization.

        Args:
            max_size (int): Maximum number of characters to keep in cache
        """
        self._cache = OrderedDict()
        self._max_size = max_size
        self._hits = 0
        self._misses = 0

    def get(self, filename):
        """
        Retrieve character data from the cache if available and current.

        Args:
            filename (str): Path to the character file

        Returns:
            dict or None: The cached character data if available and current, None otherwise
        """
        if filename not in self._cache:
            self._misses += 1
            return None

        entry = self._cache.pop(filename)
        self._cache[filename] = entry

        try:
            current_mod_time = os.path.getmtime(filename)
            if current_mod_time != entry[KEY_MOD_TIME]:
                del self._cache[filename]
                self._misses += 1
                return None

            self._hits += 1
            return entry[KEY_DATA]

        except OSError:
            self._misses += 1
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
            if len(self._cache) >= self._max_size and filename not in self._cache:
                self._cache.popitem(last=False)

            mod_time = os.path.getmtime(filename)
            self._cache[filename] = {
                KEY_DATA: data,
                KEY_MOD_TIME: mod_time,
                KEY_CACHE_TIME: time.time()
            }

            return True

        except OSError:
            return False

    def invalidate(self, filename=None):
        """
        Invalidate entries in the cache.

        Args:
            filename (str, optional): Specific file to remove from cache. If None, clears all.

        Returns:
            bool: True if invalidation was successful, False if file not in cache
        """
        if filename is None:
            self._cache.clear()
            return True
        elif filename in self._cache:
            del self._cache[filename]
            return True
        else:
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
        """
        cached_data = self.get(filename)
        if cached_data:
            return cached_data, "cache_hit"

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                character_data = json.load(f)

            if validation_function and not validation_function(character_data):
                return None, "validation_failed"

            self.put(filename, character_data)
            return character_data, "loaded_from_file"

        except FileNotFoundError:
            return None, "file_not_found"
        except json.JSONDecodeError:
            return None, "invalid_json"
        except Exception as e:
            return None, str(e)
