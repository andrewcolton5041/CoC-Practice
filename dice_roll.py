"""
Dice Roller Utility

This script defines a function `roll_dice` that parses and evaluates standard dice notation strings 
(e.g., '2D6', '1D20+5', '3D4-2') commonly used in tabletop RPGs. It supports rolling a specified number 
of dice with a given number of sides, along with optional addition, subtraction, or multiplication modifiers.

It can also handle expressions where the operation is outside the parentheses:
    Example:
        (2D6 + 6)*5 -> Rolls two 6-sided dice, adds 6, and multiplies the total by 5
        (2D6 - 3)*2 -> Rolls two 6-sided dice, subtracts 3, and multiplies the total by 2

Usage:
    roll_dice("2D6")      -> Rolls two 6-sided dice
    roll_dice("1D20+3")   -> Rolls one 20-sided die and adds 3
    roll_dice("(4D4-1)*3") -> Rolls four 4-sided dice, subtracts 1, then multiplies the total by 3

Returns:
    The total result as an integer.
Raises:
    ValueError if the input string format is invalid.
"""

import re
import random
import operator


def roll_dice(dice_string):
    # First, remove extra spaces and match the general pattern, including the outer multiplication (if any)
    pattern = r"(?i)^\((\d+)D(\d+)(?:\s*([+\-*])\s*(\d+))?\)\s*\*\s*(\d+)$|^(\d+)D(\d+)(?:\s*([+\-*])\s*(\d+))?$"
    match = re.fullmatch(pattern, dice_string.strip())

    if not match:
        raise ValueError("Invalid dice string format")

    if match.group(1):  # This means we matched the outer multiplication case
        num_dice, dice_sides = int(match.group(1)), int(match.group(2))
        operator_symbol = match.group(3)
        modifier = int(match.group(4)) if match.group(4) else 0
        multiplier = int(match.group(5))  # The number outside parentheses
    else:
        num_dice, dice_sides = int(match.group(6)), int(match.group(7))
        operator_symbol = match.group(8)
        modifier = int(match.group(9)) if match.group(9) else 0
        multiplier = 1  # No outer multiplication

    # Roll the dice
    rolls = [random.randint(1, dice_sides) for _ in range(num_dice)]
    total = sum(rolls)

    # Apply the inner modifier (+, -, *)
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
    }

    if operator_symbol:
        total = ops[operator_symbol](total, modifier)

    # Apply the outer multiplication (if any)
    total *= multiplier

    return total
