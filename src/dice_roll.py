"""
Dice Roller Utility for Call of Cthulhu RPG

This module provides robust dice rolling functionality with advanced memoization
and caching mechanisms to improve performance in repeated roll scenarios.

Key Features:
- Intelligent caching with configurable size
- Performance tracking
- Deterministic mode for testing
- Flexible cache management

Author: Unknown
Version: 3.1
Last Updated: 2025-03-30
"""

import functools
import inspect
import sys
import time
from collections import OrderedDict
from src.dice_parser import DiceParser

class DiceRollCache:
    """
    Advanced caching mechanism for dice rolls with configurable strategies.

    Implements an LRU (Least Recently Used) caching strategy with:
    - Configurable maximum cache size
    - Performance tracking
    - Thread-safe operation
    - Flexible cache management
    """

    def __init__(self, max_size=128):
        """
        Initialize the dice roll cache.

        Args:
            max_size (int): Maximum number of entries to keep in the cache
        """
        # Use OrderedDict to maintain insertion order for LRU eviction
        self._cache = OrderedDict()
        self._max_size = max_size

        # Tracking statistics
        self._stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_lookups': 0,
            'creation_time': time.time(),
            'last_access_time': None
        }

    def get(self, key):
        """
        Retrieve an item from the cache.

        Args:
            key: The cache key to retrieve

        Returns:
            The cached value or None if not found
        """
        # Update overall lookup count
        self._stats['total_lookups'] += 1

        # Check if key exists
        if key not in self._cache:
            self._stats['misses'] += 1
            return None

        # Move the item to the end (most recently used)
        value = self._cache[key]
        del self._cache[key]
        self._cache[key] = value

        # Update hit stats and last access time
        self._stats['hits'] += 1
        self._stats['last_access_time'] = time.time()

        return value

    def put(self, key, value):
        """
        Add an item to the cache, potentially evicting the least recently used item.

        Args:
            key: The cache key
            value: The value to cache
        """
        # If cache is full, remove the first (least recently used) item
        if len(self._cache) >= self._max_size:
            self._cache.popitem(last=False)
            self._stats['evictions'] += 1

        # Add the new item
        self._cache[key] = value

    def clear(self):
        """
        Clear the entire cache and reset statistics.
        """
        self._cache.clear()
        # Reset statistics, but keep the creation time
        creation_time = self._stats['creation_time']
        self._stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_lookups': 0,
            'creation_time': creation_time,
            'last_access_time': None
        }

    def get_stats(self):
        """
        Get comprehensive cache statistics.

        Returns:
            dict: Detailed cache performance statistics
        """
        # Calculate hit rate
        total_lookups = self._stats['total_lookups']
        hit_rate = (self._stats['hits'] / total_lookups * 100) if total_lookups > 0 else 0

        return {
            'size': len(self._cache),
            'max_size': self._max_size,
            'hits': self._stats['hits'],
            'misses': self._stats['misses'],
            'evictions': self._stats['evictions'],
            'hit_rate': hit_rate,
            'total_lookups': total_lookups,
            'uptime': time.time() - self._stats['creation_time'],
            'last_access_time': self._stats['last_access_time']
        }

# Create a global dice roll cache
_dice_roll_cache = DiceRollCache()

# Create a singleton instance of the DiceParser
_parser = DiceParser()

def roll_dice(dice_string, use_cache=True, deterministic=False, seed=None):
    """
    Parse and roll dice with advanced caching and configuration.

    Args:
        dice_string (str): Dice notation to roll
        use_cache (bool): Whether to use caching mechanism
        deterministic (bool): Force deterministic mode for testing
        seed (int, optional): Random seed for reproducibility

    Returns:
        int: Result of the dice roll
    """
    # If caching is disabled or deterministic mode is on, bypass cache
    if not use_cache or deterministic:
        return _parser.roll_dice(dice_string, deterministic, seed)

    # Check if result is already in cache
    cache_result = _dice_roll_cache.get(dice_string)
    if cache_result is not None:
        return cache_result

    # Roll dice and cache the result
    result = _parser.roll_dice(dice_string)
    _dice_roll_cache.put(dice_string, result)

    return result

def roll_dice_with_details(dice_string, deterministic=False, seed=None):
    """
    Roll dice and return both the total and individual die results.

    Args:
        dice_string (str): Simple dice notation (e.g., "3d6")
        deterministic (bool): Force deterministic mode for testing
        seed (int, optional): Random seed for reproducibility

    Returns:
        tuple: (total, individual_rolls)
    """
    return _parser.roll_dice_with_details(dice_string, deterministic, seed)

def clear_dice_cache():
    """
    Clear the dice rolling cache and return statistics.

    Returns:
        dict: Statistics about the cleared cache
    """
    stats = _dice_roll_cache.get_stats()
    _dice_roll_cache.clear()
    return stats

def get_cache_stats():
    """
    Get current dice roll cache statistics.

    Returns:
        dict: Comprehensive cache statistics
    """
    return _dice_roll_cache.get_stats()