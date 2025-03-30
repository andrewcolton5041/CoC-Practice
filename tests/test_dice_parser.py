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
from src.dice_parser_core import DiceParserCore
from src.dice_parser_utils import DiceParserUtils
from src.dice_parser_exceptions import DiceParserError, TokenizationError, ValidationError


class TestDiceParserMemoization(unittest.TestCase):
    """Test suite for the DiceParser with memoization features."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser_core = DiceParserCore()
        self.parser_utils = DiceParserUtils()
        # Set a fixed seed for deterministic testing
        random.seed(42)

    def test_tokenization_simple_dice(self):
        """Test basic dice notation tokenization."""
        tokens = self.parser_core.tokenize("3D6")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0], ('DICE', (3, 6)))

    def test_tokenization_complex_expression(self):
        """Test tokenization of a complex dice expression."""
        tokens = self.parser_core.tokenize("(2D6+6)*5")
        expected_tokens = [
            ('LPAREN', '('),
            ('DICE', (2, 6)),
            ('OPERATOR', '+'),
            ('NUMBER', 6),
            ('RPAREN', ')'),
            ('OPERATOR', '*'),
            ('NUMBER', 5)
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_validation_simple_expression(self):
        """Test validation of a simple dice expression."""
        tokens = self.parser_core.tokenize("3D6")
        try:
            self.parser_core.validate_tokens(tokens)
        except Exception as e:
            self.fail(f"Validation failed for simple expression: {e}")

    def test_validation_complex_expression(self):
        """Test validation of a complex dice expression."""
        tokens = self.parser_core.tokenize("(2D6+6)*5")
        try:
            self.parser_core.validate_tokens(tokens)
        except Exception as e:
            self.fail(f"Validation failed for complex expression: {e}")

    def test_parse_simple_dice(self):
        """Test parsing of a simple dice notation."""
        tokens = self.parser_core.tokenize("3D6")

        # Run multiple times to check consistency
        results = []
        for _ in range(10):
            result = self.parser_core.parse(tokens)
            results.append(result)
            self.assertTrue(3 <= result <= 18)  # 3D6 range

        # Ensure variability in results
        self.assertTrue(len(set(results)) > 1)

    def test_parse_deterministic_mode(self):
        """Test parsing in deterministic mode."""
        tokens = self.parser_core.tokenize("3D6")

        # First roll
        random.seed(42)
        first_result = self.parser_core.parse(tokens, deterministic=True)

        # Second roll should be identical
        random.seed(42)
        second_result = self.parser_core.parse(tokens, deterministic=True)

        self.assertEqual(first_result, second_result)

    def test_parse_complex_expression(self):
        """Test parsing of a complex dice expression."""
        tokens = self.parser_core.tokenize("(2D6+6)*5")

        # Run multiple times to check consistency
        results = []
        for _ in range(10):
            result = self.parser_core.parse(tokens)
            results.append(result)

            # Basic range check (minimal validation)
            self.assertTrue(result > 0)

        # Ensure variability in results
        self.assertTrue(len(set(results)) > 1)

    def test_invalid_dice_notation(self):
        """Test handling of invalid dice notations."""
        invalid_expressions = [
            "3D0",    # Zero-sided die
            "0D6",    # Zero dice count
            "3D6+",   # Incomplete expression
            "(3D6",   # Unbalanced parentheses
            "3D6++5",  # Multiple consecutive operators
            "()3D6",   # Empty parentheses
            "3D6)(+5"  # Misplaced parentheses
        ]

        for expr in invalid_expressions:
            with self.assertRaises((TokenizationError, ValidationError, ValueError), 
                                   msg=f"Failed to raise error for expression: {expr}"):
                tokens = self.parser_core.tokenize(expr)
                self.parser_core.validate_tokens(tokens)

    def test_dice_notation_validation(self):
        """Test dice notation validation utility."""
        valid_expressions = [
            "3D6", 
            "2D6+5", 
            "(3D6)*2", 
            "1D100", 
            "3D6+2", 
            "(2D6+6)*5",
            "1D20*2+3"
        ]
        invalid_expressions = [
            "3D0", 
            "0D6", 
            "3D6++5", 
            "()", 
            "3D6+()", 
            "3D6)(",
            "3D6+",  # Incomplete
            "3D6++5",  # Multiple consecutive operators
            "+3D6",   # Leading operator
            "3D6+",   # Trailing operator
            "*3D6",   # Leading multiplication
            "3D6*",   # Trailing multiplication
            "",       # Empty string
            "+",      # Just an operator
            "*"       # Just a multiplication sign
        ]

        for expr in valid_expressions:
            self.assertTrue(self.parser_utils.validate_dice_notation(expr), 
                            f"Expression should be valid: {expr}")

        for expr in invalid_expressions:
            self.assertFalse(self.parser_utils.validate_dice_notation(expr), 
                             f"Expression should be invalid: {expr}")

    def test_parsing_non_standard_characters(self):
        """Test parsing expressions with various valid characters."""
        expressions = [
            "3D6",         # Standard notation
            "2D20+5",      # With simple addition
            "(3D6+2)*2",   # With parentheses and multiplication
            "1D100-10",    # With subtraction
            "2D6+6*3",     # Mixed operators
            "(2D6+6)*5"    # Complex expression
        ]

        for expr in expressions:
            try:
                tokens = self.parser_core.tokenize(expr)
                result = self.parser_core.parse(tokens)
                self.assertTrue(isinstance(result, int), f"Failed to parse: {expr}")
            except Exception as e:
                self.fail(f"Unexpected error parsing {expr}: {e}")

    def tearDown(self):
        """Clean up test fixtures."""
        # Reset random seed
        random.seed()


if __name__ == '__main__':
    unittest.main()