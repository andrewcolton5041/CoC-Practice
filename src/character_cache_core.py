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
from src.constants import (
    DEFAULT_CACHE_SIZE,
    DEFAULT_ENCODING,
    KEY_DATA,
    KEY_MOD_TIME,
    KEY_CACHE_TIME,
    STATUS_CACHE_HIT,
    STATUS_LOADED_FROM_FILE,
    STATUS_VALIDATION_FAILED,
    STATUS_FILE_NOT_FOUND,
    STATUS_INVALID_JSON,
)

class CharacterCache:
    """
    A class to manage caching of character data with intelligent invalidation and
    memory optimization using an LRU eviction policy.
    """

    def __init__(self, max_size=DEFAULT_CACHE_SIZE):
        """
        Initialize a character cache with memory optimization.
        """
        self._cache = OrderedDict()
        self._max_size = max_size
        self._hits = 0
        self._misses = 0

    def get(self, filename):
        """
        Retrieve character data from the cache if available and current.
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
        """
        return filename in self._cache

    def load_character(self, filename, validation_function=None):
        """
        Load a character from the cache or from disk if not cached.
        """
        cached_data = self.get(filename)
        if cached_data:
            return cached_data, STATUS_CACHE_HIT

        try:
            with open(filename, 'r', encoding=DEFAULT_ENCODING) as f:
                character_data = json.load(f)

            if validation_function and not validation_function(character_data):
                return None, STATUS_VALIDATION_FAILED

            self.put(filename, character_data)
            return character_data, STATUS_LOADED_FROM_FILE

        except FileNotFoundError:
            return None, STATUS_FILE_NOT_FOUND
        except json.JSONDecodeError:
            return None, STATUS_INVALID_JSON
        except Exception as e:
            return None, str(e)
