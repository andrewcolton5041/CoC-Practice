"""
Character Cache Statistics Module for Call of Cthulhu Character Viewer

This module provides statistics tracking and reporting for the character cache,
offering insights into cache performance and memory usage.

Author: Unknown
Version: 2.1
Last Updated: 2025-03-30
"""

import time


def get_cache_stats(cache):
    """
    Get statistics about the character cache.

    Args:
        cache (CharacterCache): The character cache instance

    Returns:
        dict: Dictionary with cache statistics including:
            - size: Number of entries in the cache
            - active_entries: Number of active cache entries
            - files: List of filenames in the cache
            - memory_usage: Approximate memory usage in bytes
            - max_size: Maximum cache size setting
            - hit_rate: Percentage of successful cache retrievals
            - hits: Number of cache hits
            - misses: Number of cache misses
    """
    stats = {
        "size": len(cache._cache),
        "active_entries": len(cache._cache),
        "files": list(cache._cache.keys()),
        "memory_usage": sum(len(str(item)) for item in cache._cache.values()),
        "max_size": cache._max_size
    }

    # Calculate cache entry ages if cache is not empty
    if cache._cache:
        current_time = time.time()
        cache_times = [entry["cached_time"] for entry in cache._cache.values()]
        stats["oldest_entry_age"] = current_time - min(cache_times)
        stats["newest_entry_age"] = current_time - max(cache_times)

    # Calculate hit rate
    total_accesses = cache._hits + cache._misses
    stats["hit_rate"] = (cache._hits / total_accesses * 100) if total_accesses > 0 else 0
    stats["hits"] = cache._hits
    stats["misses"] = cache._misses

    return stats


def clear_cache(cache):
    """
    Clear the character cache and return statistics about the cleared cache.

    Args:
        cache (CharacterCache): The character cache instance

    Returns:
        dict: Statistics about the cache before clearing
    """
    # Capture current stats before clearing
    current_stats = get_cache_stats(cache)

    # Clear the cache
    cache.invalidate()

    return current_stats