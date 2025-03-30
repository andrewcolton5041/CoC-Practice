"""
Call of Cthulhu Rules Module

This module implements the core rules mechanics for the Call of Cthulhu roleplaying game,
primarily focusing on skill checks and the various success levels.

The module provides functions for:
- Improvement checks (used for character development)
- Success checks (to determine outcome of skill attempts)

These functions follow the 7th edition Call of Cthulhu rules.

Author: Unknown
Version: 2.0
Last Updated: 2025-03-30
"""

# Imports
from src.dice_roll import roll_dice  # Use the one you actually need
from src.dice_parser_exceptions import DiceParserError, TokenizationError, ValidationError
from constants import (
    EXTREME_SUCCESS_DIVISOR,
    HARD_SUCCESS_DIVISOR,
    FUMBLE_THRESHOLD_MIN,
    FUMBLE_THRESHOLD_STAT,
    D100_DICE,
    SUCCESS_LEVELS
)

def success_check(stat, use_cache=True):
    try:
        roll = roll_dice(D100_DICE, use_cache=use_cache)
        extreme_threshold = stat // EXTREME_SUCCESS_DIVISOR
        hard_threshold = stat // HARD_SUCCESS_DIVISOR

        if roll <= extreme_threshold:
            return SUCCESS_LEVELS["EXTREME_SUCCESS"]
        elif roll <= hard_threshold:
            return SUCCESS_LEVELS["HARD_SUCCESS"]
        elif roll <= stat:
            return SUCCESS_LEVELS["REGULAR_SUCCESS"]
        elif ((stat <= FUMBLE_THRESHOLD_STAT
               and FUMBLE_THRESHOLD_MIN <= roll <= 100)
              or (stat > FUMBLE_THRESHOLD_STAT and roll == 100)):
            return SUCCESS_LEVELS["FUMBLE"]
        else:
            return SUCCESS_LEVELS["FAILURE"]
    except DiceParserError as e:
        print(f"Error in success check: {e}")
        return SUCCESS_LEVELS["FAILURE"]


def improvement_check(stat, use_cache=True):
    return roll_dice(D100_DICE, use_cache=use_cache) > stat


def get_success_level(skill_value, roll):
    extreme_threshold = skill_value // EXTREME_SUCCESS_DIVISOR
    hard_threshold = skill_value // HARD_SUCCESS_DIVISOR

    if roll <= extreme_threshold:
        return SUCCESS_LEVELS["EXTREME_SUCCESS"]
    elif roll <= hard_threshold:
        return SUCCESS_LEVELS["HARD_SUCCESS"]
    elif roll <= skill_value:
        return SUCCESS_LEVELS["REGULAR_SUCCESS"]
    elif ((skill_value <= FUMBLE_THRESHOLD_STAT
           and FUMBLE_THRESHOLD_MIN <= roll <= 100)
          or (skill_value > FUMBLE_THRESHOLD_STAT and roll == 100)):
        return SUCCESS_LEVELS["FUMBLE"]
    else:
        return SUCCESS_LEVELS["FAILURE"]
