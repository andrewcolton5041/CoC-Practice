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
        last_token_type = None

        for i, (token_type, token_value) in enumerate(tokens):
            # Check for alternate value and operator patterns
            if expect_value:
                # We expect a value (NUMBER, DICE, or LPAREN)
                if token_type not in ['NUMBER', 'DICE', 'LPAREN']:
                    raise ValueError(f"Expected a value at position {i}, got {token_type}")
                expect_value = False
            else:
                # We expect an operator or right parenthesis
                if token_type not in ['OPERATOR', 'RPAREN']:
                    raise ValueError(f"Expected an operator at position {i}, got {token_type}")
                expect_value = True

            # Special check for parentheses
            if token_type == 'RPAREN' and last_token_type == 'LPAREN':
                raise ValueError("Empty parentheses are not allowed")

            last_token_type = token_type

        # Final check: expression should end with a value
        if expect_value:
            raise ValueError("Incomplete dice expression")