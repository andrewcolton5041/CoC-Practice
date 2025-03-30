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
from src.constants import (
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
    # Class constants for use in tests
    MAX_DICE_STRING_LENGTH = MAX_DICE_STRING_LENGTH
    MAX_DICE_COUNT = MAX_DICE_COUNT
    MAX_DICE_SIDES = MAX_DICE_SIDES

    def __init__(self):
        """Initialize the dice parser with operator maps and deterministic random generator."""
        # Define operator mappings with their functions and precedence
        self.operators = {
            '+': (operator.add, 1),
            '-': (operator.sub, 1),
            '*': (operator.mul, 2),
            '/': (operator.floordiv, 2)  # Integer division for dice rolls
        }
        # Deterministic random number generator - initialized with a fixed seed
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

    def validate_tokens(self, tokens) -> bool:
        """
        Validate that a list of tokens represents a valid dice expression.

        Args:
            tokens (list): List of tokens to validate

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If tokens fail validation
        """
        # Check for empty token list
        if not tokens:
            raise ValidationError("Empty token list", error_type="empty_tokens")

        # Check for invalid token sequences and syntax errors

        # Track parentheses balance
        paren_count = 0

        # Track last token type for sequence validation
        last_token_type = None

        for i, (token_type, token_value) in enumerate(tokens):
            # Check parentheses balance
            if token_type == 'LPAREN':
                paren_count += 1
            elif token_type == 'RPAREN':
                paren_count -= 1
                if paren_count < 0:
                    raise ValidationError("Mismatched parentheses", tokens=tokens, error_type="unbalanced_parentheses")

            # Check for empty parentheses
            if (i > 0 and token_type == 'RPAREN' and 
                tokens[i-1][0] == 'LPAREN'):
                raise ValidationError("Empty parentheses", tokens=tokens, error_type="empty_parentheses")

            # Check for invalid token sequences
            if last_token_type == 'OPERATOR' and token_type == 'OPERATOR':
                raise ValidationError("Multiple consecutive operators", tokens=tokens, error_type="invalid_token_sequence")

            # Check for missing operands
            if i == len(tokens) - 1 and token_type == 'OPERATOR':
                raise ValidationError("Missing operand after operator", tokens=tokens, error_type="missing_operand")

            # Check for invalid placement of operators
            if i == 0 and token_type == 'OPERATOR':
                raise ValidationError("Expression cannot start with an operator", tokens=tokens, error_type="invalid_operator_placement")

            # Update last token type
            last_token_type = token_type

        # Check final parentheses balance
        if paren_count != 0:
            raise ValidationError("Unbalanced parentheses", tokens=tokens, error_type="unbalanced_parentheses")

        return True

    def parse(self, tokens, deterministic=False):
        """
        Parse tokens and evaluate the dice expression.

        Args:
            tokens (list): List of tokens to parse
            deterministic (bool): Whether to use deterministic mode

        Returns:
            int: Result of the dice expression
        """
        if not tokens:
            return 0

        # For deterministic mode, we need to reset the random number generator to the fixed seed
        if deterministic:
            # Reset the random state for deterministic mode to ensure consistent results
            self._det_rng = random.Random(42)

        # Simple case for a single dice token
        if len(tokens) == 1 and tokens[0][0] == 'DICE':
            count, sides = tokens[0][1]
            return self._roll_dice(count, sides, deterministic)

        # For more complex expressions, implement a proper evaluation algorithm
        # Using shunting yard algorithm to handle operator precedence
        output_queue = []
        operator_stack = []

        for token_type, token_value in tokens:
            if token_type in ('DICE', 'NUMBER'):
                if token_type == 'DICE':
                    count, sides = token_value
                    # Roll the dice according to deterministic flag
                    dice_result = self._roll_dice(count, sides, deterministic)
                    output_queue.append(dice_result)
                else:
                    output_queue.append(token_value)
            elif token_type == 'OPERATOR':
                # Process operators according to precedence
                while (operator_stack and operator_stack[-1] != '(' and
                       self.operators[token_value][1] <= self.operators[operator_stack[-1]][1]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token_value)
            elif token_type == 'LPAREN':
                operator_stack.append('(')
            elif token_type == 'RPAREN':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # Discard the left parenthesis

        # Pop any remaining operators
        while operator_stack:
            output_queue.append(operator_stack.pop())

        # Evaluate the result using a stack
        result_stack = []
        for item in output_queue:
            if isinstance(item, (int, float)):
                result_stack.append(item)
            else:  # It's an operator
                op_func = self.operators[item][0]
                if len(result_stack) < 2:
                    # This should not happen if validation passes
                    raise ValidationError(f"Not enough operands for operator {item}")
                b = result_stack.pop()
                a = result_stack.pop()
                result_stack.append(op_func(a, b))

        # The final result should be the only item on the stack
        if len(result_stack) != 1:
            raise ValidationError("Invalid expression - multiple results")

        return result_stack[0]

    def _roll_dice(self, count, sides, deterministic=False):
        """
        Roll dice with the given parameters.

        Args:
            count (int): Number of dice to roll
            sides (int): Number of sides on each die
            deterministic (bool): Whether to use deterministic mode

        Returns:
            int: Sum of all dice rolls
        """
        if deterministic:
            # Use the deterministic RNG with fixed seed
            return sum(self._det_rng.randint(1, sides) for _ in range(count))
        else:
            # Use regular random for normal operation
            return sum(random.randint(1, sides) for _ in range(count))