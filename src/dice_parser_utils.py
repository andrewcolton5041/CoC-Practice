"""
Dice Parser Utility Module for Call of Cthulhu RPG

This module provides utility functions and deterministic mode handling
for dice notation expressions, supporting advanced testing and 
reproducible random number generation.

Author: Unknown
Version: 4.0
Last Updated: 2025-03-30
"""

import random
import re
from typing import Dict, Union, Optional, List, Tuple

from src.dice_parser_exceptions import (
    DeterministicModeError, 
    TokenizationError, 
    ValidationError
)
from src.dice_parser_core import DiceParserCore


class DiceParserUtils:
    """
    A utility class for advanced dice parsing features.

    Provides deterministic mode for testing and reproducible random generation,
    along with additional helper methods for dice rolling and manipulation.
    """

    def __init__(self):
        """Initialize the dice parser utilities."""
        # For deterministic mode
        self._deterministic_mode = False
        self._deterministic_values: Dict[str, List[int]] = {}
        self._next_deterministic_value = 0
        # Create a parser core for parsing support
        self._parser_core = DiceParserCore()

    def set_deterministic_mode(self, 
                                enabled: bool = True, 
                                values: Optional[Dict[str, List[int]]] = None) -> None:
        """
        Set the parser to use deterministic values instead of random ones.

        This is primarily useful for testing, where consistent results are needed.

        Args:
            enabled (bool): Whether to enable deterministic mode
            values (dict, optional): Dictionary mapping dice notation to fixed values
                e.g., {"1D6": [3], "2D8": [5, 7]}

        Raises:
            DeterministicModeError: If provided values are invalid
        """
        # Validate input values if provided
        if values is not None:
            for notation, roll_values in values.items():
                # Validate notation
                try:
                    tokens = self._parser_core.tokenize(notation)
                    self._parser_core.validate_tokens(tokens)
                except (TokenizationError, ValidationError) as e:
                    raise DeterministicModeError(
                        f"Invalid dice notation in deterministic values: {notation}",
                        values=values,
                        error_type='invalid_notation'
                    ) from e

                # Validate roll values
                if not all(isinstance(v, int) for v in roll_values):
                    raise DeterministicModeError(
                        "Deterministic values must be integers",
                        values=values,
                        error_type='invalid_value_type'
                    )

        # Set deterministic mode
        self._deterministic_mode = enabled
        self._deterministic_values = values or {}
        self._next_deterministic_value = 0

    def validate_dice_notation(self, dice_string: str) -> bool:
        """
        Validate a dice notation string with comprehensive checks.

        Args:
            dice_string (str): Dice notation to validate 
                (e.g., "3D6", "1D20+5", "(2D6+6)*5")

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Remove all whitespace and handle preprocessing for complex cases
            dice_string = dice_string.replace(' ', '')

            # Reject entirely empty or whitespace-only strings
            if not dice_string:
                return False

            # Comprehensive regex-based validation
            validation_patterns = [
                # Reject strings with consecutive operators
                r'[+\-*/]{2,}',

                # Reject strings starting or ending with an operator
                r'^[+\-*/]|[+\-*/]$',

                # Reject strings with empty or nested problematic parentheses
                r'\(\)|\([+\-*/]*\)|\([+\-*/]*\([+\-*/]*\)[+\-*/]*\)',

                # Reject dice notations with zero or negative parameters
                r'0D|D0|(\d+)D(0+)',

                # Reject invalid parentheses combinations
                r'\)[\dD(]|\d\(|D\('
            ]

            for pattern in validation_patterns:
                if re.search(pattern, dice_string):
                    return False

            # Attempt to tokenize and validate
            try:
                tokens = self._parser_core.tokenize(dice_string)
                self._parser_core.validate_tokens(tokens)
                return True
            except Exception:
                return False

        except Exception:
            return False

    def get_deterministic_roll(self, sides: int, count: int = 1) -> List[int]:
        """
        Get a deterministic roll value for testing purposes.

        Args:
            sides (int): Number of sides on the die
            count (int): Number of dice to roll

        Returns:
            list: List of deterministic roll values

        Raises:
            DeterministicModeError: If deterministic mode is not set up correctly
        """
        if not self._deterministic_mode:
            raise DeterministicModeError(
                "Deterministic mode is not enabled",
                error_type='mode_not_enabled'
            )

        dice_key = f"{count}D{sides}"

        # If we have predetermined values for this dice notation, use those
        if dice_key in self._deterministic_values:
            values = self._deterministic_values[dice_key]
            # If there are fewer values than requested, cycle through them
            return [values[i % len(values)] for i in range(count)]

        # Otherwise, use a simple deterministic sequence based on sides
        return [(self._next_deterministic_value % sides) + 1 for _ in range(count)]

    def roll_random_dice(self, 
                          sides: int, 
                          count: int = 1, 
                          seed: Optional[int] = None) -> List[int]:
        """
        Roll random dice with optional seeding for reproducibility.

        Args:
            sides (int): Number of sides on the die
            count (int): Number of dice to roll
            seed (int, optional): Seed for the random number generator

        Returns:
            list: List of random roll values
        """
        # Store the current random state
        state = random.getstate()

        try:
            # Set seed if provided
            if seed is not None:
                random.seed(seed)

            # Generate random rolls
            rolls = [random.randint(1, sides) for _ in range(count)]

            return rolls
        finally:
            # Restore the previous random state
            random.setstate(state)

    def parse_dice_notation(self, dice_string: str) -> Dict[str, Union[List[int], List[str], List[Tuple[int, int]]]]:
        """
        Parse a dice notation string into its components.

        Args:
            dice_string (str): Dice notation to parse

        Returns:
            dict: Dictionary with parsed components
                Keys include: 'dice', 'numbers', 'operators', 'parentheses'

        Raises:
            TokenizationError: If the dice string cannot be tokenized
            ValidationError: If the dice string is not valid
        """
        try:
            # Tokenize the dice string
            tokens = self._parser_core.tokenize(dice_string)

            # Organize tokens into categories
            parsed_components = {
                'dice': [],
                'numbers': [],
                'operators': [],
                'parentheses': []
            }

            for token_type, token_value in tokens:
                if token_type == 'DICE':
                    parsed_components['dice'].append(token_value)
                elif token_type == 'NUMBER':
                    parsed_components['numbers'].append(token_value)
                elif token_type == 'OPERATOR':
                    parsed_components['operators'].append(token_value)
                elif token_type in ['LPAREN', 'RPAREN']:
                    parsed_components['parentheses'].append(token_value)

            return parsed_components

        except (TokenizationError, ValidationError) as e:
            # Re-raise with additional context if needed
            raise e