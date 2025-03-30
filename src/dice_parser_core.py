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


class DiceParserCore:
    """
    A class for parsing and performing tokenization of dice notation expressions.

    This parser uses regex-based tokenization and a stack-based parsing approach 
    to efficiently handle dice expressions.
    """

    # Configuration constants for parsing limits
    MAX_DICE_STRING_LENGTH = 1000  # Maximum allowed length of dice string
    MAX_DICE_COUNT = 100  # Maximum number of dice in a single roll
    MAX_DICE_SIDES = 1000  # Maximum number of sides on a die

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

        if len(dice_string) > self.MAX_DICE_STRING_LENGTH:
            raise LimitExceededError(
                f"Dice notation exceeds maximum length of {self.MAX_DICE_STRING_LENGTH}",
                dice_string,
                max_length=self.MAX_DICE_STRING_LENGTH
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
                    if count <= 0 or count > self.MAX_DICE_COUNT:
                        raise RollError(
                            f"Dice count must be between 1 and {self.MAX_DICE_COUNT}",
                            dice_string,
                            sides=sides,
                            count=count,
                            error_type='invalid_dice_count'
                        )

                    if sides <= 0 or sides > self.MAX_DICE_SIDES:
                        raise RollError(
                            f"Dice sides must be between 1 and {self.MAX_DICE_SIDES}",
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

    def parse(self, tokens: List[Tuple[str, Any]], deterministic: bool = False) -> int:
        """
        Parse and evaluate a sequence of tokens using a stack-based approach.

        Args:
            tokens (list): Tokens from tokenize method
            deterministic (bool): Use deterministic mode if True

        Returns:
            int: Result of the dice expression
        """
        # Validate tokens first
        self.validate_tokens(tokens)

        # Reset deterministic random number generator if in deterministic mode
        if deterministic:
            self._det_rng = random.Random(42)

        # Prepare stacks for parsing
        value_stack = []
        operator_stack = []

        # Helper function to apply an operator
        def apply_operator():
            if len(value_stack) < 2 or not operator_stack:
                raise ValidationError("Invalid expression: insufficient values for operator")

            right = value_stack.pop()
            left = value_stack.pop()
            op_func, _ = self.operators[operator_stack.pop()]
            value_stack.append(op_func(left, right))

        # Process tokens
        for token_type, token_value in tokens:
            if token_type == 'NUMBER':
                value_stack.append(token_value)

            elif token_type == 'DICE':
                # Roll dice
                count, sides = token_value

                # Use deterministic or random roll
                if deterministic:
                    # Deterministic roll
                    result = sum(self._deterministic_roll(sides) for _ in range(count))
                else:
                    # Random roll
                    result = sum(random.randint(1, sides) for _ in range(count))

                value_stack.append(result)

            elif token_type == 'OPERATOR':
                # Handle operator precedence
                while (operator_stack and 
                       operator_stack[-1] != '(' and 
                       self.operators[str(operator_stack[-1])][1] >= self.operators[str(token_value)][1]):
                    apply_operator()
                operator_stack.append(token_value)

            elif token_type == 'LPAREN':
                operator_stack.append(token_value)

            elif token_type == 'RPAREN':
                # Evaluate everything inside the parentheses
                while operator_stack and operator_stack[-1] != '(':
                    apply_operator()

                # Remove the left parenthesis
                if not operator_stack or operator_stack[-1] != '(':
                    raise ValidationError("Mismatched parentheses")
                operator_stack.pop()

        # Apply any remaining operators
        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValidationError("Unbalanced parentheses")
            apply_operator()

        # Final result should be the only item left in value stack
        if len(value_stack) != 1:
            raise ValidationError("Invalid expression: too many values")

        return value_stack[0]

    def validate_tokens(self, tokens: List[Tuple[str, Any]]) -> None:
        """
        Validate a sequence of tokens to ensure they form a valid dice expression.

        Args:
            tokens (list): List of tokens to validate

        Raises:
            ValidationError: If the token sequence is invalid
        """
        # Check for empty token list
        if not tokens:
            raise ValidationError(
                "Empty dice expression", 
                error_type='missing_tokens'
            )

        # Special case: Immediately reject if tokens are only parentheses
        if all(token_type in ['LPAREN', 'RPAREN'] for token_type, _ in tokens):
            raise ValidationError(
                "Empty or unbalanced parentheses",
                tokens=tokens,
                error_type='empty_parentheses'
            )

        # Track state during validation
        expect_value = True
        paren_level = 0
        last_token_type = None

        for i, (token_type, token_value) in enumerate(tokens):
            # Parenthesis handling
            if token_type == 'LPAREN':
                paren_level += 1
                if not expect_value:
                    raise ValidationError(
                        f"Unexpected opening parenthesis at position {i}",
                        tokens=tokens,
                        error_type='unbalanced_parentheses'
                    )
                expect_value = True
                continue
            elif token_type == 'RPAREN':
                paren_level -= 1
                if paren_level < 0:
                    raise ValidationError(
                        "Unbalanced parentheses: too many closing parentheses",
                        tokens=tokens,
                        error_type='unbalanced_parentheses'
                    )
                if last_token_type == 'LPAREN':
                    raise ValidationError(
                        "Empty parentheses are not allowed",
                        tokens=tokens,
                        error_type='empty_parentheses'
                    )
                expect_value = False
                continue

            # Check for alternate value and operator patterns
            if expect_value:
                # We expect a value (NUMBER, DICE, or LPAREN)
                if token_type not in ['NUMBER', 'DICE']:
                    raise ValidationError(
                        f"Expected a value at position {i}, got {token_type}",
                        tokens=tokens,
                        error_type='missing_operand'
                    )

                # Additional validation for DICE token
                if token_type == 'DICE':
                    if not isinstance(token_value, tuple) or len(token_value) != 2:
                        raise ValidationError(
                            f"Invalid DICE token structure at position {i}",
                            tokens=tokens,
                            error_type='invalid_dice_token'
                        )

                    count, sides = token_value
                    if not isinstance(count, int) or not isinstance(sides, int):
                        raise ValidationError(
                            f"DICE token must have integer values at position {i}",
                            tokens=tokens,
                            error_type='invalid_dice_values'
                        )

                expect_value = False
            else:
                # We expect an operator
                if token_type != 'OPERATOR':
                    raise ValidationError(
                        f"Expected an operator at position {i}, got {token_type}",
                        tokens=tokens,
                        error_type='invalid_operator_placement'
                    )
                expect_value = True

            last_token_type = token_type

        # Final checks
        if paren_level > 0:
            raise ValidationError(
                "Unbalanced parentheses: missing closing parentheses",
                tokens=tokens,
                error_type='unbalanced_parentheses'
            )

        if expect_value:
            raise ValidationError(
                "Incomplete dice expression",
                tokens=tokens,
                error_type='missing_operand'
            )