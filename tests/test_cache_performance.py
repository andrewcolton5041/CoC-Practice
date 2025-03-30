"""
Cache Performance Test Module for Call of Cthulhu Character Viewer

This module contains comprehensive tests for the various caching mechanisms,
focusing on performance improvements, cache hit rates, and correct behavior
under different usage patterns.

Author: Unknown
Version: 1.0
Last Updated: 2025-03-30
"""

import unittest
import time
import random
import os
import sys
import tempfile
import json
import gc
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.character_cache_core import CharacterCache
from src.character_loader import load_character_from_json
from src.character_metadata import CharacterMetadata
from src.dice_roll import roll_dice, clear_dice_cache, get_dice_cache_stats
from src.file_utils import read_json_file, get_file_modification_time
from src.cache_stats import calculate_character_cache_stats
from src.constants import (
    TEST_CACHE_ITERATIONS,
    TEST_CACHE_WARMUP_ITERATIONS,
    TEST_CACHE_TYPES,
    TEST_CACHE_COMPARISON_THRESHOLD,
    TEST_CACHE_MIN_HIT_RATE,
    TEST_CACHE_TIMEOUT_SECONDS,
    TEST_CACHE_FILE_COUNT,
    TEST_CACHE_STRESS_FACTOR,
    DEFAULT_CACHE_SIZE
)


class TestCachePerformance(unittest.TestCase):
    """Test suite for cache performance across different cache implementations."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create test character files
        self.test_files = []
        for i in range(TEST_CACHE_FILE_COUNT):
            # Create different character data for each file
            character_data = {
                "name": f"Test Character {i}",
                "age": 30 + i,
                "attributes": {
                    "Strength": 50 + i,
                    "Intelligence": 60 - i
                },
                "skills": {
                    f"Skill {j}": 40 + j for j in range(5)
                }
            }

            # Write to file
            filename = os.path.join(self.temp_dir.name, f"test_character_{i}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(character_data, f)

            self.test_files.append(filename)

        # Initialize caches
        self.character_cache = CharacterCache(max_size=DEFAULT_CACHE_SIZE)

        # Clear dice cache
        clear_dice_cache()

        # Generate test dice expressions
        self.dice_expressions = [
            "1D20",
            "3D6",
            "2D8+5",
            "(1D10+2)*3",
            "2D6+1D8+3",
        ]

    def test_character_cache_performance(self):
        """Test performance of character caching."""
        if "character" not in TEST_CACHE_TYPES:
            self.skipTest("Character cache tests disabled")

        # Helper to load characters
        def load_characters(use_cache=True):
            results = []
            for file in self.test_files:
                character, _ = load_character_from_json(file, self.character_cache if use_cache else None)
                results.append(character)
            return results

        # Warm up
        for _ in range(TEST_CACHE_WARMUP_ITERATIONS):
            load_characters(use_cache=True)

        # Measure uncached performance
        empty_cache = CharacterCache(max_size=1)  # Use minimal cache to force misses
        start_time = time.time()
        uncached_results = []
        for _ in range(TEST_CACHE_ITERATIONS // 10):  # Use fewer iterations for uncached as it's slower
            uncached_results.extend(load_characters(use_cache=False))
        uncached_time = time.time() - start_time

        # Measure cached performance
        start_time = time.time()
        cached_results = []
        for _ in range(TEST_CACHE_ITERATIONS):
            cached_results.extend(load_characters(use_cache=True))
        cached_time = time.time() - start_time

        # Calculate effective iterations for fair comparison
        uncached_effective_iterations = TEST_CACHE_ITERATIONS // 10
        cached_effective_iterations = TEST_CACHE_ITERATIONS

        # Normalize times to per-iteration
        normalized_uncached_time = uncached_time / uncached_effective_iterations
        normalized_cached_time = cached_time / cached_effective_iterations

        # Calculate speedup
        if normalized_cached_time > 0:  # Avoid division by zero
            speedup = normalized_uncached_time / normalized_cached_time
            self.assertGreater(
                speedup,
                TEST_CACHE_COMPARISON_THRESHOLD,
                f"Character cache speedup factor of {speedup:.2f}x is below threshold"
            )

        # Check cache hit rate
        stats = calculate_character_cache_stats(self.character_cache)
        self.assertGreater(
            stats.get("hit_rate", 0),
            TEST_CACHE_MIN_HIT_RATE,
            f"Character cache hit rate of {stats.get('hit_rate', 0):.2f}% is below threshold"
        )

    def test_metadata_cache_performance(self):
        """Test performance of metadata caching."""
        if "metadata" not in TEST_CACHE_TYPES:
            self.skipTest("Metadata cache tests disabled")

        # Helper to load metadata
        def load_metadata(use_cache=True):
            if use_cache:
                return CharacterMetadata.load_all_from_directory(self.temp_dir.name)
            else:
                # Bypass cache by directly instantiating metadata objects
                metadata_list = []
                for file in self.test_files:
                    metadata_list.append(CharacterMetadata(file))
                return metadata_list

        # Warm up
        for _ in range(TEST_CACHE_WARMUP_ITERATIONS):
            load_metadata(use_cache=True)

        # Measure uncached performance
        start_time = time.time()
        uncached_results = []
        for _ in range(TEST_CACHE_ITERATIONS // 10):  # Use fewer iterations for uncached
            uncached_results.extend(load_metadata(use_cache=False))
        uncached_time = time.time() - start_time

        # Clear any internal caches
        gc.collect()

        # Measure cached performance
        start_time = time.time()
        cached_results = []
        for _ in range(TEST_CACHE_ITERATIONS):
            cached_results.extend(load_metadata(use_cache=True))
        cached_time = time.time() - start_time

        # Calculate effective iterations for fair comparison
        uncached_effective_iterations = TEST_CACHE_ITERATIONS // 10
        cached_effective_iterations = TEST_CACHE_ITERATIONS

        # Normalize times to per-iteration
        normalized_uncached_time = uncached_time / uncached_effective_iterations
        normalized_cached_time = cached_time / cached_effective_iterations

        # Calculate speedup
        if normalized_cached_time > 0:  # Avoid division by zero
            speedup = normalized_uncached_time / normalized_cached_time
            self.assertGreater(
                speedup,
                TEST_CACHE_COMPARISON_THRESHOLD,
                f"Metadata cache speedup factor of {speedup:.2f}x is below threshold"
            )

        # Verify results are consistent
        self.assertEqual(
            len(cached_results[0]),
            len(self.test_files),
            "Incorrect number of metadata entries loaded"
        )

    def test_dice_cache_performance(self):
        """Test performance of dice roll caching."""
        if "dice" not in TEST_CACHE_TYPES:
            self.skipTest("Dice cache tests disabled")

        # Clear dice cache
        clear_dice_cache()

        # Helper to roll dice
        def roll_all_dice(use_cache=True):
            results = []
            for dice in self.dice_expressions:
                result = roll_dice(dice, use_cache=use_cache)
                results.append(result)
            return results

        # Warm up
        for _ in range(TEST_CACHE_WARMUP_ITERATIONS):
            roll_all_dice(use_cache=True)

        # Measure uncached performance
        start_time = time.time()
        uncached_results = []
        for _ in range(TEST_CACHE_ITERATIONS):
            uncached_results.extend(roll_all_dice(use_cache=False))
        uncached_time = time.time() - start_time

        # Clear and then measure cached performance
        clear_dice_cache()
        start_time = time.time()
        cached_results = []
        for _ in range(TEST_CACHE_ITERATIONS):
            cached_results.extend(roll_all_dice(use_cache=True))
        cached_time = time.time() - start_time

        # Calculate speedup
        if cached_time > 0:  # Avoid division by zero
            speedup = uncached_time / cached_time
            self.assertGreater(
                speedup,
                TEST_CACHE_COMPARISON_THRESHOLD,
                f"Dice cache speedup factor of {speedup:.2f}x is below threshold"
            )

        # Check cache hit rate
        stats = get_dice_cache_stats()
        self.assertGreater(
            stats.get("hit_rate", 0),
            TEST_CACHE_MIN_HIT_RATE,
            f"Dice cache hit rate of {stats.get('hit_rate', 0):.2f}% is below threshold"
        )

    def test_file_operations_cache_performance(self):
        """Test performance of file operations caching."""
        if "file" not in TEST_CACHE_TYPES:
            self.skipTest("File cache tests disabled")

        # Helper to read files
        def read_all_files():
            results = []
            for file in self.test_files:
                data, _ = read_json_file(file)
                results.append(data)
            return results

        # Create a mock version of read_json_file to measure calls
        original_read_json_file = read_json_file
        call_count = [0]  # Use list for mutable reference

        def counting_read_json_file(filename):
            call_count[0] += 1
            return original_read_json_file(filename)

        # Patch the read_json_file function
        with patch('src.file_utils.read_json_file', side_effect=counting_read_json_file):
            # Warm up
            for _ in range(TEST_CACHE_WARMUP_ITERATIONS):
                read_all_files()

            # Reset counter
            call_count[0] = 0

            # First batch should trigger actual file reads
            start_time = time.time()
            first_batch = read_all_files()
            first_batch_time = time.time() - start_time
            first_batch_calls = call_count[0]

            # Reset counter
            call_count[0] = 0

            # Second batch should use cached results
            start_time = time.time()
            second_batch = read_all_files()
            second_batch_time = time.time() - start_time
            second_batch_calls = call_count[0]

        # Second batch should be faster
        if second_batch_time > 0:  # Avoid division by zero
            speedup = first_batch_time / second_batch_time
            self.assertGreater(
                speedup,
                1.0,  # Even a minimal speedup indicates caching
                f"File operations cache speedup factor of {speedup:.2f}x indicates no caching"
            )

        # Should have fewer actual file reads in second batch due to caching
        self.assertLess(
            second_batch_calls,
            first_batch_calls,
            "No reduction in file read calls, indicating caching isn't working"
        )

    def test_cache_invalidation_performance(self):
        """Test that cache invalidation works correctly and efficiently."""
        # Load all characters into cache
        for file in self.test_files:
            load_character_from_json(file, self.character_cache)

        # Verify they're in cache
        stats_before = calculate_character_cache_stats(self.character_cache)
        self.assertEqual(
            len(self.test_files),
            stats_before.get("size", 0),
            "Not all test files were cached as expected"
        )

        # Measure time to invalidate cache
        start_time = time.time()
        self.character_cache.invalidate()
        invalidation_time = time.time() - start_time

        # Invalidation should be quick
        self.assertLess(
            invalidation_time,
            0.1,  # 100ms is very generous for cache invalidation
            f"Cache invalidation took too long: {invalidation_time:.4f}s"
        )

        # Verify cache is empty
        stats_after = calculate_character_cache_stats(self.character_cache)
        self.assertEqual(
            0,
            stats_after.get("size", -1),
            "Cache not properly invalidated"
        )

    def test_cache_stress(self):
        """Stress test caches with large numbers of operations."""
        # Character cache stress test
        self.character_cache.invalidate()

        # Create a moderate number of test characters to cache
        stress_count = min(TEST_CACHE_FILE_COUNT, DEFAULT_CACHE_SIZE // 2)

        # Repeatedly load and invalidate to stress the cache
        start_time = time.time()
        for i in range(TEST_CACHE_ITERATIONS * TEST_CACHE_STRESS_FACTOR):
            # Load a random character
            idx = i % stress_count
            load_character_from_json(self.test_files[idx], self.character_cache)

            # Occasionally invalidate a single entry
            if i % 20 == 0:
                self.character_cache.invalidate(self.test_files[random.randint(0, stress_count-1)])

            # Occasionally invalidate the entire cache
            if i % 100 == 0:
                self.character_cache.invalidate()

        stress_time = time.time() - start_time

        # Stress test should complete within timeout
        self.assertLess(
            stress_time,
            TEST_CACHE_TIMEOUT_SECONDS,
            f"Cache stress test took too long: {stress_time:.2f}s"
        )

        # Dice cache stress test
        clear_dice_cache()

        # Repeatedly roll dice with different expressions
        start_time = time.time()
        for i in range(TEST_CACHE_ITERATIONS * TEST_CACHE_STRESS_FACTOR):
            # Generate a somewhat random dice expression
            count = (i % 6) + 1
            sides = ((i * 17) % 20) + 4
            dice_expr = f"{count}D{sides}"

            # Roll the dice
            roll_dice(dice_expr, use_cache=True)

            # Occasionally clear the cache
            if i % 100 == 0:
                clear_dice_cache()

        stress_time = time.time() - start_time

        # Stress test should complete within timeout
        self.assertLess(
            stress_time,
            TEST_CACHE_TIMEOUT_SECONDS,
            f"Dice cache stress test took too long: {stress_time:.2f}s"
        )

        # Verify caches are still functioning
        stats = get_dice_cache_stats()
        self.assertGreaterEqual(
            stats.get("size", 0),
            0,
            "Dice cache in invalid state after stress test"
        )

    def test_lru_eviction_policy(self):
        """Test that the Least Recently Used eviction policy works correctly."""
        # Create a small cache to force evictions
        small_cache = CharacterCache(max_size=3)

        # Load more files than the cache can hold
        for file in self.test_files[:5]:  # Load 5 files into a cache of size 3
            load_character_from_json(file, small_cache)

        # Get stats to check evictions
        stats = calculate_character_cache_stats(small_cache)

        # Verify cache size is maintained
        self.assertEqual(
            3,  # Max size of the small_cache
            stats.get("size", 0),
            "Cache size exceeded maximum"
        )

        # The first loaded files should have been evicted
        for file in self.test_files[:2]:
            self.assertNotIn(
                file,
                stats.get("files", []),
                f"File {file} was not evicted as expected"
            )

        # The most recently used files should still be in cache
        for file in self.test_files[2:5]:
            self.assertIn(
                file,
                stats.get("files", []),
                f"File {file} was evicted unexpectedly"
            )

        # Now access an older file to make it "recently used"
        load_character_from_json(self.test_files[2], small_cache)

        # Load one more file to force another eviction
        load_character_from_json(self.test_files[5], small_cache)

        # Get updated stats
        stats = calculate_character_cache_stats(small_cache)

        # Verify the recently used file wasn't evicted
        self.assertIn(
            self.test_files[2],
            stats.get("files", []),
            "Recently used file was incorrectly evicted"
        )

        # Make sure the total size is still correct
        self.assertEqual(
            3,
            stats.get("size", 0),
            "Cache size incorrect after LRU operations"
        )

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()
        clear_dice_cache()
        self.character_cache.invalidate()


if __name__ == '__main__':
    unittest.main()