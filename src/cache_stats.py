"""
Cache Statistics Module for Call of Cthulhu Character Viewer

This module provides a unified approach to tracking and reporting
cache statistics for different caching systems in the application.

Author: Unknown
Version: 1.0
Last Updated: 2025-03-30
"""

import time
from typing import Dict, Any, List, Optional
from collections import OrderedDict

from src.constants import (
    PERCENTAGE_MULTIPLIER,
    STAT_SIZE,
    STAT_ACTIVE_ENTRIES,
    STAT_MAX_SIZE,
    STAT_HIT_RATE,
    STAT_HITS,
    STAT_MISSES,
    STAT_OLDEST_AGE,
    STAT_NEWEST_AGE,
    STAT_MEMORY_USAGE,
    STAT_FILES,
    KEY_CACHE_TIME,
    MEMORY_CALCULATION_METHOD
)


class CacheStats:
    """
    Generic class for tracking and reporting cache statistics.
    Can be used with different types of caches throughout the application.
    """

    def __init__(self):
        """Initialize cache statistics tracking."""
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._creation_time = time.time()
        self._last_access_time = None

    def record_hit(self) -> None:
        """Record a cache hit."""
        self._hits += 1
        self._last_access_time = time.time()

    def record_miss(self) -> None:
        """Record a cache miss."""
        self._misses += 1
        self._last_access_time = time.time()

    def record_eviction(self) -> None:
        """Record a cache eviction."""
        self._evictions += 1

    def reset(self) -> None:
        """Reset all statistics except creation time."""
        creation_time = self._creation_time
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._creation_time = creation_time
        self._last_access_time = None

    def get_hit_rate(self) -> float:
        """
        Calculate the cache hit rate as a percentage.

        Returns:
            float: Hit rate percentage
        """
        total = self._hits + self._misses
        if total == 0:
            return 0.0
        return (self._hits / total) * PERCENTAGE_MULTIPLIER

    def get_uptime(self) -> float:
        """
        Get the cache uptime in seconds.

        Returns:
            float: Uptime in seconds
        """
        return time.time() - self._creation_time


def calculate_memory_usage(cache_data: Dict[Any, Any]) -> int:
    """
    Calculate the memory usage of cache data.

    Args:
        cache_data: The cache data dictionary

    Returns:
        int: Estimated memory usage in bytes
    """
    if MEMORY_CALCULATION_METHOD == "string_representation":
        return sum(len(str(item)) for item in cache_data.values())
    else:
        # Default fallback method
        return sum(len(str(item)) for item in cache_data.values())


def calculate_character_cache_stats(cache) -> Dict[str, Any]:
    """
    Calculate comprehensive statistics for a character cache.

    Args:
        cache: The character cache object

    Returns:
        dict: Cache statistics
    """
    stats = {
        STAT_SIZE: len(cache._cache),
        STAT_ACTIVE_ENTRIES: len(cache._cache),
        STAT_FILES: list(cache._cache.keys()),
        STAT_MEMORY_USAGE: calculate_memory_usage(cache._cache),
        STAT_MAX_SIZE: cache._max_size
    }

    if cache._cache:
        current_time = time.time()
        cache_times = [entry[KEY_CACHE_TIME] for entry in cache._cache.values()]
        stats[STAT_OLDEST_AGE] = current_time - min(cache_times)
        stats[STAT_NEWEST_AGE] = current_time - max(cache_times)

    total_accesses = cache._hits + cache._misses
    stats[STAT_HIT_RATE] = (
        (cache._hits / total_accesses) * PERCENTAGE_MULTIPLIER
        if total_accesses > 0 else 0
    )
    stats[STAT_HITS] = cache._hits
    stats[STAT_MISSES] = cache._misses

    return stats


def calculate_dice_cache_stats(dice_cache) -> Dict[str, Any]:
    """
    Calculate comprehensive statistics for a dice roll cache.

    Args:
        dice_cache: The dice roll cache object

    Returns:
        dict: Cache statistics
    """
    # Get basic stats
    stats = {
        STAT_SIZE: len(dice_cache._cache),
        STAT_MAX_SIZE: dice_cache._max_size,
        STAT_HITS: dice_cache._stats['hits'],
        STAT_MISSES: dice_cache._stats['misses'],
        'evictions': dice_cache._stats['evictions'],
        STAT_HIT_RATE: dice_cache.get_stats()[STAT_HIT_RATE],
        'total_lookups': dice_cache._stats['total_lookups'],
        'uptime': time.time() - dice_cache._stats['creation_time'],
    }

    # Add last access time if available
    if dice_cache._stats['last_access_time']:
        stats['last_access_time'] = dice_cache._stats['last_access_time']

    return stats


def clear_cache_and_get_stats(cache) -> Dict[str, Any]:
    """
    Clear a cache and return its statistics before clearing.

    Args:
        cache: The cache object to clear

    Returns:
        dict: Cache statistics before clearing
    """
    if hasattr(cache, '_cache_stats'):
        # For caches using the new CacheStats class
        stats = calculate_character_cache_stats(cache)
        cache.invalidate()
        cache._cache_stats.reset()
    else:
        # For backward compatibility with older cache implementations
        stats = calculate_character_cache_stats(cache)
        cache.invalidate()

    return stats