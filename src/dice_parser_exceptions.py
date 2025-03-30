# We'll format the updated content and write it to a downloadable file

updated_exceptions_content = """
\"\"\"
Custom Exceptions for Dice Parsing in Call of Cthulhu RPG

This module defines specialized exceptions to provide more detailed
error handling for dice notation parsing and evaluation.

Author: Unknown
Version: 4.1
Last Updated: 2025-03-30
\"\"\"

from typing import Optional, List, Union, Any, Dict, Tuple


class DiceParserError(Exception):
    \"\"\"Base exception for all dice parser-related errors.\"\"\"

    def __init__(self, message: str, dice_string: Optional[str] = None,
                 context: Optional[Dict[str, Any]] = None):
        \"\"\"
        Initialize the base dice parser error.

        Args:
            message (str): Detailed error message.
            dice_string (Optional[str]): The original dice string that caused the error.
            context (Optional[Dict[str, Any]]): Additional context.
        \"\"\"
        super().__init__(message)
        self.dice_string = dice_string
        self.context = context or {}


class TokenizationError(DiceParserError):
    \"\"\"Raised when tokenizing a dice expression fails.\"\"\"

    def __init__(self, message: str, dice_string: Optional[str] = None,
                 position: Optional[int] = None, problematic_token: Optional[str] = None):
        \"\"\"
        Initialize the tokenization error.

        Args:
            message (str): Error message.
            dice_string (Optional[str]): Dice string being parsed.
            position (Optional[int]): Position of error.
            problematic_token (Optional[str]): Token causing the error.
        \"\"\"
        context = {
            'position': position,
            'problematic_token': problematic_token
        }
        super().__init__(message, dice_string, context)
        self.position = position
        self.problematic_token = problematic_token


class ValidationError(DiceParserError):
    \"\"\"Raised when a dice expression fails semantic validation.\"\"\"

    ERROR_TYPES = [
        'unbalanced_parentheses',
        'invalid_token_sequence',
        'missing_operand',
        'invalid_operator_placement',
        'empty_parentheses',
        'invalid_dice_token',
        'invalid_dice_values',
        'missing_tokens'
    ]

    def __init__(self, message: str, dice_string: Optional[str] = None,
                 tokens: Optional[List[Tuple[str, Any]]] = None, error_type: Optional[str] = None):
        \"\"\"
        Initialize the validation error.

        Args:
            message (str): Error message.
            dice_string (Optional[str]): Dice string being validated.
            tokens (Optional[List[Tuple[str, Any]]]): Tokens causing error.
            error_type (Optional[str]): Type of validation error.
        \"\"\"
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
    \"\"\"Raised during errors with rolling dice.\"\"\"

    def __init__(self, message: str, dice_notation: Optional[str] = None,
                 sides: Optional[int] = None, count: Optional[int] = None,
                 error_type: Optional[str] = None):
        \"\"\"
        Initialize the roll error.

        Args:
            message (str): Error message.
            dice_notation (Optional[str]): Dice notation being evaluated.
            sides (Optional[int]): Number of dice sides.
            count (Optional[int]): Number of dice rolled.
            error_type (Optional[str]): Specific roll error type.
        \"\"\"
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
    \"\"\"Raised when parsing limits are exceeded.\"\"\"

    def __init__(self, message: str, dice_string: Optional[str] = None,
                 max_length: Optional[int] = None, max_dice: Optional[int] = None,
                 max_sides: Optional[int] = None):
        \"\"\"
        Initialize the limit exceeded error.

        Args:
            message (str): Error message.
            dice_string (Optional[str]): Original dice string.
            max_length (Optional[int]): Max allowed dice string length.
            max_dice (Optional[int]): Max dice allowed.
            max_sides (Optional[int]): Max sides per die.
        \"\"\"
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
    \"\"\"Raised when there are issues with deterministic mode configuration.\"\"\"

    def __init__(self, message: str,
                 values: Optional[Union[Dict, list]] = None,
                 error_type: Optional[str] = None):
        \"\"\"
        Initialize the deterministic mode error.

        Args:
            message (str): Error message.
            values (Optional[Union[Dict, list]]): Problematic deterministic values.
            error_type (Optional[str]): Specific deterministic error type.
        \"\"\"
        context = {
            'values': values,
            'error_type': error_type
        }
        super().__init__(message, context=context)
        self.values = values
        self.error_type = error_type
"""

# Write the updated content to a file
from pathlib import Path

output_path = Path("/mnt/data/dice_parser_exceptions_fixed.py")
output_path.write_text(updated_exceptions_content)

output_path.name
