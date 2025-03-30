"""
Test Dice Memoization Module for Call of Cthulhu Character Viewer

This module contains tests specifically for verifying that dice roll memoization
works correctly and provides significant performance improvements.

The tests focus on:
- Correctness of memoized vs. non-memoized results
- Performance improvements from memoization
- Proper cache invalidation
- Handling of cache hits and misses

Author: Unknown
Version: 1.0
Last Updated: 2025-03-30
"""

import unittest
import time
import random
import sys
import os
from unittest.mock import patch

# Add the src directory to the path so we can import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.dice_roll import roll_dice, clear_dice_cache, get_dice_cache_stats
from src.dice_parser_core import DiceParserCore
from src.dice_parser_utils import DiceParserUtils
from src.constants import (
    TEST_MEMO_DICE_ITERATIONS,
    TEST_MEMO_DICE_TYPES,
    TEST_MEMO_COMPARISON_THRESHOLD,
    TEST_MEMO_LARGE_DICE_COUNT,
    TEST_MEMO_TIMEOUT_SECONDS,
    TEST_MEMO_MIN_HIT_RATE,
    TEST_DICE_SEED
)


class TestDiceMemoization(unittest.TestCase):
    """Test suite for dice roll memoization functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Clear dice cache before each test
        clear_dice_cache()
        # Set fixed seed for reproducibility
        random.seed(TEST_DICE_SEED)
        # Create parser instances
        self.parser_core = DiceParserCore()
        self.parser_utils = DiceParserUtils()

    def test_basic_memoization_correctness(self):
        """Test that memoized dice rolls return consistent results when repeated."""
        # Set deterministic mode for testing
        with patch('random.randint', side_effect=lambda a, b: (a + b) // 2):
            # First roll with cache
            first_rolls = {}
            for dice in TEST_MEMO_DICE_TYPES:
                first_rolls[dice] = roll_dice(dice, use_cache=True)

            # Second roll with cache should return same values
            for dice in TEST_MEMO_DICE_TYPES:
                second_roll = roll_dice(dice, use_cache=True)
                self.assertEqual(
                    second_roll, 
                    first_rolls[dice],
                    f"Cached roll for {dice} returned different results"
                )

            # Now with cache disabled, should return same values in deterministic mode
            for dice in TEST_MEMO_DICE_TYPES:
                uncached_roll = roll_dice(dice, use_cache=False)
                self.assertEqual(
                    uncached_roll, 
                    first_rolls[dice],
                    f"Deterministic uncached roll for {dice} returned different results"
                )

    def test_memoization_performance(self):
        """Test that memoization provides significant performance improvements."""
        # Select a complex dice expression for testing
        complex_dice = "(3D6+2D8)*2+5"

        # Time uncached rolls
        clear_dice_cache()
        start_time = time.time()
        uncached_results = []
        for _ in range(TEST_MEMO_DICE_ITERATIONS):
            uncached_results.append(roll_dice(complex_dice, use_cache=False))
        uncached_time = time.time() - start_time

        # Time cached rolls
        clear_dice_cache()
        start_time = time.time()
        cached_results = []
        for _ in range(TEST_MEMO_DICE_ITERATIONS):
            cached_results.append(roll_dice(complex_dice, use_cache=True))
        cached_time = time.time() - start_time

        # Calculate speedup factor
        if cached_time > 0:  # Avoid division by zero
            speedup = uncached_time / cached_time
            # Allow for some variability but should see significant improvement
            self.assertGreater(
                speedup, 
                TEST_MEMO_COMPARISON_THRESHOLD,
                f"Memoization speedup factor of {speedup:.2f}x is below threshold"
            )

        # Verify cache hit rate
        stats = get_dice_cache_stats()
        hit_rate = stats.get('hit_rate', 0)
        self.assertGreater(
            hit_rate, 
            TEST_MEMO_MIN_HIT_RATE,
            f"Cache hit rate of {hit_rate:.2f}% is below minimum threshold"
        )

    def test_memoization_with_different_dice_notations(self):
        """Test that the same underlying dice roll is recognized despite notation differences."""
        # These notations are semantically equivalent with the same dice count and sides
        equivalent_notations = [
            "3D6",  # Standard
            "3d6",  # Lowercase
            " 3D6 ",  # Whitespace
            "3 D 6"  # Spaced out
        ]

        # Roll the first notation
        first_roll = roll_dice(equivalent_notations[0], use_cache=True)

        # All equivalent notations should be treated the same and return the cached result
        for notation in equivalent_notations[1:]:
            next_roll = roll_dice(notation, use_cache=True)
            self.assertEqual(
                first_roll, 
                next_roll,
                f"Equivalent notation {notation} not properly memoized"
            )

        # Get cache stats to verify we have cache hits
        stats = get_dice_cache_stats()
        self.assertGreater(
            stats.get('hits', 0), 
            0,
            "No cache hits recorded for equivalent notations"
        )

    def test_large_dice_expressions(self):
        """Test memoization with large dice expressions."""
        # Create a very large dice expression
        large_expr = "+".join([f"1D6" for _ in range(TEST_MEMO_LARGE_DICE_COUNT)])

        # Time how long it takes without memoization (should be slower)
        start_time = time.time()
        uncached_result = roll_dice(large_expr, use_cache=False)
        uncached_time = time.time() - start_time

        # Time with memoization for first roll (should be similar to uncached)
        clear_dice_cache()
        start_time = time.time()
        first_cached_result = roll_dice(large_expr, use_cache=True)
        first_cached_time = time.time() - start_time

        # Time with memoization for second roll (should be much faster)
        start_time = time.time()
        second_cached_result = roll_dice(large_expr, use_cache=True)
        second_cached_time = time.time() - start_time

        # Second cached call should be significantly faster
        self.assertLess(
            second_cached_time,
            first_cached_time / TEST_MEMO_COMPARISON_THRESHOLD,
            "Second cached call not significantly faster than first"
        )

        # And should complete within timeout
        self.assertLess(
            second_cached_time,
            TEST_MEMO_TIMEOUT_SECONDS,
            f"Cached lookup took too long: {second_cached_time:.4f}s"
        )

        # Results should be deterministic with the same seed
        random.seed(TEST_DICE_SEED)
        repeat_result = roll_dice(large_expr, use_cache=False)
        self.assertEqual(uncached_result, repeat_result)

    def test_cache_size_management(self):
        """Test that the cache size is properly managed and doesn't grow unbounded."""
        # Generate many unique dice notations to fill the cache
        unique_dice = [f"{i}D{100-i}" for i in range(1, 100)]

        # Roll each unique dice expression
        for dice in unique_dice:
            roll_dice(dice, use_cache=True)

        # Get cache stats
        stats = get_dice_cache_stats()

        # Cache size should be limited
        self.assertLessEqual(
            stats.get('size', float('inf')),
            stats.get('max_size', float('inf')),
            "Cache size exceeded maximum size"
        )

        # Ensure we had evictions if we exceeded the max size
        if len(unique_dice) > stats.get('max_size', float('inf')):
            self.assertGreater(
                stats.get('evictions', 0),
                0,
                "No cache evictions recorded despite exceeding max size"
            )

    def test_deterministic_mode_bypass(self):
        """Test that deterministic mode bypasses the cache."""
        # Use a simple dice expression
        dice = "2D10"

        # First roll with deterministic mode should bypass cache
        first_roll = roll_dice(dice, deterministic=True)

        # Get stats after first roll
        stats1 = get_dice_cache_stats()

        # Second roll with deterministic mode should also bypass cache
        second_roll = roll_dice(dice, deterministic=True)

        # Get stats after second roll
        stats2 = get_dice_cache_stats()

        # Cache statistics should remain unchanged
        self.assertEqual(
            stats1.get('hits', 0), 
            stats2.get('hits', 0),
            "Cache hits changed despite deterministic mode"
        )
        self.assertEqual(
            stats1.get('misses', 0), 
            stats2.get('misses', 0),
            "Cache misses changed despite deterministic mode"
        )

    def test_cache_invalidation(self):
        """Test that cache can be properly invalidated."""
        # Roll some dice to populate the cache
        for dice in TEST_MEMO_DICE_TYPES:
            roll_dice(dice, use_cache=True)

        # Get stats before clearing
        before_stats = get_dice_cache_stats()
        self.assertGreater(
            before_stats.get('size', 0), 
            0,
            "Cache not populated before invalidation test"
        )

        # Clear the cache
        clear_dice_cache()

        # Get stats after clearing
        after_stats = get_dice_cache_stats()
        self.assertEqual(
            after_stats.get('size', -1), 
            0,
            "Cache not properly cleared"
        )

        # Roll again and make sure it's treated as a cache miss
        roll_dice(TEST_MEMO_DICE_TYPES[0], use_cache=True)
        new_stats = get_dice_cache_stats()
        self.assertGreater(
            new_stats.get('misses', 0), 
            after_stats.get('misses', 0),
            "Cache miss not recorded after invalidation"
        )

    def tearDown(self):
        """Clean up test fixtures."""
        clear_dice_cache()
        random.seed()  # Reset random seed


if __name__ == '__main__':
    unittest.main()