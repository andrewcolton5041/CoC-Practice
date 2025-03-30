"""
Character Cache Core Module for Call of Cthulhu Character Viewer

This module provides the core caching mechanism for character data,
focusing on the fundamental caching operations and least recently used (LRU) policy.

Author: Unknown
Version: 2.3
Last Updated: 2025-03-30
"""

import time
import functools
from collections import OrderedDict
from typing import Dict, Any, Tuple, Optional, Callable

from src.constants import (
    DEFAULT_CACHE_SIZE,
    KEY_DATA,
    KEY_MOD_TIME,
    KEY_CACHE_TIME,
    STATUS_CACHE_HIT,
    STATUS_LOADED_FROM_FILE,
    STATUS_VALIDATION_FAILED,
    STATUS_FILE_NOT_FOUND,
    STATUS_INVALID_JSON
)
from src.file_utils import read_json_file, get_file_modification_time
from src.cache_stats import CacheStats


class CharacterCache:
    """
    A class to manage caching of character data with intelligent invalidation and
    memory optimization using an LRU eviction policy.
    """

    def __init__(self, max_size=DEFAULT_CACHE_SIZE):
        """
        Initialize a character cache with memory optimization.

        Args:
            max_size (int): Maximum number of entries to keep in the cache
        """
        self._cache = OrderedDict()
        self._max_size = max_size
        self._hits = 0
        self._misses = 0
        self._cache_stats = CacheStats()

    def get(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve character data from the cache if available and current.

        Args:
            filename (str): Path to the character file

        Returns:
            dict or None: Character data or None if not in cache or outdated
        """
        if filename not in self._cache:
            self._misses += 1
            self._cache_stats.record_miss()
            return None

        # Use move_to_end() instead of pop/re-add pattern for better efficiency
        self._cache.move_to_end(filename)
        entry = self._cache[filename]

        try:
            # Check if file has been modified using lru_cached function
            current_mod_time = self._get_file_mod_time(filename)
            if current_mod_time is None or current_mod_time != entry[KEY_MOD_TIME]:
                del self._cache[filename]
                self._misses += 1
                self._cache_stats.record_miss()
                return None

            self._hits += 1
            self._cache_stats.record_hit()
            return entry[KEY_DATA]

        except Exception:
            self._misses += 1
            self._cache_stats.record_miss()
            return None

    @functools.lru_cache(maxsize=128)
    def _get_file_mod_time(self, filename: str) -> Optional[float]:
        """
        Get file modification time with caching for performance.

        Args:
            filename (str): Path to the file

        Returns:
            float or None: Modification time or None if file doesn't exist
        """
        return get_file_modification_time(filename)

    def put(self, filename: str, data: Dict[str, Any]) -> bool:
        """
        Add or update character data in the cache.

        Args:
            filename (str): Path to the character file
            data (dict): Character data to cache

        Returns:
            bool: True if caching was successful, False otherwise
        """
        try:
            # Evict least recently used item if cache is full
            if len(self._cache) >= self._max_size and filename not in self._cache:
                self._cache.popitem(last=False)
                self._cache_stats.record_eviction()

            mod_time = self._get_file_mod_time(filename)
            if mod_time is None:
                return False

            self._cache[filename] = {
                KEY_DATA: data,
                KEY_MOD_TIME: mod_time,
                KEY_CACHE_TIME: time.time()
            }

            # Move this entry to the end to mark as most recently used
            self._cache.move_to_end(filename)
            return True

        except Exception:
            return False

    def invalidate(self, filename: Optional[str] = None) -> bool:
        """
        Invalidate entries in the cache.

        Args:
            filename (str, optional): Specific file to invalidate, or None to invalidate all

        Returns:
            bool: True if invalidation was successful, False otherwise
        """
        if filename is None:
            self._cache.clear()
            # Also clear the file mod time cache
            self._get_file_mod_time.cache_clear()
            return True
        elif filename in self._cache:
            del self._cache[filename]
            # Invalidate specific file in mod time cache
            self._get_file_mod_time.cache_clear()
            return True
        else:
            return False

    def contains(self, filename: str) -> bool:
        """
        Check if a file is currently in the cache.

        Args:
            filename (str): Path to the character file

        Returns:
            bool: True if in cache, False otherwise
        """
        return filename in self._cache

    @functools.lru_cache(maxsize=32)
    def _cached_validation(self, data_tuple: Tuple, validation_function: Callable) -> bool:
        """
        Cached validation using immutable data representation.

        Args:
            data_tuple: Tuple representation of data for cache key
            validation_function: Function to validate the data

        Returns:
            bool: True if valid, False otherwise
        """
        # Convert back to dictionary for validation
        # (This is just for the cache key - the actual data isn't modified)
        return validation_function(dict(data_tuple))

    def load_character(self, filename: str, validation_function: Optional[Callable] = None) -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Load a character from the cache or from disk if not cached.

        Args:
            filename (str): Path to the character file
            validation_function (callable, optional): Function to validate character data

        Returns:
            tuple: (character_data, status) where character_data is the character data
                  (or None on error) and status is a string indicating success or error type
        """
        cached_data = self.get(filename)
        if cached_data:
            if validation_function:
                # Convert dict to tuple of items for caching
                cached_items = tuple(sorted(cached_data.items()))
                if not self._cached_validation(cached_items, validation_function):
                    return None, STATUS_VALIDATION_FAILED
            return cached_data, STATUS_CACHE_HIT

        character_data, status = read_json_file(filename)

        if status != "success":
            return None, status

        if validation_function:
            character_items = tuple(sorted(character_data.items()))
            if not self._cached_validation(character_items, validation_function):
                return None, STATUS_VALIDATION_FAILED

        self.put(filename, character_data)
        return character_data, STATUS_LOADED_FROM_FILE