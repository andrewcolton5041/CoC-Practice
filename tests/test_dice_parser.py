"""
Test module for the optimized dice parser implementation.

This module contains tests for the dice parser functionality,
verifying that it correctly handles various dice notation formats
and edge cases using the new regex-based tokenization approach.

Author: Unknown
Version: 2.0
Last Updated: 2025-03-30
"""

import unittest
import random
import time
import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.dice_parser import DiceParser


class TestDiceParser(unittest.TestCase):
    """Test suite for the DiceParser class."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = DiceParser()
        # Set a fixed seed for deterministic testing
        random.seed(42)

    def test_tokenize_simple(self):
        """Test tokenizing of simple dice expressions."""
        tokens = self.parser.tokenize("3D6")
        self.assertEqual(tokens, [('DICE', (3, 6))])

        tokens = self.parser.tokenize("1D20")
        self.assertEqual(tokens, [('DICE', (1, 20))])

    def test_tokenize_with_modifiers(self):
        """Test tokenizing of dice expressions with modifiers."""
        tokens = self.parser.tokenize("3D6+5")
        self.assertEqual(tokens, [('DICE', (3, 6)), ('OPERATOR', '+'), ('NUMBER', 5)])

        tokens = self.parser.tokenize("1D20-3")
        self.assertEqual(tokens, [('DICE', (1, 20)), ('OPERATOR', '-'), ('NUMBER', 3)])

    def test_tokenize_complex(self):
        """Test tokenizing of complex dice expressions."""
        tokens = self.parser.tokenize("(2D6+6)*5")
        self.assertEqual(tokens, [
            ('LPAREN', '('), 
            ('DICE', (2, 6)), 
            ('OPERATOR', '+'), 
            ('NUMBER', 6), 
            ('RPAREN', ')'), 
            ('OPERATOR', '*'), 
            ('NUMBER', 5)
        ])

    def test_tokenize_whitespace(self):
        """Test that whitespace is correctly handled."""
        tokens = self.parser.tokenize("3 D 6 + 5")
        self.assertEqual(tokens, [('DICE', (3, 6)), ('OPERATOR', '+'), ('NUMBER', 5)])

    def test_tokenize_invalid(self):
        """Test that invalid dice expressions raise appropriate errors."""
        with self.assertRaises(ValueError):
            self.parser.tokenize("3D")  # Missing sides value

        with self.assertRaises(ValueError):
            self.parser.tokenize("D6")  # Missing count value

        with self.assertRaises(ValueError):
            self.parser.tokenize("3D6X")  # Invalid character

        with self.assertRaises(ValueError):
            self.parser.tokenize("")  # Empty string

    def test_parse_simple(self):
        """Test parsing of simple dice expressions."""
        # Use fixed random values for testing
        random.seed(42)

        # Test parsing basic dice expressions
        tokens = self.parser.tokenize("3D6")
        result = self.parser.parse(tokens)
        self.assertIsInstance(result, int)
        self.assertTrue(3 <= result <= 18)  # 3d6 range

        tokens = self.parser.tokenize("1D20")
        result = self.parser.parse(tokens)
        self.assertIsInstance(result, int)
        self.assertTrue(1 <= result <= 20)  # 1d20 range

    def test_parse_with_modifiers(self):
        """Test parsing of dice expressions with modifiers."""
        # Use fixed random values for testing
        random.seed(42)

        # We can't check exact values due to randomness, but we can verify ranges
        tokens = self.parser.tokenize("3D6+5")
        result = self.parser.parse(tokens)
        self.assertTrue(8 <= result <= 23)  # 3d6+5 range

        tokens = self.parser.tokenize("1D20-3")
        result = self.parser.parse(tokens)
        self.assertTrue(-2 <= result <= 17)  # 1d20-3 range

    def test_parse_complex(self):
        """Test parsing of complex dice expressions."""
        # Use fixed random values for testing
        random.seed(42)

        tokens = self.parser.tokenize("(2D6+6)*5")
        result = self.parser.parse(tokens)
        # (2d6+6)*5 range: (2-12+6)*5 = (8-18)*5 = 40-90
        self.assertTrue(40 <= result <= 90)

    def test_roll_dice(self):
        """Test the combined tokenize and parse functionality."""
        # Use fixed random values for testing
        random.seed(42)

        result = self.parser.roll_dice("3D6")
        self.assertTrue(3 <= result <= 18)

        result = self.parser.roll_dice("1D20+5")
        self.assertTrue(6 <= result <= 25)

        result = self.parser.roll_dice("(2D6+6)*5")
        self.assertTrue(40 <= result <= 90)

    def test_roll_dice_with_details(self):
        """Test the roll_dice_with_details functionality."""
        # Use fixed random values for testing
        random.seed(42)

        total, rolls = self.parser.roll_dice_with_details("3D6")
        self.assertEqual(len(rolls), 3)  # Check we have 3 dice
        self.assertEqual(sum(rolls), total)  # Check the total is correct
        for roll in rolls:
            self.assertTrue(1 <= roll <= 6)  # Check each die is in range

    def test_invalid_dice_with_details(self):
        """Test error handling for roll_dice_with_details."""
        with self.assertRaises(ValueError):
            self.parser.roll_dice_with_details("3D6+5")  # Not a simple dice roll

    def test_performance(self):
        """Test the performance of the new tokenization implementation."""
        # Generate a complex dice expression
        complex_expr = "+".join([f"{i}D{20-i}" for i in range(1, 10)])

        # Time how long it takes to tokenize and parse
        start_time = time.time()
        for _ in range(1000):
            tokens = self.parser.tokenize(complex_expr)
        tokenize_time = time.time() - start_time

        # This is just to verify it runs and doesn't need to be compared
        # to the old implementation in the test itself
        self.assertLess(tokenize_time, 5.0)  # Should be much faster than 5 seconds

        # Log the time for manual verification if needed
        print(f"\nTokenization performance for 1000 iterations: {tokenize_time:.4f} seconds")

    def test_case_insensitivity(self):
        """Test that the parser handles different case variations."""
        tokens_upper = self.parser.tokenize("3D6")
        tokens_lower = self.parser.tokenize("3d6")
        tokens_mixed = self.parser.tokenize("3D6")

        self.assertEqual(tokens_upper, tokens_lower)
        self.assertEqual(tokens_upper, tokens_mixed)

    def test_parentheses_matching(self):
        """Test proper handling of nested parentheses."""
        # Simple parentheses
        tokens = self.parser.tokenize("(3D6)")
        self.assertEqual(tokens, [
            ('LPAREN', '('), 
            ('DICE', (3, 6)), 
            ('RPAREN', ')')
        ])

        # Nested parentheses
        tokens = self.parser.tokenize("((1D20+5)*2)")
        self.assertEqual(tokens, [
            ('LPAREN', '('), 
            ('LPAREN', '('), 
            ('DICE', (1, 20)), 
            ('OPERATOR', '+'), 
            ('NUMBER', 5), 
            ('RPAREN', ')'), 
            ('OPERATOR', '*'), 
            ('NUMBER', 2), 
            ('RPAREN', ')')
        ])

        # Mismatched parentheses should raise an error when parsing
        tokens = self.parser.tokenize("(3D6")
        with self.assertRaises(ValueError):
            self.parser.parse(tokens)

    def tearDown(self):
        """Clean up test fixtures."""
        # Reset random seed
        random.seed()


if __name__ == '__main__':
    unittest.main()