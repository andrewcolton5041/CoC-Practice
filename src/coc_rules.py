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

from src.dice_roll import roll_dice, get_cache_stats, clear_dice_cache


def improvement_check(stat, use_cache=True):
    """
    Determines if a character's stat can improve based on a d100 roll.

    In Call of Cthulhu, skills can improve if the player rolls higher than 
    their current skill value on a d100 roll.

    Args:
        stat (int): The current value of the stat or skill (0-100).
        use_cache (bool, optional): Whether to use dice roll caching. Defaults to True.

    Returns:
        bool: True if the check succeeds (roll > stat), False otherwise.
    """
    return roll_dice("1D100", use_cache=use_cache) > stat


def success_check(stat, use_cache=True):
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
        use_cache (bool, optional): Whether to use dice roll caching. Defaults to True.

    Returns:
        str: One of: "Extreme Success", "Hard Success", "Regular Success", "Failure", or "Fumble"
    """
    # Roll a d100
    roll = roll_dice("1D100", use_cache=use_cache)

    # Calculate success thresholds
    extreme_threshold = stat // 5
    hard_threshold = stat // 2

    # Check for Extreme Success (Critical) - 1/5 of skill value
    if roll <= extreme_threshold:
        return "Extreme Success"
    # Check for Hard Success - 1/2 of skill value
    elif roll <= hard_threshold:
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


def opposed_check(char1_data, char1_skill, char2_data, char2_skill, use_cache=True):
    """
    Perform an opposed check between two characters.

    In opposed checks, both characters make skill checks and the results are compared.
    The character with the higher success level wins. If both achieve the same level,
    the character with the better margin of success wins.

    Args:
        char1_data (dict): First character's data dictionary
        char1_skill (str): First character's skill name to check
        char2_data (dict): Second character's data dictionary
        char2_skill (str): Second character's skill name to check
        use_cache (bool, optional): Whether to use dice roll caching. Defaults to True.

    Returns:
        tuple: (winner, char1_success, char2_success, char1_roll, char2_roll)
            winner can be 1, 2, or 0 (tie)
    """
    # Get skill values
    char1_value = get_skill_value(char1_data, char1_skill)
    char2_value = get_skill_value(char2_data, char2_skill)

    # Roll for each character
    char1_roll = roll_dice("1D100", use_cache=use_cache)
    char2_roll = roll_dice("1D100", use_cache=use_cache)

    # Determine success levels
    char1_success = get_success_level(char1_value, char1_roll)
    char2_success = get_success_level(char2_value, char2_roll)

    # Map success levels to numerical values for easy comparison
    success_levels = {
        "Extreme Success": 4,
        "Hard Success": 3,
        "Regular Success": 2,
        "Failure": 1,
        "Fumble": 0
    }

    # Convert success levels to numerical values
    char1_level = success_levels[char1_success]
    char2_level = success_levels[char2_success]

    # Determine winner based on success level
    if char1_level > char2_level:
        winner = 1
    elif char2_level > char1_level:
        winner = 2
    else:
        # If same success level, compare margins
        char1_margin = char1_value - char1_roll
        char2_margin = char2_value - char2_roll

        if char1_margin > char2_margin:
            winner = 1
        elif char2_margin > char1_margin:
            winner = 2
        else:
            winner = 0  # Tie

    return (winner, char1_success, char2_success, char1_roll, char2_roll)


def get_skill_value(character_data, skill_name):
    """
    Get the value of a skill or attribute from character data.

    Args:
        character_data (dict): Character data dictionary
        skill_name (str): Name of the skill or attribute to retrieve

    Returns:
        int: The skill or attribute value

    Raises:
        ValueError: If the skill or attribute doesn't exist
    """
    if 'skills' in character_data and skill_name in character_data['skills']:
        return character_data['skills'][skill_name]
    elif 'attributes' in character_data and skill_name in character_data['attributes']:
        return character_data['attributes'][skill_name]
    else:
        raise ValueError(f"Skill or attribute '{skill_name}' not found for character")


def get_success_level(skill_value, roll):
    """
    Determine the success level based on skill value and roll.

    This is a helper function used by other rule functions.

    Args:
        skill_value (int): The character's skill value
        roll (int): The result of a d100 roll

    Returns:
        str: One of: "Extreme Success", "Hard Success", "Regular Success", "Failure", or "Fumble"
    """
    # Calculate success thresholds
    extreme_threshold = skill_value // 5
    hard_threshold = skill_value // 2

    # Check for various success levels
    if roll <= extreme_threshold:
        return "Extreme Success"
    elif roll <= hard_threshold:
        return "Hard Success"
    elif roll <= skill_value:
        return "Regular Success"
    elif (skill_value <= 50 and 96 <= roll <= 100) or (skill_value > 50 and roll == 100):
        return "Fumble"
    else:
        return "Failure"


def get_rules_cache_stats():
    """
    Get statistics about the dice cache used by the rules module.

    Returns:
        dict: Cache statistics from the dice_roll module
    """
    return get_cache_stats()


def clear_rules_cache():
    """
    Clear the dice cache used by the rules module.

    Returns:
        dict: Statistics about the cleared cache
    """
    return clear_dice_cache()