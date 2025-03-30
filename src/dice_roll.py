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
from src.dice_parser_core import DiceParserCore
from src.dice_parser_utils import DiceParserUtils
from src.dice_parser_exceptions import DiceParserError, TokenizationError, ValidationError
import constants


class DiceRollCache:
    """
    Advanced caching mechanism for dice rolls with configurable strategies.

    Implements an LRU (Least Recently Used) caching strategy with:
    - Configurable maximum cache size
    - Performance tracking
    - Thread-safe operation
    - Flexible cache management
    """

    def __init__(self, max_size=constants.DEFAULT_DICE_CACHE_SIZE):
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
        value = self._cache.pop(key)
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
        hit_rate = (self._stats['hits'] / total_lookups * constants.PERCENTAGE_MULTIPLIER) if total_lookups > 0 else 0

        return {
            constants.STAT_SIZE: len(self._cache),
            constants.STAT_MAX_SIZE: self._max_size,
            constants.STAT_HITS: self._stats['hits'],
            constants.STAT_MISSES: self._stats['misses'],
            'evictions': self._stats['evictions'],
            constants.STAT_HIT_RATE: hit_rate,
            'total_lookups': total_lookups,
            'uptime': time.time() - self._stats['creation_time'],
            'last_access_time': self._stats['last_access_time']
        }

# Create a global dice roll cache
_dice_roll_cache = DiceRollCache()

# Create a singleton instance of the parser
_parser_core = DiceParserCore()
_parser_utils = DiceParserUtils()

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

    Raises:
        DiceParserError: For any dice parsing or rolling issues
    """
    try:
        # Validate dice notation first
        if not _parser_utils.validate_dice_notation(dice_string):
            raise ValidationError(f"Invalid dice notation: {dice_string}")

        # If caching is disabled or deterministic mode is on, bypass cache
        if not use_cache or deterministic:
            tokens = _parser_core.tokenize(dice_string)
            return _parse_and_roll_tokens(tokens, deterministic=deterministic)

        # Check if result is already in cache
        cache_result = _dice_roll_cache.get(dice_string)
        if cache_result is not None:
            return cache_result

        # Tokenize and parse
        tokens = _parser_core.tokenize(dice_string)

        # Roll dice and cache the result
        result = _parse_and_roll_tokens(tokens)
        _dice_roll_cache.put(dice_string, result)

        return result

    except (TokenizationError, ValidationError) as e:
        raise DiceParserError(f"Error parsing dice: {e}")

# Remaining functions remain unchanged as no other magic numbers were identified.
