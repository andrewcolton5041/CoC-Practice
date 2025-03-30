"""
Custom Exceptions for Dice Parsing in Call of Cthulhu RPG

This module defines specialized exceptions to provide more detailed
error handling for dice notation parsing and evaluation.

Exceptions are designed to give precise information about parsing errors,
helping developers and users understand exactly what went wrong.

Author: Unknown
Version: 4.0
Last Updated: 2025-03-30
"""

from typing import Optional, List, Union


class DiceParserError(Exception):
    """
    Base exception for all dice parser-related errors.

    Serves as a common base for more specific dice parsing exceptions
    with enhanced error reporting capabilities.
    """
    def __init__(self, 
                 message: str, 
                 dice_string: Optional[str] = None,
                 context: Optional[dict] = None):
        """
        Initialize the base dice parser error.

        Args:
            message (str): Detailed error message
            dice_string (str, optional): The original dice notation that caused the error
            context (dict, optional): Additional context about the error
        """
        super().__init__(message)
        self.dice_string = dice_string
        self.context = context or {}


class TokenizationError(DiceParserError):
    """
    Raised when there are issues with tokenizing a dice expression.

    This exception occurs during the initial breakdown of a dice notation
    into individual tokens, such as encountering invalid characters
    or malformed expressions.
    """
    def __init__(self, 
                 message: str, 
                 dice_string: Optional[str] = None, 
                 position: Optional[int] = None,
                 problematic_token: Optional[str] = None):
        """
        Initialize the tokenization error.

        Args:
            message (str): Detailed error message
            dice_string (str, optional): The original dice string that caused the error
            position (int, optional): The position in the string where the error occurred
            problematic_token (str, optional): The specific token causing the error
        """
        context = {
            'position': position,
            'problematic_token': problematic_token
        }
        super().__init__(message, dice_string, context)
        self.position = position
        self.problematic_token = problematic_token


class ValidationError(DiceParserError):
    """
    Raised when a dice expression fails validation.

    This exception is raised when the token sequence is semantically 
    incorrect, such as having mismatched parentheses or invalid 
    token sequences.
    """
    ERROR_TYPES = [
        'unbalanced_parentheses',
        'invalid_token_sequence',
        'missing_operand',
        'invalid_operator_placement',
        'empty_parentheses'
    ]

    def __init__(self, 
                 message: str, 
                 dice_string: Optional[str] = None,
                 tokens: Optional[List[tuple]] = None,
                 error_type: Optional[str] = None):
        """
        Initialize the validation error.

        Args:
            message (str): Detailed error message
            dice_string (str, optional): The original dice string
            tokens (list, optional): The tokens that failed validation
            error_type (str, optional): Specific type of validation error
        """
        # Validate error type
        if error_type and error_type not in self.ERROR_TYPES:
            raise ValueError(f"Invalid error type. Must be one of {self.ERROR_TYPES}")

        context = {
            'tokens': tokens,
            'error_type': error_type
        }
        super().__init__(message, dice_string, context)
        self.tokens = tokens or []
        self.error_type = error_type


class RollError(DiceParserError):
    """
    Raised when there are issues with rolling dice.

    This exception covers problems during the actual dice rolling process,
    such as invalid dice parameters or roll generation failures.
    """
    def __init__(self, 
                 message: str, 
                 dice_notation: Optional[str] = None, 
                 sides: Optional[int] = None, 
                 count: Optional[int] = None,
                 error_type: Optional[str] = None):
        """
        Initialize the roll error.

        Args:
            message (str): Detailed error message
            dice_notation (str, optional): The dice notation that caused the error
            sides (int, optional): Number of sides on the die
            count (int, optional): Number of dice to roll
            error_type (str, optional): Specific type of roll error
        """
        context = {
            'sides': sides,
            'count': count,
            'error_type': error_type
        }
        super().__init__(message, dice_notation, context)
        self.dice_notation = dice_notation
        self.sides = sides
        self.count = count
        self.error_type = error_type


class LimitExceededError(DiceParserError):
    """
    Raised when parsing limits are exceeded.

    This exception occurs when dice parameters or expression complexity
    goes beyond predefined limits to prevent computational or memory issues.
    """
    def __init__(self, 
                 message: str, 
                 dice_string: Optional[str] = None,
                 max_length: Optional[int] = None,
                 max_dice: Optional[int] = None, 
                 max_sides: Optional[int] = None):
        """
        Initialize the limit exceeded error.

        Args:
            message (str): Detailed error message
            dice_string (str, optional): The original dice string
            max_length (int, optional): Maximum allowed length of dice string
            max_dice (int, optional): Maximum number of dice allowed
            max_sides (int, optional): Maximum number of sides allowed per die
        """
        context = {
            'max_length': max_length,
            'max_dice': max_dice,
            'max_sides': max_sides
        }
        super().__init__(message, dice_string, context)
        self.max_length = max_length
        self.max_dice = max_dice
        self.max_sides = max_sides


class DeterministicModeError(DiceParserError):
    """
    Raised when there are issues with deterministic mode configuration.

    This exception occurs when there are problems with predefined
    deterministic roll values or mode configuration.
    """
    def __init__(self, 
                 message: str, 
                 values: Optional[Union[dict, list]] = None,
                 error_type: Optional[str] = None):
        """
        Initialize the deterministic mode error.

        Args:
            message (str): Detailed error message
            values (dict or list, optional): The problematic deterministic values
            error_type (str, optional): Specific type of deterministic mode error
        """
        context = {
            'values': values,
            'error_type': error_type
        }
        super().__init__(message, context=context)
        self.values = values
        self.error_type = error_type