"""
Dice Roller Utility for Call of Cthulhu RPG

This module provides functionality to parse and evaluate dice notation strings
commonly used in tabletop RPGs like Call of Cthulhu.

The module can handle various dice formats including:
- Basic rolls:         "3D6" or "1D20+3" or "4D4-1" 
- Parenthetical rolls: "(2D6+6)*5" or "(3D4-2)*2"

Each function is documented with its purpose, parameters, and return values.

Author: Andrew C
Version: 1.0
Last Updated: 03/31/2025
"""

import re
import random
import operator
from typing import TypedDict, List, Union, overload, Literal
from src.constants import Dice, RegexFlags, ErrorMessages, MaxLimits


class DiceResult(TypedDict):
    '''
    Dictionary to store the result of a dice roll
    '''

    total: int
    rolls: List[int]

# First overload: when return_details is False (default)
@overload
def roll_dice(dice_string: str, return_details: Literal[False] = False) -> int: ...

# Second overload: when return_details is True
@overload
def roll_dice(dice_string: str, return_details: Literal[True] = True) -> DiceResult: ...

# Actual implementation
def roll_dice(dice_string: str, return_details: bool = False) -> Union[int, DiceResult]:
    '''
    Rolls a set of dice based on the given dice string.
    Args:
        dice_string (str): A string representing the dice to be rolled.
        return_details (bool): Whether to return just the total (False) or detailed results (True).
    Returns:
        int | DiceResult: The total value of the rolled dice or a dictionary with total and individual rolls.
    Raises:
        ValueError: If the dice string is invalid.
    '''

    #parse the dice string
    pattern = Dice.DicePattern.DICE_PATTERN

    match = re.search(pattern, dice_string, RegexFlags.CASE_INSENSITIVE)

    if not match:
        raise ValueError(f"{ErrorMessages.DICE_VALUE_ERROR}: '{dice_string}'")

    num_dice = int(match.group(1))
    dice_sides = int(match.group(2))
    add_sub = match.group(4)
    modifier = int(match.group(5)) if match.group(4) else 0
    multiplier = int(match.group(7)) if match.group(6) else 0

    #Check to see if the number of dice is within the limit
    if num_dice > MaxLimits.MAX_DICE_NUM:
        raise ValueError(f"{ErrorMessages.DICE_NUM_ERROR}: '{dice_string}'")
    #Check to see if the number of dice sides is within the limit
    if dice_sides > MaxLimits.MAX_DICE_SIDES:
        raise ValueError(f"{ErrorMessages.DICE_SIDE_ERROR}: '{dice_string}'")

    #roll the dice
    rolls = [random.randint(1, dice_sides) for _ in range(num_dice)]
    total = sum(rolls)
    #calculate the total
    if add_sub == "+":
        total += modifier
    elif add_sub == "-":
        total -= modifier

    if multiplier > 1:
        total *= multiplier
    #return the result

    if return_details:
        return {"total": total, "rolls": rolls}
    else:
        return total