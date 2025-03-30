"""
Dice Parser Module for Call of Cthulhu RPG

This module provides a robust parser for dice notation expressions commonly used 
in tabletop RPGs like Call of Cthulhu. It uses a token-based approach rather than 
complex regular expressions, making it more maintainable and extensible.

The module can handle various dice formats including:
- Basic rolls:         "3D6" or "1D20+3" or "4D4-1" 
- Parenthetical rolls: "(2D6+6)*5" or "(3D4-2)*2"

Author: Unknown
Version: 1.0
Last Updated: 2025-03-30
"""

import random
import operator


class DiceParser:
    """
    A class for parsing and evaluating dice notation expressions.

    This parser uses a token-based approach to handle dice expressions, breaking them
    down into components and evaluating them according to standard RPG rules.
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
        Convert a dice string into tokens for processing.

        Args:
            dice_string (str): A string in standard dice notation

        Returns:
            list: A list of tokens representing the dice expression

        Raises:
            ValueError: If the dice string contains invalid tokens
        """
        # Remove all whitespace
        dice_string = dice_string.replace(' ', '').upper()

        # Initialize an empty list of tokens and current token
        tokens = []
        current = ''

        # Process each character
        i = 0
        while i < len(dice_string):
            char = dice_string[i]

            # Check for dice notation (e.g., "3D6")
            if char == 'D' and current.isdigit():
                dice_count = int(current)
                current = 'D'
                i += 1

                # Get the number of sides
                sides = ''
                while i < len(dice_string) and dice_string[i].isdigit():
                    sides += dice_string[i]
                    i += 1

                if not sides:
                    raise ValueError("Invalid dice notation: missing sides value after 'D'")

                # Add the dice roll token
                tokens.append(('DICE', (dice_count, int(sides))))
                current = ''
                continue

            # Handle operators
            if char in self.operators or char in '()':
                # Add any accumulated digits as a number token
                if current:
                    if current.isdigit():
                        tokens.append(('NUMBER', int(current)))
                    else:
                        raise ValueError(f"Invalid token: {current}")
                    current = ''

                # Add the operator or parenthesis token
                if char in self.operators:
                    tokens.append(('OPERATOR', char))
                elif char == '(':
                    tokens.append(('LPAREN', char))
                elif char == ')':
                    tokens.append(('RPAREN', char))
                i += 1
                continue

            # Accumulate digits for numbers
            if char.isdigit():
                current += char
                i += 1
                continue

            # Invalid character
            raise ValueError(f"Invalid character in dice string: {char}")

        # Add any remaining token
        if current:
            if current.isdigit():
                tokens.append(('NUMBER', int(current)))
            else:
                raise ValueError(f"Invalid token: {current}")

        return tokens

    def parse(self, tokens):
        """
        Parse tokenized dice expression and evaluate it.

        Args:
            tokens (list): List of tokens from the tokenize method

        Returns:
            int: The result of evaluating the dice expression

        Raises:
            ValueError: If the expression has invalid syntax
        """
        # Handle empty token list
        if not tokens:
            raise ValueError("Empty dice expression")

        # Define a helper function to evaluate a sequence of tokens
        def evaluate_sequence(token_seq):
            # Process dice rolls first
            values = []
            operators_seq = []

            i = 0
            while i < len(token_seq):
                token_type, token_value = token_seq[i]

                if token_type == 'NUMBER':
                    values.append(token_value)
                elif token_type == 'DICE':
                    # Roll the dice and add the result
                    count, sides = token_value
                    result = sum(random.randint(1, sides) for _ in range(count))
                    values.append(result)
                elif token_type == 'OPERATOR':
                    operators_seq.append(token_value)
                elif token_type == 'LPAREN':
                    # Find the matching parenthesis
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

                    # Evaluate the sub-expression
                    sub_expr = token_seq[i+1:j-1]
                    values.append(evaluate_sequence(sub_expr))
                    i = j  # Skip the processed tokens
                    continue

                i += 1

            # Ensure we have a valid expression
            if not values:
                raise ValueError("No values in expression")

            if len(values) != len(operators_seq) + 1:
                raise ValueError("Mismatched number of values and operators")

            # Calculate the result using the operators in order
            # This is a simplified approach that doesn't handle operator precedence
            result = values[0]
            for i, op in enumerate(operators_seq):
                result = self.operators[op](result, values[i+1])

            return result

        # Evaluate the complete token sequence
        return evaluate_sequence(tokens)

    def roll_dice(self, dice_string):
        """
        Parse a dice notation string and roll the dice.

        Args:
            dice_string (str): A string in standard dice notation

        Returns:
            int: The result of evaluating the dice expression

        Raises:
            ValueError: If the dice string has invalid syntax
        """
        try:
            tokens = self.tokenize(dice_string)
            return self.parse(tokens)
        except ValueError as e:
            raise ValueError(f"Error parsing dice string '{dice_string}': {e}")

    @staticmethod
    def roll_dice_with_details(dice_string):
        """
        Roll dice and return both the total and individual die results.

        This is useful for systems that need to know the individual die results,
        such as critical hit determination in some RPG systems.

        Args:
            dice_string (str): A simple dice notation (e.g., "3d6")

        Returns:
            tuple: (total, individual_rolls)

        Raises:
            ValueError: If the dice string is not a simple dice roll
        """
        # Simplify the dice string
        dice_string = dice_string.replace(' ', '').upper()

        # Check for simple dice roll format (e.g., "3D6")
        parts = dice_string.split('D')
        if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
            raise ValueError("For detailed rolls, use simple dice notation (e.g., '3D6')")

        count = int(parts[0])
        sides = int(parts[1])

        # Roll the dice and track individual results
        rolls = [random.randint(1, sides) for _ in range(count)]
        total = sum(rolls)

        return (total, rolls)