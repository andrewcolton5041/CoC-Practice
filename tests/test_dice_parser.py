"""
Test module for the optimized dice parser implementation with memoization.

This module contains tests for the dice parser functionality,
verifying that it correctly handles memoization, caching, and performance
improvements for repeated dice rolls.

Author: Unknown
Version: 2.1
Last Updated: 2025-03-30
"""

import unittest
import random
import time
import sys
import os
import functools

# Add the src directory to the path so we can import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.dice_parser import DiceParser


class TestDiceParserMemoization(unittest.TestCase):
    """Test suite for the DiceParser class with memoization features."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = DiceParser()
        # Set a fixed seed for deterministic testing
        random.seed(42)

    def test_memoization_identical_rolls(self):
        """Test that identical dice rolls return the same result when memoized."""
        # Enable deterministic mode for consistent testing
        self.parser.set_deterministic_mode(True)

        # Roll the same dice expression multiple times
        dice_string = "3D6"
        first_roll = self.parser.roll_dice(dice_string)
        second_roll = self.parser.roll_dice(dice_string)
        third_roll = self.parser.roll_dice(dice_string)

        # Verify that all rolls are identical
        self.assertEqual(first_roll, second_roll)
        self.assertEqual(first_roll, third_roll)

    def test_memoization_performance(self):
        """
        Test the performance improvement of memoization for repeated dice rolls.

        This test checks that subsequent identical rolls are faster than the first roll.
        """
        # Use a complex dice expression
        dice_string = "(2D6+6)*5"

        # First roll (uncached)
        start_time = time.time()
        first_roll = self.parser.roll_dice(dice_string)
        first_roll_time = time.time() - start_time

        # Subsequent rolls (should benefit from memoization)
        rolls = []
        total_time = 0
        num_rolls = 100

        for _ in range(num_rolls):
            start_time = time.time()
            roll = self.parser.roll_dice(dice_string)
            roll_time = time.time() - start_time

            rolls.append(roll)
            total_time += roll_time

        # Verify that the first roll is significantly slower than subsequent rolls
        # Allow some variance, but subsequent rolls should be much faster
        avg_subsequent_time = total_time / num_rolls

        # First roll should take at least 5x longer than subsequent rolls
        self.assertGreater(first_roll_time, avg_subsequent_time * 5)

        # Verify that all subsequent rolls are consistent
        self.assertTrue(all(roll == first_roll for roll in rolls))

    def test_memoization_different_expressions(self):
        """
        Test that different dice expressions are handled separately in memoization.
        """
        # Enable deterministic mode for consistent testing
        self.parser.set_deterministic_mode(True)

        # Roll different dice expressions
        expr1 = "3D6"
        expr2 = "3D6+5"
        expr3 = "(2D6+6)*5"

        roll1_first = self.parser.roll_dice(expr1)
        roll2_first = self.parser.roll_dice(expr2)
        roll3_first = self.parser.roll_dice(expr3)

        # Repeat the rolls
        roll1_second = self.parser.roll_dice(expr1)
        roll2_second = self.parser.roll_dice(expr2)
        roll3_second = self.parser.roll_dice(expr3)

        # Verify that each expression maintains its own memoized result
        self.assertEqual(roll1_first, roll1_second)
        self.assertEqual(roll2_first, roll2_second)
        self.assertEqual(roll3_first, roll3_second)

        # Ensure the results are different between expressions
        self.assertNotEqual(roll1_first, roll2_first)
        self.assertNotEqual(roll1_first, roll3_first)
        self.assertNotEqual(roll2_first, roll3_first)

    def test_cache_size_limit(self):
        """
        Test that the cache respects a maximum size limit.
        """
        # A helper method to count unique rolls
        def count_unique_rolls(expressions):
            unique_rolls = set()
            for expr in expressions:
                unique_rolls.add(self.parser.roll_dice(expr))
            return len(unique_rolls)

        # Generate more expressions than the expected cache size
        expressions = [f"{i}D6" for i in range(1, 20)]  # More than typical cache size

        # Count unique rolls to verify cache behavior
        unique_roll_count = count_unique_rolls(expressions)

        # The number of unique rolls should be limited
        # Exact number depends on implementation, but should be significantly less than total expressions
        self.assertLess(unique_roll_count, len(expressions))
        self.assertGreater(unique_roll_count, 0)

    def test_cache_invalidation(self):
        """
        Test cache invalidation mechanisms.
        """
        # Enable deterministic mode for consistent testing
        self.parser.set_deterministic_mode(True)

        # Initial roll
        expr = "3D6"
        first_roll = self.parser.roll_dice(expr)

        # Roll again (should return cached result)
        second_roll = self.parser.roll_dice(expr)
        self.assertEqual(first_roll, second_roll)

        # Simulate cache invalidation by changing mode
        self.parser.set_deterministic_mode(False)

        # Roll should now be different
        third_roll = self.parser.roll_dice(expr)
        self.assertNotEqual(first_roll, third_roll)

    def test_cache_details_with_details(self):
        """
        Test memoization with roll_dice_with_details method.
        """
        # Enable deterministic mode for consistent testing
        self.parser.set_deterministic_mode(True)

        # Initial roll with details
        expr = "3D6"
        first_total, first_rolls = self.parser.roll_dice_with_details(expr)

        # Repeat roll
        second_total, second_rolls = self.parser.roll_dice_with_details(expr)

        # Verify total and individual rolls are identical
        self.assertEqual(first_total, second_total)
        self.assertEqual(first_rolls, second_rolls)

    def tearDown(self):
        """Clean up test fixtures."""
        # Reset random seed
        random.seed()
        # Reset parser state
        self.parser.set_deterministic_mode(False)


if __name__ == '__main__':
    unittest.main()