"""
Character Cache Statistics Module for Call of Cthulhu Character Viewer

This module provides statistics tracking and reporting for the character cache,
offering insights into cache performance and memory usage.

Author: Unknown
Version: 2.1
Last Updated: 2025-03-30
"""

import time
from src.constants import (
    PERCENTAGE_MULTIPLIER,
    KEY_CACHE_TIME,
    STAT_SIZE,
    STAT_ACTIVE_ENTRIES,
    STAT_FILES,
    STAT_MEMORY_USAGE,
    STAT_MAX_SIZE,
    STAT_HIT_RATE,
    STAT_HITS,
    STAT_MISSES,
    STAT_OLDEST_AGE,
    STAT_NEWEST_AGE,
)

def get_cache_stats(cache):
    """
    Get statistics about the character cache.
    """
    stats = {
        STAT_SIZE: len(cache._cache),
        STAT_ACTIVE_ENTRIES: len(cache._cache),
        STAT_FILES: list(cache._cache.keys()),
        STAT_MEMORY_USAGE: sum(len(str(item)) for item in cache._cache.values()),
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

def clear_cache(cache):
    """
    Clear the character cache and return statistics about the cleared cache.
    """
    current_stats = get_cache_stats(cache)
    cache.invalidate()
    return current_stats
