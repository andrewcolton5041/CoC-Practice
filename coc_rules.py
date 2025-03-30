"""
Call of Cthulhu Rules Module

This module implements the core rules mechanics for the Call of Cthulhu roleplaying game,
primarily focusing on skill checks and the various success levels.

The module provides functions for:
- Improvement checks (used for character development)
- Success checks (to determine outcome of skill attempts)

These functions follow the 7th edition Call of Cthulhu rules.

Author: Unknown
Version: 1.1
Last Updated: 2025-03-30
"""

import dice_roll as dr

def improvement_check(stat):
    """
    Determines if a character's stat can improve based on a d100 roll.

    In Call of Cthulhu, skills can improve if the player rolls higher than 
    their current skill value on a d100 roll.

    Args:
        stat (int): The current value of the stat or skill (0-100).

    Returns:
        bool: True if the check succeeds (roll > stat), False otherwise.
    """
    return dr.roll_dice("1D100") > stat

def success_check(stat):
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
    roll = dr.roll_dice("1D100")

    # Check for Extreme Success (Critical) - 1/5 of skill value
    if roll <= stat / 5:
        return "Extreme Success"
    # Check for Hard Success - 1/2 of skill value
    elif roll <= stat / 2:
        return "Hard Success"
    # Check for Regular Success - equal to or under skill value
    elif roll <= stat:
        return "Regular Success"
    # Check for Fumble - 96-100 for skills 50 or less, only 100 for skills over 50
    elif (stat <= 50 and 96 <= roll <= 100) or (stat > 50 and roll == 100):
        return "Fumble"
    # Everything else is a normal failure
    else:
        return "Failure"