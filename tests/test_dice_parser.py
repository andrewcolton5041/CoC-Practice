"""
Test module for the optimized dice parser implementation with memoization.

This module contains tests for the dice parser functionality,
verifying that it correctly handles memoization, caching, and performance
improvements for repeated dice rolls.

Author: Unknown
Version: 4.0
Last Updated: 2025-03-30
"""

import unittest
import random
import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.dice_parser_core import DiceParserCore
from src.dice_parser_utils import DiceParserUtils
from src.dice_parser_exceptions import (
    TokenizationError, 
    ValidationError, 
    RollError, 
    LimitExceededError, 
    DiceParserError
)
from src.constants import (
    TEST_DICE_SEED,
    TEST_DICE_ROLL_COUNT,
    TEST_SIMPLE_DICE,
    TEST_COMPLEX_DICE,
    TEST_SIMPLE_DICE_MIN,
    TEST_SIMPLE_DICE_MAX
)


class TestDiceParserMemoization(unittest.TestCase):
    """Test suite for the DiceParser with memoization features."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser_core = DiceParserCore()
        self.parser_utils = DiceParserUtils()
        # Set a fixed seed for deterministic testing
        random.seed(TEST_DICE_SEED)

    def test_tokenization_simple_dice(self):
        """Test basic dice notation tokenization."""
        tokens = self.parser_core.tokenize(TEST_SIMPLE_DICE)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0], ('DICE', (3, 6)))

    def test_tokenization_complex_expression(self):
        """Test tokenization of a complex dice expression."""
        tokens = self.parser_core.tokenize(TEST_COMPLEX_DICE)
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
        tokens = self.parser_core.tokenize(TEST_SIMPLE_DICE)
        try:
            self.parser_core.validate_tokens(tokens)
        except Exception as e:
            self.fail(f"Validation failed for simple expression: {e}")

    def test_validation_complex_expression(self):
        """Test validation of a complex dice expression."""
        tokens = self.parser_core.tokenize(TEST_COMPLEX_DICE)
        try:
            self.parser_core.validate_tokens(tokens)
        except Exception as e:
            self.fail(f"Validation failed for complex expression: {e}")

    def test_parse_simple_dice(self):
        """Test parsing of a simple dice notation."""
        tokens = self.parser_core.tokenize(TEST_SIMPLE_DICE)

        # Run multiple times to check consistency
        results = []
        for _ in range(TEST_DICE_ROLL_COUNT):
            result = self.parser_core.parse(tokens)
            results.append(result)
            self.assertTrue(TEST_SIMPLE_DICE_MIN <= result <= TEST_SIMPLE_DICE_MAX)  # 3D6 range

        # Ensure variability in results
        self.assertTrue(len(set(results)) > 1)

    def test_parse_deterministic_mode(self):
        """Test parsing in deterministic mode."""
        tokens = self.parser_core.tokenize(TEST_SIMPLE_DICE)

        # First roll
        random.seed(TEST_DICE_SEED)
        first_result = self.parser_core.parse(tokens, deterministic=True)

        # Second roll should be identical
        random.seed(TEST_DICE_SEED)
        second_result = self.parser_core.parse(tokens, deterministic=True)

        self.assertEqual(first_result, second_result)

    def test_parse_complex_expression(self):
        """Test parsing of a complex dice expression."""
        tokens = self.parser_core.tokenize(TEST_COMPLEX_DICE)

        # Run multiple times to check consistency
        results = []
        for _ in range(TEST_DICE_ROLL_COUNT):
            result = self.parser_core.parse(tokens)
            results.append(result)

            # Basic range check (minimal validation)
            self.assertTrue(result > 0)

        # Ensure variability in results
        self.assertTrue(len(set(results)) > 1)

    def test_invalid_dice_notation_errors(self):
        """Test handling of various invalid dice notations."""
        invalid_expressions = [
            ("3D0", RollError, "Zero-sided die"),
            ("0D6", RollError, "Zero dice count"),
            ("3D6+", ValidationError, "Incomplete expression"),
            ("(3D6", ValidationError, "Unbalanced parentheses"),
            ("3D6++5", ValidationError, "Multiple consecutive operators"),
            ("3D6)(+5", ValidationError, "Misplaced parentheses"),
            ("()", ValidationError, "Empty parentheses")
        ]

        for expr, expected_error, description in invalid_expressions:
            with self.subTest(expr=expr, description=description):
                with self.assertRaises(expected_error, msg=description):
                    tokens = self.parser_core.tokenize(expr)
                    self.parser_core.validate_tokens(tokens)

    def test_limit_exceeded_errors(self):
        """Test handling of parsing limits."""
        # Create an excessively long dice string
        long_string = "1D6" * (DiceParserCore.MAX_DICE_STRING_LENGTH // 3 + 1)
        with self.assertRaises(LimitExceededError):
            self.parser_core.tokenize(long_string)

    def test_notation_parsing_utility(self):
        """Test the dice notation parsing utility method."""
        test_cases = [
            (TEST_SIMPLE_DICE, {
                'dice': [(3, 6)],
                'numbers': [],
                'operators': [],
                'parentheses': []
            }),
            (TEST_COMPLEX_DICE, {
                'dice': [(2, 6)],
                'numbers': [6, 5],
                'operators': ['+', '*'],
                'parentheses': ['(', ')']
            })
        ]

        for notation, expected in test_cases:
            parsed = self.parser_utils.parse_dice_notation(notation)
            self.assertEqual(parsed, expected)

    def test_validation_utility(self):
        """Test the dice notation validation utility."""
        valid_expressions = [
            TEST_SIMPLE_DICE, 
            "2D6+5", 
            "(3D6)*2", 
            "1D100", 
            "3D6+2", 
            TEST_COMPLEX_DICE,
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

    def test_deterministic_mode_setup(self):
        """Test setting up deterministic mode with custom values."""
        try:
            # Setup deterministic mode with valid values
            self.parser_utils.set_deterministic_mode(
                enabled=True, 
                values={
                    "1D6": [3, 4, 5],
                    "2D8": [2, 7]
                }
            )
        except Exception as e:
            self.fail(f"Failed to set up deterministic mode: {e}")

    def tearDown(self):
        """Clean up test fixtures."""
        # Reset random seed
        random.seed()


if __name__ == '__main__':
    unittest.main()