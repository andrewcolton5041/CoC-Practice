"""
Cache Decorators Module for Call of Cthulhu Character Viewer

This module provides optimized caching decorators that leverage functools.lru_cache
while adding additional functionality specific to different use cases.

Author: Unknown
Version: 1.0
Last Updated: 2025-03-30
"""

import functools
import os
import time
from typing import Any, Callable, Dict, Optional, TypeVar

from src.constants import (
    DEFAULT_LRU_CACHE_SIZE,
    DEFAULT_CHARACTER_CACHE_SIZE,
    DEFAULT_METADATA_CACHE_SIZE,
    DEFAULT_FILE_CACHE_SIZE,
    DEFAULT_SKILL_CACHE_SIZE,
    DEFAULT_DICE_LRU_CACHE_SIZE
)

# Type variables for better type hints
R = TypeVar('R')

# Global registry of file modification times for each function
_file_mod_times: Dict[str, Dict[str, float]] = {}


def monitored_lru_cache(maxsize: int = DEFAULT_LRU_CACHE_SIZE, typed: bool = False):
    """
    Standard LRU cache decorator using functools.lru_cache directly.

    Args:
        maxsize: Maximum cache size
        typed: Whether different argument types should be cached separately

    Returns:
        Decorator function
    """
    return functools.lru_cache(maxsize=maxsize, typed=typed)


def character_cache(maxsize: int = DEFAULT_CHARACTER_CACHE_SIZE):
    """
    Cache decorator for character loading functions.

    This decorator handles file modification time tracking to invalidate the cache
    when a character file has been modified.

    Args:
        maxsize: Maximum cache size

    Returns:
        Decorator function
    """
    def decorator(func):
        # Create function-specific cache
        cached_func = functools.lru_cache(maxsize=maxsize)(func)

        # Get function ID for tracking
        func_id = f"{func.__module__}.{func.__qualname__}"

        # Initialize file modification times dictionary for this function
        if func_id not in _file_mod_times:
            _file_mod_times[func_id] = {}

        # Create wrapper function that checks file modification time
        @functools.wraps(func)
        def wrapper(filename, *args, **kwargs):
            file_times = _file_mod_times[func_id]

            try:
                # Check if file has been modified
                current_mod_time = os.path.getmtime(filename)

                # If file is tracked and has been modified, invalidate cache
                if filename in file_times and file_times[filename] != current_mod_time:
                    cached_func.cache_clear()

                # Update modification time
                file_times[filename] = current_mod_time

            except (OSError, IOError):
                # Can't check modification time, proceed anyway
                pass

            # Call cached function
            return cached_func(filename, *args, **kwargs)

        # Function to clear modification times
        def clear_mod_times():
            """Clear file modification times for this function."""
            if func_id in _file_mod_times:
                _file_mod_times[func_id].clear()

        # Store file modification clearing function in module-level dict
        globals()[f"clear_mod_times_{func_id.replace('.', '_')}"] = clear_mod_times

        return wrapper

    return decorator


def metadata_cache(maxsize: int = DEFAULT_METADATA_CACHE_SIZE):
    """
    Cache decorator for character metadata functions.
    Uses the same implementation as character_cache.

    Args:
        maxsize: Maximum cache size

    Returns:
        Decorator function
    """
    return character_cache(maxsize=maxsize)


def file_operation_cache(maxsize: int = DEFAULT_FILE_CACHE_SIZE):
    """
    Cache decorator for file operation functions.
    Uses the same implementation as character_cache.

    Args:
        maxsize: Maximum cache size

    Returns:
        Decorator function
    """
    return character_cache(maxsize=maxsize)


def dice_roll_cache(maxsize: int = DEFAULT_DICE_LRU_CACHE_SIZE):
    """
    Cache decorator for dice rolling functions.

    This decorator handles special cases like deterministic mode,
    which should bypass the cache.

    Args:
        maxsize: Maximum cache size

    Returns:
        Decorator function
    """
    def decorator(func):
        # Create cached function
        cached_func = functools.lru_cache(maxsize=maxsize)(func)

        @functools.wraps(func)
        def wrapper(dice_string, *args, **kwargs):
            # Check for deterministic mode or explicit cache bypass
            deterministic = kwargs.get('deterministic', False)
            use_cache = kwargs.get('use_cache', True)

            if deterministic or not use_cache:
                # Bypass cache for deterministic mode
                return func(dice_string, *args, **kwargs)

            # Use cached function
            return cached_func(dice_string, *args, **kwargs)

        return wrapper

    return decorator


def skill_check_cache(maxsize: int = DEFAULT_SKILL_CACHE_SIZE):
    """
    Cache decorator for skill check functions.

    This decorator handles character data by extracting the specific
    skill value for caching rather than using the entire character dict.

    Args:
        maxsize: Maximum cache size

    Returns:
        Decorator function
    """
    def decorator(func):
        # Create cached function for skill values
        cached_func = functools.lru_cache(maxsize=maxsize)(func)

        @functools.wraps(func)
        def wrapper(character_data, skill_name, *args, **kwargs):
            # Handle mutable character data
            if isinstance(character_data, dict):
                skill_value = None

                # Try to get skill value
                if 'skills' in character_data and skill_name in character_data['skills']:
                    skill_value = character_data['skills'][skill_name]
                elif 'attributes' in character_data and skill_name in character_data['attributes']:
                    skill_value = character_data['attributes'][skill_name]

                if skill_value is not None:
                    # Use skill value directly for caching
                    return cached_func(skill_value, skill_name, *args, **kwargs)

            # If we can't extract skill value, call original function
            return func(character_data, skill_name, *args, **kwargs)

        return wrapper

    return decorator


def memoize(func):
    """
    Simple memoization decorator for functions with immutable arguments.
    Uses unlimited cache size.

    Args:
        func: Function to memoize

    Returns:
        Decorated function with caching
    """
    return functools.lru_cache(maxsize=None)(func)


def clear_mod_times(func=None):
    """
    Clear file modification times for a function or all functions.

    Args:
        func: Function or None to clear times for all functions
    """
    if func is None:
        # Clear all modification times
        _file_mod_times.clear()
    else:
        # Get function ID
        func_id = f"{func.__module__}.{func.__qualname__}"
        if func_id in _file_mod_times:
            _file_mod_times[func_id].clear()


def get_all_mod_times():
    """
    Get all file modification times.

    Returns:
        Dictionary of file modification times
    """
    return _file_mod_times.copy()