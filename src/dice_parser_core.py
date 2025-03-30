"""
Dice Parser Core Module for Call of Cthulhu RPG

This module provides the core parsing and tokenization logic for dice notation expressions 
commonly used in tabletop RPGs like Call of Cthulhu.

The module focuses on efficiently breaking down dice expressions into tokens
that can be evaluated according to standard RPG rules.

Author: Unknown
Version: 3.1
Last Updated: 2025-03-30
"""

import random
import operator
import re
from typing import List, Tuple, Union


class DiceParserCore:
    """
    A class for parsing and performing basic tokenization of dice notation expressions.

    This parser uses regex-based tokenization to efficiently handle dice expressions,
    breaking them down into components for further evaluation.
    """

    def __init__(self):
        """Initialize the dice parser with operator maps."""
        # Define operator mappings
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.floordiv  # Integer division for dice rolls
        }
        # For tracking deterministic values
        self._next_deterministic_value = 0

    def tokenize(self, dice_string):
        """
        Convert a dice string into tokens for processing using regex matching.

        Args:
            dice_string (str): A string in standard dice notation

        Returns:
            list: A list of tokens representing the dice expression

        Raises:
            ValueError: If the dice string contains invalid tokens
        """
        # Validate input to fail fast with better error messages
        if not dice_string:
            raise ValueError("Empty dice expression")

        # Remove all whitespace and convert to uppercase
        dice_string = dice_string.replace(' ', '').upper()

        # Initialize tokens list
        tokens = []

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

        for match in re.finditer(pattern, dice_string):
            # Check if there's a gap between matches (invalid character)
            if match.start() > position:
                invalid_char = dice_string[position]
                raise ValueError(f"Invalid character in dice string: '{invalid_char}'")

            # Extract the match groups
            groups = match.groups()

            # Determine token type based on which group matched
            if groups[0] is not None:  # Dice notation (e.g., "3D6")
                count = int(groups[0])
                sides = int(groups[1])

                # Validation for dice parameters
                if count <= 0:
                    raise ValueError(f"Dice count must be positive: {count}D{sides}")
                if sides <= 0:
                    raise ValueError(f"Dice sides must be positive: {count}D{sides}")

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
            invalid_char = dice_string[position]
            raise ValueError(f"Invalid character in dice string: '{invalid_char}'")

        # Validate balanced parentheses
        paren_count = 0
        for token_type, _ in tokens:
            if token_type == 'LPAREN':
                paren_count += 1
            elif token_type == 'RPAREN':
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Unbalanced parentheses: too many closing parentheses")

        if paren_count > 0:
            raise ValueError("Unbalanced parentheses: missing closing parentheses")

        return tokens

    def validate_tokens(self, tokens):
        """
        Validate a sequence of tokens to ensure they form a valid dice expression.

        Args:
            tokens (list): List of tokens to validate

        Raises:
            ValueError: If the token sequence is invalid
        """
        # Check for empty token list
        if not tokens:
            raise ValueError("Empty dice expression")

        # Track state during validation
        expect_value = True
        paren_level = 0
        last_token_type = None

        for i, (token_type, token_value) in enumerate(tokens):
            # Parenthesis handling
            if token_type == 'LPAREN':
                paren_level += 1
                if not expect_value:
                    raise ValueError(f"Unexpected opening parenthesis at position {i}")
                continue
            elif token_type == 'RPAREN':
                paren_level -= 1
                if paren_level < 0:
                    raise ValueError("Unbalanced parentheses: too many closing parentheses")
                if last_token_type == 'LPAREN':
                    raise ValueError("Empty parentheses are not allowed")
                expect_value = False
                continue

            # Check for alternate value and operator patterns
            if expect_value:
                # We expect a value (NUMBER, DICE, or LPAREN)
                if token_type not in ['NUMBER', 'DICE']:
                    raise ValueError(f"Expected a value at position {i}, got {token_type}")
                expect_value = False
            else:
                # We expect an operator
                if token_type != 'OPERATOR':
                    raise ValueError(f"Expected an operator at position {i}, got {token_type}")
                expect_value = True

            last_token_type = token_type

        # Final checks
        if paren_level > 0:
            raise ValueError("Unbalanced parentheses: missing closing parentheses")

        if expect_value:
            raise ValueError("Incomplete dice expression")

    def parse(self, tokens, deterministic=False):
        """
        Parse and evaluate a sequence of tokens.

        Args:
            tokens (list): Tokens from tokenize method
            deterministic (bool): Use deterministic mode if True

        Returns:
            int: Result of the dice expression
        """
        # Validate tokens first
        self.validate_tokens(tokens)

        def evaluate_sequence(token_seq):
            values = []
            operators_seq = []

            i = 0
            while i < len(token_seq):
                token_type, token_value = token_seq[i]

                if token_type == 'NUMBER':
                    values.append(token_value)
                elif token_type == 'DICE':
                    # Roll the dice
                    count, sides = token_value

                    if deterministic:
                        # Use deterministic values when specified
                        result = sum([(self._next_deterministic_value % sides) + 1 for _ in range(count)])
                        self._next_deterministic_value += 1
                    else:
                        # Use random rolls
                        result = sum(random.randint(1, sides) for _ in range(count))

                    values.append(result)
                elif token_type == 'OPERATOR':
                    operators_seq.append(token_value)
                elif token_type == 'LPAREN':
                    # Find matching parenthesis
                    paren_level = 1
                    j = i + 1

                    while j < len(token_seq) and paren_level > 0:
                        if token_seq[j][0] == 'LPAREN':
                            paren_level += 1
                        elif token_seq[j][0] == 'RPAREN':
                            paren_level -= 1
                        j += 1

                    if paren_level > 0:
                        raise ValueError("Mismatched parentheses")

                    # Evaluate sub-expression
                    sub_expr = token_seq[i+1:j-1]
                    values.append(evaluate_sequence(sub_expr))
                    i = j
                    continue

                i += 1

            # Validate expression
            if not values:
                raise ValueError("No values in expression")

            if len(values) != len(operators_seq) + 1:
                raise ValueError("Mismatched number of values and operators")

            # Calculate result
            result = values[0]
            for i, op in enumerate(operators_seq):
                result = self.operators[op](result, values[i+1])

            return result

        # Start with a deterministic seed to ensure reproducibility if needed
        if deterministic:
            self._next_deterministic_value = 0
            random.seed(42)  # Use a fixed seed for deterministic mode

        return evaluate_sequence(tokens)