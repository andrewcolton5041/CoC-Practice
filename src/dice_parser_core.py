"""
Dice Parser Core Module for Call of Cthulhu RPG

This module provides the core parsing and tokenization logic for dice notation expressions 
commonly used in tabletop RPGs like Call of Cthulhu.

The module focuses on efficiently breaking down dice expressions into tokens
that can be evaluated according to standard RPG rules.

Author: Unknown
Version: 4.1
Last Updated: 2025-03-30
"""

import random
import operator
import re
from typing import List, Tuple, Union, Optional, Any

from src.dice_parser_exceptions import (
    TokenizationError, 
    ValidationError, 
    RollError, 
    LimitExceededError
)
from constants import (
    MAX_DICE_STRING_LENGTH,
    MAX_DICE_COUNT,
    MAX_DICE_SIDES
)


class DiceParserCore:
    """
    A class for parsing and performing tokenization of dice notation expressions.

    This parser uses regex-based tokenization and a stack-based parsing approach 
    to efficiently handle dice expressions.
    """

    def __init__(self):
        """Initialize the dice parser with operator maps and deterministic random generator."""
        # Define operator mappings with their functions and precedence
        self.operators = {
            '+': (operator.add, 1),
            '-': (operator.sub, 1),
            '*': (operator.mul, 2),
            '/': (operator.floordiv, 2)  # Integer division for dice rolls
        }
        # Deterministic random number generator
        self._det_rng = random.Random(42)  # Fixed seed for deterministic mode

    def _deterministic_roll(self, sides: int) -> int:
        """
        Generate a deterministic roll for a die with given number of sides.

        Args:
            sides (int): Number of sides on the die

        Returns:
            int: A deterministic roll value
        """
        return self._det_rng.randint(1, sides)

    def tokenize(self, dice_string: str) -> List[Tuple[str, Union[int, Tuple[int, int], str]]]:
        """
        Convert a dice string into tokens for processing using regex matching.

        Args:
            dice_string (str): A string in standard dice notation

        Returns:
            list: A list of tokens representing the dice expression

        Raises:
            LimitExceededError: If dice string exceeds maximum length
            TokenizationError: For invalid tokens or characters
        """
        # Validate input length
        if not dice_string:
            raise TokenizationError("Empty dice expression")

        if len(dice_string) > MAX_DICE_STRING_LENGTH:
            raise LimitExceededError(
                f"Dice notation exceeds maximum length of {MAX_DICE_STRING_LENGTH}",
                dice_string,
                max_length=MAX_DICE_STRING_LENGTH
            )

        # Remove all whitespace and convert to uppercase
        dice_string = dice_string.replace(' ', '').upper()

        # Initialize tokens list
        tokens: List[Tuple[str, Union[int, Tuple[int, int], str]]] = []

        # Define regex patterns for different token types
        dice_pattern = r'(\d+)D(\d+)'  # For dice notation like 3D6
        number_pattern = r'(\d+)'      # For standalone numbers
        operator_pattern = r'([+\-*/])' # For operators
        lparen_pattern = r'(\()'       # For left parenthesis
        rparen_pattern = r'(\))'       # For right parenthesis

        # Combined pattern for tokenization
        pattern = f"{dice_pattern}|{number_pattern}|{operator_pattern}|{lparen_pattern}|{rparen_pattern}"

        # Process the string using regex
        position = 0

        try:
            for match in re.finditer(pattern, dice_string):
                # Check if there's a gap between matches (invalid character)
                if match.start() > position:
                    invalid_char = dice_string[position:match.start()]
                    raise TokenizationError(
                        f"Invalid character(s) in dice string",
                        dice_string,
                        position=position,
                        problematic_token=invalid_char
                    )

                # Extract the match groups
                groups = match.groups()

                # Determine token type based on which group matched
                if groups[0] is not None:  # Dice notation (e.g., "3D6")
                    count = int(groups[0])
                    sides = int(groups[1])

                    # Validation for dice parameters
                    if count <= 0 or count > MAX_DICE_COUNT:
                        raise RollError(
                            f"Dice count must be between 1 and {MAX_DICE_COUNT}",
                            dice_string,
                            sides=sides,
                            count=count,
                            error_type='invalid_dice_count'
                        )

                    if sides <= 0 or sides > MAX_DICE_SIDES:
                        raise RollError(
                            f"Dice sides must be between 1 and {MAX_DICE_SIDES}",
                            dice_string,
                            sides=sides,
                            count=count,
                            error_type='invalid_dice_sides'
                        )

                    tokens.append(('DICE', (count, sides)))
                elif groups[2] is not None:  # Standalone number
                    tokens.append(('NUMBER', int(groups[2])))
                elif groups[3] is not None:  # Operator
                    tokens.append(('OPERATOR', groups[3]))
                elif groups[4] is not None:  # Left parenthesis
                    tokens.append(('LPAREN', '('))
                elif groups[5] is not None:  # Right parenthesis
                    tokens.append(('RPAREN', ')'))

                position = match.end()

            # Check if we've processed the entire string
            if position < len(dice_string):
                raise TokenizationError(
                    "Unexpected characters at end of dice notation",
                    dice_string,
                    position=position,
                    problematic_token=dice_string[position:]
                )

            return tokens

        except Exception as e:
            # Wrap any unexpected errors with more context
            if isinstance(e, (TokenizationError, RollError, LimitExceededError)):
                raise
            raise TokenizationError(
                f"Unexpected error during tokenization: {str(e)}",
                dice_string
            ) from e
