"""
Call of Cthulhu Rules Module

This module implements the core rules mechanics for the Call of Cthulhu roleplaying game,
primarily focusing on skill checks and the various success levels.

The module provides functions for:
- Improvement checks (used for character development)
- Success checks (to determine outcome of skill attempts)

These functions follow the 7th edition Call of Cthulhu rules.

Author: Andrew C
Version: 1.0
Last Updated: 03/31/2025
"""

import src.dice_roll as dr
from src.constants import SuccessLevel, Dice, FumbleBoundaries, HalfFifth

def improvement_check(stat: int)-> bool:
    """
    Determines if a character's stat can improve based on a d100 roll.

    In Call of Cthulhu, skills can improve if the player rolls higher than 
    their current skill value on a d100 roll.

    Args:
        stat (int): The current value of the stat or skill (0-100).

    Returns:
        bool: True if the check succeeds (roll > stat), False otherwise.
    """
    return dr.roll_dice(Dice.PERCENTILE_DIE, False) > stat

def success_check(stat: int) -> str:
    """
    Rolls 1D100 and determines the level of success based on the character's stat.

    According to CoC rules, the success level depends on how much lower the roll is
    compared to the character's stat:
    - Extreme Success: roll <= stat/5
    - Hard Success: roll <= stat/2
    - Regular Success: roll <= stat
    - Fumble: special case for very high rolls
    - Failure: roll > stat (and not a fumble)

    Args:
        stat (int): The character's stat or skill value (0-100).

    Returns:
        str: One of: "Extreme Success", "Hard Success", "Regular Success", "Failure", or "Fumble"
    """
    # Roll a d100
    roll = dr.roll_dice(Dice.PERCENTILE_DIE)

    # Check for Extreme Success (Critical) - 1/5 of skill value
    if roll <= stat / HalfFifth.FIFTH_VALUE:
        return SuccessLevel.EXTREME_SUCCESS
    # Check for Hard Success - 1/2 of skill value
    elif roll <= stat / HalfFifth.HALF_VALUE:
        return SuccessLevel.HARD_SUCCESS
    # Check for Regular Success - equal to or under skill value
    elif roll <= stat:
        return SuccessLevel.REGULAR_SUCCESS
    # Check for Fumble - 96-100 for skills 50 or less, only 100 for skills over 50
    elif (stat <= FumbleBoundaries.FUMBLE_REDUCED_CHECK and FumbleBoundaries.FUMBLE_REDUCED_CHECK_MIN <= roll) or (stat > FumbleBoundaries.FUMBLE_REDUCED_CHECK and roll == FumbleBoundaries.FUMBLE_CHECK_MIN):
        return SuccessLevel.FUMBLE
    # Everything else is a normal failure
    else:
        return SuccessLevel.FAILURE