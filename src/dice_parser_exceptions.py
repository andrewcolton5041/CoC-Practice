"""
Custom Exceptions for Dice Parsing in Call of Cthulhu RPG

This module defines specialized exceptions to provide more detailed
error handling for dice notation parsing and evaluation.

Author: Unknown
Version: 3.1
Last Updated: 2025-03-30
"""


class DiceParserError(Exception):
    """
    Base exception for all dice parser-related errors.

    Serves as a common base for more specific dice parsing exceptions.
    """
    pass


class TokenizationError(DiceParserError):
    """
    Raised when there are issues with tokenizing a dice expression.

    This exception occurs during the initial breakdown of a dice notation
    into individual tokens, such as encountering invalid characters
    or malformed expressions.
    """
    def __init__(self, message, dice_string=None, position=None):
        """
        Initialize the tokenization error.

        Args:
            message (str): Detailed error message
            dice_string (str, optional): The original dice string that caused the error
            position (int, optional): The position in the string where the error occurred
        """
        super().__init__(message)
        self.dice_string = dice_string
        self.position = position


class ValidationError(DiceParserError):
    """
    Raised when a dice expression fails validation.

    This exception is raised when the token sequence is semantically 
    incorrect, such as having mismatched parentheses or invalid 
    token sequences.
    """
    def __init__(self, message, tokens=None):
        """
        Initialize the validation error.

        Args:
            message (str): Detailed error message
            tokens (list, optional): The tokens that failed validation
        """
        super().__init__(message)
        self.tokens = tokens


class RollError(DiceParserError):
    """
    Raised when there are issues with rolling dice.

    This exception covers problems during the actual dice rolling process,
    such as invalid dice parameters or roll generation failures.
    """
    def __init__(self, message, dice_notation=None, sides=None, count=None):
        """
        Initialize the roll error.

        Args:
            message (str): Detailed error message
            dice_notation (str, optional): The dice notation that caused the error
            sides (int, optional): Number of sides on the die
            count (int, optional): Number of dice to roll
        """
        super().__init__(message)
        self.dice_notation = dice_notation
        self.sides = sides
        self.count = count


class DeterministicModeError(DiceParserError):
    """
    Raised when there are issues with deterministic mode.

    This exception occurs when there are problems with predefined
    deterministic roll values or mode configuration.
    """
    def __init__(self, message, values=None):
        """
        Initialize the deterministic mode error.

        Args:
            message (str): Detailed error message
            values (dict, optional): The problematic deterministic values
        """
        super().__init__(message)
        self.values = values