"""
Function Cache Module for Call of Cthulhu Character Viewer

This module provides utilities for using LRU caching efficiently in the application.

Author: Unknown
Version: 1.0
Last Updated: 2025-03-30
"""

import functools
import time
import os
from collections import OrderedDict
from typing import Any, Callable, Dict, Optional

# Import constants for cache configuration
from src.constants import (
    DEFAULT_LRU_CACHE_SIZE,
    PERCENTAGE_MULTIPLIER
)

# Global registry to track cache statistics
_cache_registry = {}


def optimize_orderdict_usage(cache_obj: OrderedDict) -> None:
    """
    Helper function to optimize OrderedDict usage.

    This function can be used to patch existing code that uses the
    inefficient pattern of: item = cache.pop(key); cache[key] = item

    Instead, it should use: cache.move_to_end(key)

    Args:
        cache_obj: The OrderedDict instance to optimize
    """
    # This is a utility function that would be used to patch
    # existing code - in practice, new code should directly use
    # the move_to_end method
    pass


def get_cache_stats() -> Dict[str, Dict[str, Any]]:
    """
    Get statistics for all registered caches.

    Returns:
        Dictionary of cache statistics
    """
    result = {}

    for func_id, wrapper in _cache_registry.items():
        # Get cache info if available
        if hasattr(wrapper, 'cache_info'):
            info = wrapper.cache_info()

            # Calculate hit rate
            total = info.hits + info.misses
            hit_rate = (info.hits / total * PERCENTAGE_MULTIPLIER) if total > 0 else 0

            result[func_id] = {
                'hits': info.hits,
                'misses': info.misses,
                'total': total,
                'hit_rate': hit_rate,
                'maxsize': info.maxsize,
                'currsize': info.currsize
            }

    return result


def clear_all_caches() -> None:
    """Clear all registered caches."""
    for func_id, wrapper in _cache_registry.items():
        if hasattr(wrapper, 'cache_clear'):
            wrapper.cache_clear()


def register_cached_function(func_id: str, func: Callable) -> None:
    """
    Register a cached function for tracking.

    Args:
        func_id: Function identifier
        func: Cached function
    """
    _cache_registry[func_id] = func


# Patch for character data caching
def check_file_modification(filename: str, mod_times: Dict[str, float]) -> bool:
    """
    Check if a file has been modified since last access.

    Args:
        filename: Path to the file
        mod_times: Dictionary of file modification times

    Returns:
        True if file has been modified, False otherwise
    """
    try:
        current_mod_time = os.path.getmtime(filename)

        if filename in mod_times:
            if mod_times[filename] != current_mod_time:
                mod_times[filename] = current_mod_time
                return True
        else:
            mod_times[filename] = current_mod_time

        return False
    except (OSError, IOError):
        return True  # Assume modified if error


# Simple utility functions for working with standard lru_cache
def lru_cache(maxsize: int = DEFAULT_LRU_CACHE_SIZE, typed: bool = False):
    """
    Thin wrapper around functools.lru_cache that registers the function.

    Args:
        maxsize: Maximum cache size
        typed: Whether to use argument types in cache keys

    Returns:
        Decorator function
    """
    def decorator(func):
        # Apply standard lru_cache
        cached_func = functools.lru_cache(maxsize=maxsize, typed=typed)(func)

        # Register for statistics
        func_id = f"{func.__module__}.{func.__qualname__}"
        register_cached_function(func_id, cached_func)

        return cached_func

    return decorator


def get_cache_summary() -> str:
    """
    Get a human-readable summary of cache statistics.

    Returns:
        Formatted string with cache statistics
    """
    stats = get_cache_stats()

    if not stats:
        return "No cache statistics available."

    lines = ["=== Cache Statistics ==="]

    for func_id, func_stats in sorted(stats.items()):
        lines.append(f"{func_id}:")
        lines.append(f"  Hit rate: {func_stats['hit_rate']:.1f}% ({func_stats['hits']}/{func_stats['total']})")
        lines.append(f"  Cache size: {func_stats['currsize']}/{func_stats['maxsize']}")

    return "\n".join(lines)