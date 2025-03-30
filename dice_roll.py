"""
Dice Roller Utility for Call of Cthulhu RPG

This module provides functionality to parse and evaluate dice notation strings
commonly used in tabletop RPGs like Call of Cthulhu.

The module can handle various dice formats including:
- Basic rolls:         "3D6" or "1D20+3" or "4D4-1" 
- Parenthetical rolls: "(2D6+6)*5" or "(3D4-2)*2"

Author: Unknown
Version: 1.1
Last Updated: 2025-03-30
"""

import re
import random
import operator


def roll_dice(dice_string):
    """
    Parses and rolls a dice expression, evaluating the result according to RPG dice notation.

    Supports standard dice notation with various formats:
    - Simple dice rolls: "3D6", "1D20"
    - Dice with modifiers: "1D20+3", "4D4-1"
    - Complex expressions: "(2D6+6)*5"

    Args:
        dice_string (str): A string representing dice to roll in standard RPG notation.

    Returns:
        int: The final calculated result of the dice roll expression.

    Raises:
        ValueError: If the input dice string format is invalid or cannot be parsed.
    """
    # Regular expression pattern to match dice notation with or without parentheses and multiplier
    # The pattern is verbose to handle complex dice expressions
    pattern = r"""
        ^\(\s*(\d+)D(\d+)\s*(?:([+\-*])\s*(\d+))?\)\s*\*\s*(\d+)$   # With parentheses and outer *
        |^(\d+)D(\d+)\s*(?:([+\-*])\s*(\d+))?$                     # Simple format
    """
    # Attempt to match the dice string against our pattern
    match = re.fullmatch(pattern, dice_string.strip(), flags=re.IGNORECASE | re.VERBOSE)

    # If no match, the format is invalid
    if not match:
        raise ValueError("Invalid dice string format")

    # Determine which pattern matched and extract the relevant components
    if match.group(1):  # Match with parentheses and outer multiplier
        num_dice = int(match.group(1))      # Number of dice to roll
        dice_sides = int(match.group(2))    # Number of sides on each die
        op = match.group(3)                 # Operator for modifier (+, -, *)
        modifier = int(match.group(4)) if match.group(4) else 0  # Numeric modifier
        multiplier = int(match.group(5))    # Outer multiplier
    else:  # Simple format without outer multiplier
        num_dice = int(match.group(6))      # Number of dice to roll
        dice_sides = int(match.group(7))    # Number of sides on each die
        op = match.group(8)                 # Operator for modifier
        modifier = int(match.group(9)) if match.group(9) else 0  # Numeric modifier
        multiplier = 1                      # Default multiplier (no effect)

    # Roll the specified number of dice with the given sides
    rolls = [random.randint(1, dice_sides) for _ in range(num_dice)]
    total = sum(rolls)

    # Map operators to their corresponding functions
    ops = {'+': operator.add, '-': operator.sub, '*': operator.mul}

    # Apply inner operator if present
    if op in ops:
        total = ops[op](total, modifier)

    # Apply outer multiplier
    total *= multiplier

    return total