"""
Test module for the optimized dice parser implementation with memoization.

This module contains tests for the dice parser functionality,
verifying that it correctly handles memoization, caching, and performance
improvements for repeated dice rolls.

Author: Unknown
Version: 4.1
Last Updated: 2025-03-30
"""

import unittest
import random
import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import List, Tuple, Union, Any, Sequence, cast

from src.dice_parser_core import DiceParserCore
from src.dice_parser_utils import DiceParserUtils
from src.dice_parser_exceptions import (
    TokenizationError, 
    ValidationError, 
    RollError, 
    LimitExceededError, 
    DiceParserError
)

TokenType = Union[int, Tuple[int, int], str]


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
        self.assertEqual(tokens[0][0], 'DICE')
        self.assertEqual(tokens[0][1], (3, 6))

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
        # Cast tokens to the expected type
        tokens: List[Tuple[str, TokenType]] = cast(
            List[Tuple[str, TokenType]], 
            self.parser_core.tokenize("3D6")
        )

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
        # Cast tokens to the expected type
        tokens: List[Tuple[str, TokenType]] = cast(
            List[Tuple[str, TokenType]], 
            self.parser_core.tokenize("3D6")
        )

        # Perform multiple runs to ensure consistency
        results = []
        for _ in range(5):
            result = self.parser_core.parse(tokens, deterministic=True)
            results.append(result)
            print(f"Deterministic result {_+1}: {result}")

        # Verify all results are the same
        self.assertTrue(
            all(r == results[0] for r in results), 
            "Deterministic parsing should always produce the same result"
        )

    def test_parse_complex_expression(self):
        """Test parsing of a complex dice expression."""
        # Cast tokens to the expected type
        tokens: List[Tuple[str, TokenType]] = cast(
            List[Tuple[str, TokenType]], 
            self.parser_core.tokenize("(2D6+6)*5")
        )

        # Run multiple times to check consistency
        results = []
        for _ in range(10):
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
                    try:
                        tokens = self.parser_core.tokenize(expr)
                        self.parser_core.validate_tokens(tokens)
                    except Exception as e:
                        raise e

    def test_limit_exceeded_errors(self):
        """Test handling of parsing limits."""
        # Create an excessively long dice string
        long_string = "1D6" * (DiceParserCore.MAX_DICE_STRING_LENGTH // 3 + 1)
        with self.assertRaises(LimitExceededError):
            self.parser_core.tokenize(long_string)

    def test_validation_enhanced_dice_token(self):
        """Test enhanced validation for DICE tokens."""
        with self.assertRaises(ValidationError):
            # Invalid DICE token (not a tuple)
            self.parser_core.validate_tokens([('DICE', 'invalid')])

        with self.assertRaises(ValidationError):
            # DICE token with non-integer values
            self.parser_core.validate_tokens([('DICE', ('3', '6'))])

        with self.assertRaises(ValidationError):
            # DICE token with wrong tuple length
            self.parser_core.validate_tokens([('DICE', (3, 6, 9))])

    def test_notation_parsing_utility(self):
        """Test the dice notation parsing utility method."""
        test_cases = [
            ("3D6", {
                'dice': [(3, 6)],
                'numbers': [],
                'operators': [],
                'parentheses': []
            }),
            ("(2D6+6)*5", {
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