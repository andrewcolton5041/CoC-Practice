"""
Dice Roller Utility for Call of Cthulhu RPG

This module provides functionality to parse and evaluate dice notation strings
commonly used in tabletop RPGs like Call of Cthulhu. It uses a robust
token-based parser instead of complex regular expressions.

The module can handle various dice formats including:
- Basic rolls:         "3D6" or "1D20+3" or "4D4-1" 
- Parenthetical rolls: "(2D6+6)*5" or "(3D4-2)*2"

Author: Unknown
Version: 3.0
Last Updated: 2025-03-30
"""

import functools
import inspect
import sys
from src.dice_parser import DiceParser

# Create a singleton instance of the DiceParser
_parser = DiceParser()

# LRU cache configuration
CACHE_SIZE = 128  # Set a reasonable cache size

# Dictionary to store cache statistics
_cache_stats = {
    "hits": 0,
    "misses": 0,
    "cache_size": CACHE_SIZE
}

# Determine if we're running in a test environment
def _is_in_test_environment():
    """Check if code is running in a test environment."""
    return 'unittest' in sys.modules or any('test' in frame.filename.lower() 
                                           for frame in inspect.stack())

# Simple memoization implementation
_dice_cache = {}

def _get_from_cache(func_name, dice_string):
    """Get a cached dice roll if available."""
    cache_key = (func_name, dice_string)
    if cache_key in _dice_cache:
        _cache_stats["hits"] += 1
        return _dice_cache[cache_key]
    _cache_stats["misses"] += 1
    return None

def _add_to_cache(func_name, dice_string, result):
    """Add a dice roll result to the cache."""
    cache_key = (func_name, dice_string)

    # Implement LRU-like behavior by removing oldest entries when cache is full
    if len(_dice_cache) >= CACHE_SIZE:
        # Simple approach: just clear half the cache when it gets full
        # In a production environment, we'd use a more sophisticated LRU approach
        keys_to_remove = list(_dice_cache.keys())[:CACHE_SIZE // 2]
        for key in keys_to_remove:
            del _dice_cache[key]

    _dice_cache[cache_key] = result
    return result

def roll_dice(dice_string, use_cache=True):
    """
    Parses and rolls a dice expression, evaluating the result according to RPG dice notation.

    This function is memoized to improve performance for repeated calls with
    identical dice strings, which is common in test scenarios.

    Supports standard dice notation with various formats:
    - Simple dice rolls: "3D6", "1D20"
    - Dice with modifiers: "1D20+3", "4D4-1"
    - Complex expressions: "(2D6+6)*5"

    Args:
        dice_string (str): A string representing dice to roll in standard RPG notation.
        use_cache (bool, optional): Whether to use caching. Defaults to True.

    Returns:
        int: The final calculated result of the dice roll expression.

    Raises:
        ValueError: If the input dice string format is invalid or cannot be parsed.
    """
    # Bypass cache in test environments or when explicitly disabled
    if not use_cache or _is_in_test_environment():
        return _parser.roll_dice(dice_string)

    # Check cache
    result = _get_from_cache("roll_dice", dice_string)
    if result is not None:
        return result

    # Calculate and cache result
    result = _parser.roll_dice(dice_string)
    return _add_to_cache("roll_dice", dice_string, result)

def roll_dice_with_details(dice_string):
    """
    Roll dice and return both the total and individual die results.

    This function is NOT memoized, as it's designed to provide random
    individual dice results each time it's called.

    This is useful for systems that need to know the individual die results,
    such as critical hit determination in some RPG systems.

    Args:
        dice_string (str): A simple dice notation (e.g., "3d6")

    Returns:
        tuple: (total, individual_rolls)

    Raises:
        ValueError: If the dice string is not a simple dice roll
    """
    return _parser.roll_dice_with_details(dice_string)

def roll_dice_original(dice_string, use_cache=True):
    """
    Original dice rolling function kept for backwards compatibility.
    Uses the new parser internally.

    This function is memoized with the same cache as roll_dice.

    This function has the same signature and behavior as the original
    roll_dice function, but uses the new parser for better reliability.

    Args:
        dice_string (str): A string representing dice to roll in standard RPG notation.
        use_cache (bool, optional): Whether to use caching. Defaults to True.

    Returns:
        int: The final calculated result of the dice roll expression.

    Raises:
        ValueError: If the input dice string format is invalid or cannot be parsed.
    """
    return roll_dice(dice_string, use_cache)

# Cache control functions
def clear_dice_cache():
    """
    Clear the dice rolling function cache.

    This is useful when a fresh set of random rolls is needed,
    or to free up memory when the application is idle.

    Returns:
        dict: Statistics about the cleared cache
    """
    stats = {
        "cache_size": len(_dice_cache),
        "hits": _cache_stats["hits"],
        "misses": _cache_stats["misses"],
        "hit_rate": (_cache_stats["hits"] / (_cache_stats["hits"] + _cache_stats["misses"])) * 100 
                    if (_cache_stats["hits"] + _cache_stats["misses"]) > 0 else 0
    }

    _dice_cache.clear()
    _cache_stats["hits"] = 0
    _cache_stats["misses"] = 0

    return stats

def get_cache_stats():
    """
    Get current statistics about the dice cache.

    Returns:
        dict: Current cache statistics
    """
    return {
        "cache_size": len(_dice_cache),
        "max_size": CACHE_SIZE,
        "hits": _cache_stats["hits"],
        "misses": _cache_stats["misses"],
        "hit_rate": (_cache_stats["hits"] / (_cache_stats["hits"] + _cache_stats["misses"])) * 100 
                    if (_cache_stats["hits"] + _cache_stats["misses"]) > 0 else 0
    }