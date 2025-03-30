"""
Character Cache Utility Functions for Call of Cthulhu Character Viewer

This module provides additional utility functions related to character caching.

Author: Unknown
Version: 2.2
Last Updated: 2025-03-30
"""

from typing import Dict, Any, List, Optional, Tuple

from src.character_cache_core import CharacterCache
from src.validation import validate_character_data
from src.cache_stats import calculate_character_cache_stats, clear_cache_and_get_stats
from src.constants import (
    DEFAULT_CACHE_SIZE,
    CACHE_SIZE_MIN,
    CACHE_SIZE_MAX
)
from src.error_handling import log_error, display_user_error


def create_cache(max_size: int = DEFAULT_CACHE_SIZE) -> CharacterCache:
    """
    Create a new character cache with the specified maximum size.

    Args:
        max_size (int): Maximum number of entries to keep in the cache

    Returns:
        CharacterCache: A new character cache instance
    """
    if max_size < CACHE_SIZE_MIN:
        log_error("invalid_cache_size", f"Cache size {max_size} is below minimum {CACHE_SIZE_MIN}")
        max_size = CACHE_SIZE_MIN
    elif max_size > CACHE_SIZE_MAX:
        log_error("invalid_cache_size", f"Cache size {max_size} exceeds maximum {CACHE_SIZE_MAX}")
        max_size = CACHE_SIZE_MAX

    return CharacterCache(max_size=max_size)


def resize_cache(cache: CharacterCache, new_size: int) -> Tuple[bool, CharacterCache]:
    """
    Resize an existing cache, preserving its most recently used entries.

    Args:
        cache (CharacterCache): Existing cache to resize
        new_size (int): New maximum size for the cache

    Returns:
        tuple: (success, new_cache) where success is a boolean and new_cache
               is the resized cache or the original if resizing failed
    """
    try:
        if new_size < CACHE_SIZE_MIN or new_size > CACHE_SIZE_MAX:
            display_user_error(
                "invalid_cache_size", 
                f"Cache size must be between {CACHE_SIZE_MIN} and {CACHE_SIZE_MAX}"
            )
            return False, cache

        # Create a new cache with the specified size
        new_cache = CharacterCache(max_size=new_size)

        # Get current cache stats and entries
        stats = calculate_character_cache_stats(cache)

        # Transfer entries from old cache to new cache (most recent first)
        entries_to_keep = min(new_size, len(stats["files"]))
        for filename in stats["files"][-entries_to_keep:]:
            if cache.contains(filename):
                data = cache.get(filename)
                if data:
                    new_cache.put(filename, data)

        return True, new_cache

    except Exception as e:
        log_error("cache_resize_error", f"Error resizing cache: {str(e)}")
        return False, cache


def get_cache_usage_report(cache: CharacterCache) -> str:
    """
    Generate a human-readable report of cache usage.

    Args:
        cache (CharacterCache): Cache to report on

    Returns:
        str: Formatted cache usage report
    """
    stats = calculate_character_cache_stats(cache)

    report = [
        "=== Cache Usage Report ===",
        f"Entries: {stats.get('size', 0)}/{stats.get('max_size', 0)} ({stats.get('hit_rate', 0):.1f}% hit rate)",
        f"Hits: {stats.get('hits', 0)}, Misses: {stats.get('misses', 0)}",
        f"Memory usage: {stats.get('memory_usage', 0)/1024:.1f} KB"
    ]

    if stats.get('size', 0) > 0:
        report.append("\nCached files:")
        for i, filename in enumerate(stats.get('files', []), 1):
            report.append(f"{i}. {filename}")

    return "\n".join(report)


def preload_characters(cache: CharacterCache, filenames: List[str]) -> int:
    """
    Preload a list of character files into the cache.

    Args:
        cache (CharacterCache): Cache to preload into
        filenames (list): List of character file paths to preload

    Returns:
        int: Number of successfully preloaded characters
    """
    successfully_loaded = 0

    for filename in filenames:
        character_data, status = cache.load_character(filename, validate_character_data)
        if character_data is not None:
            successfully_loaded += 1

    return successfully_loaded