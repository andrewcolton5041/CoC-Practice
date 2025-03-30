"""
Dice Roller Utility

This script defines functions to parse and evaluate standard dice notation strings 
(e.g., '2D6', '1D20+5', '3D4-2') commonly used in tabletop RPGs like Call of Cthulhu.

Supported Formats:
- Basic:         "3D6" or "1D20+3" or "4D4-1"
- Parenthetical: "(2D6+6)*5" or "(3D4-2)*2"

Functions:
- roll_dice():     Parses and evaluates a dice string, returns the total result as an integer.
- improvementCheck(): Determines if a stat can improve based on a 1D100 roll.
- successCheck():  Evaluates a roll result against a stat and returns the success level.

Raises:
    ValueError if the input dice string format is invalid.
"""

import re
import random
import operator


def roll_dice(dice_string):
    """
    Parses and rolls a dice expression, with optional inner math and outer multiplication.

    Example Inputs:
        "3D6"
        "1D20+3"
        "(2D6+6)*5"

    Returns:
        Integer result of the evaluated dice roll.
    """
    # Regular expression matches either:
    # - (XdY ± Z) * multiplier
    # - XdY ± Z
    pattern = r"""
        ^\(\s*(\d+)D(\d+)\s*(?:([+\-*])\s*(\d+))?\)\s*\*\s*(\d+)$   # With parentheses and outer *
        |^(\d+)D(\d+)\s*(?:([+\-*])\s*(\d+))?$                     # Simple format
    """
    match = re.fullmatch(pattern, dice_string.strip(), flags=re.IGNORECASE | re.VERBOSE)

    if not match:
        raise ValueError("Invalid dice string format")

    # Parse matched groups based on which pattern matched
    if match.group(1):  # Match with parentheses and outer multiplier
        num_dice = int(match.group(1))
        dice_sides = int(match.group(2))
        op = match.group(3)
        modifier = int(match.group(4)) if match.group(4) else 0
        multiplier = int(match.group(5))
    else:  # Simple format without outer multiplier
        num_dice = int(match.group(6))
        dice_sides = int(match.group(7))
        op = match.group(8)
        modifier = int(match.group(9)) if match.group(9) else 0
        multiplier = 1

    # Roll the dice
    rolls = [random.randint(1, dice_sides) for _ in range(num_dice)]
    total = sum(rolls)

    # Apply inner operator if present
    ops = {'+': operator.add, '-': operator.sub, '*': operator.mul}
    if op in ops:
        total = ops[op](total, modifier)

    # Apply outer multiplier
    total *= multiplier

    return total