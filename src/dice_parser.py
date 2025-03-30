"""
Dice Parser Module for Call of Cthulhu RPG

This module provides a robust parser for dice notation expressions commonly used 
in tabletop RPGs like Call of Cthulhu. It uses efficient regex-based tokenization
instead of character-by-character processing for better performance.

The module can handle various dice formats including:
- Basic rolls:         "3D6" or "1D20+3" or "4D4-1" 
- Parenthetical rolls: "(2D6+6)*5" or "(3D4-2)*2"

Author: Unknown
Version: 3.0
Last Updated: 2025-03-30
"""

import random
import operator
import re


class DiceParser:
    """
    A class for parsing and evaluating dice notation expressions.

    This parser uses regex-based tokenization to efficiently handle dice expressions,
    breaking them down into components and evaluating them according to standard RPG rules.
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

    def _get_deterministic_roll(self, sides, count=1):
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

    def parse(self, tokens, deterministic=False):
        """
        Parse tokenized dice expression and evaluate it.

        Args:
            tokens (list): List of tokens from the tokenize method
            deterministic (bool): If True, use deterministic values instead of random

        Returns:
            int: The result of evaluating the dice expression

        Raises:
            ValueError: If the expression has invalid syntax
        """
        # Store the deterministic setting for this parse operation
        old_deterministic = self._deterministic_mode
        if deterministic:
            self._deterministic_mode = True

        try:
            # Handle empty token list
            if not tokens:
                raise ValueError("Empty dice expression")

            # Define a helper function to evaluate a sequence of tokens
            def evaluate_sequence(token_seq):
                # Process dice rolls first
                values = []
                operators_seq = []

                i = 0  # Fixed: changed from a0 to 0
                while i < len(token_seq):
                    token_type, token_value = token_seq[i]

                    if token_type == 'NUMBER':
                        values.append(token_value)
                    elif token_type == 'DICE':
                        # Roll the dice and add the result
                        count, sides = token_value

                        if self._deterministic_mode:
                            # Use deterministic values for testing
                            roll_values = self._get_deterministic_roll(sides, count)
                            result = sum(roll_values)
                            # Increment the counter for next deterministic roll
                            self._next_deterministic_value += 1
                        else:
                            # Use random for normal operation
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

        finally:
            # Restore the previous deterministic mode
            self._deterministic_mode = old_deterministic

    def roll_dice(self, dice_string, deterministic=False, seed=None):
        """
        Parse a dice notation string and roll the dice.

        Args:
            dice_string (str): A string in standard dice notation
            deterministic (bool): If True, use deterministic values instead of random
            seed (int, optional): Seed for the random number generator

        Returns:
            int: The result of evaluating the dice expression

        Raises:
            ValueError: If the dice string has invalid syntax
        """
        # Initialize state variable to avoid "possibly unbound" error
        state = None

        # Set seed if provided for reproducible randomness
        if seed is not None and not deterministic:
            # Store the current state
            state = random.getstate()
            # Set the seed
            random.seed(seed)

        try:
            tokens = self.tokenize(dice_string)
            return self.parse(tokens, deterministic)
        except ValueError as e:
            raise ValueError(f"Error parsing dice string '{dice_string}': {e}")
        finally:
            # Restore the random state if seed was set
            if seed is not None and not deterministic and state is not None:
                random.setstate(state)

    def roll_dice_with_details(self, dice_string, deterministic=False, seed=None):
        """
        Roll dice and return both the total and individual die results.

        Args:
            dice_string (str): A simple dice notation (e.g., "3d6")
            deterministic (bool): If True, use deterministic values instead of random
            seed (int, optional): Seed for the random number generator

        Returns:
            tuple: (total, individual_rolls)

        Raises:
            ValueError: If the dice string is not a simple dice roll
        """
        # Initialize state variable to avoid "possibly unbound" error
        state = None

        # Set seed if provided for reproducible randomness
        if seed is not None and not deterministic:
            # Store the current state
            state = random.getstate()
            # Set the seed
            random.seed(seed)

        try:
            # Simplify the dice string
            dice_string = dice_string.replace(' ', '').upper()

            # Check for simple dice roll format using regex
            match = re.match(r'^(\d+)D(\d+)$', dice_string)
            if not match:
                raise ValueError("For detailed rolls, use simple dice notation (e.g., '3D6')")

            count = int(match.group(1))
            sides = int(match.group(2))

            # Roll the dice and track individual results
            if deterministic or self._deterministic_mode:
                # Use deterministic values for testing
                rolls = self._get_deterministic_roll(sides, count)
                # Increment the counter for next deterministic roll
                self._next_deterministic_value += 1
            else:
                # Use random for normal operation
                rolls = [random.randint(1, sides) for _ in range(count)]

            total = sum(rolls)

            return (total, rolls)

        finally:
            # Restore the random state if seed was set
            if seed is not None and not deterministic and state is not None:
                random.setstate(state)