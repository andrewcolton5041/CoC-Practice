"""
Dice Parser Utility Module for Call of Cthulhu RPG

This module provides utility functions and deterministic mode handling
for dice notation expressions, supporting advanced testing and 
reproducible random number generation.

Author: Unknown
Version: 3.1
Last Updated: 2025-03-30
"""

import random


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
        self._deterministic_values = {}
        self._next_deterministic_value = 0

    def set_deterministic_mode(self, enabled=True, values=None):
        """
        Set the parser to use deterministic values instead of random ones.

        This is primarily useful for testing, where consistent results are needed.

        Args:
            enabled (bool): Whether to enable deterministic mode
            values (dict, optional): Dictionary mapping dice notation to fixed values
                e.g., {"1D6": [3], "2D8": [5, 7]}
        """
        self._deterministic_mode = enabled
        self._deterministic_values = values or {}
        self._next_deterministic_value = 0

    def get_deterministic_roll(self, sides, count=1):
        """
        Get a deterministic roll value for testing purposes.

        Args:
            sides (int): Number of sides on the die
            count (int): Number of dice to roll

        Returns:
            list: List of deterministic roll values
        """
        dice_key = f"{count}D{sides}"

        # If we have predetermined values for this dice notation, use those
        if dice_key in self._deterministic_values:
            values = self._deterministic_values[dice_key]
            # If there are fewer values than requested, cycle through them
            return [values[i % len(values)] for i in range(count)]

        # Otherwise, use a simple deterministic sequence based on sides
        return [(self._next_deterministic_value % sides) + 1 for _ in range(count)]

    def roll_random_dice(self, sides, count=1, seed=None):
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

    def validate_dice_notation(self, dice_string):
        """
        Validate a dice notation string.

        Args:
            dice_string (str): Dice notation to validate 
                (e.g., "3D6", "1D20+5", "(2D6+6)*5")

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            from src.dice_parser_core import DiceParserCore
            parser_core = DiceParserCore()
            tokens = parser_core.tokenize(dice_string)
            parser_core.validate_tokens(tokens)
            return True
        except ValueError:
            return False

    def parse_dice_notation(self, dice_string):
        """
        Parse a dice notation string into its components.

        Args:
            dice_string (str): Dice notation to parse

        Returns:
            dict: Dictionary with parsed components
                Keys may include: 'dice', 'operators', 'numbers', 'parentheses'
        """
        from src.dice_parser_core import DiceParserCore
        parser_core = DiceParserCore()

        # Tokenize the dice string
        tokens = parser_core.tokenize(dice_string)

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