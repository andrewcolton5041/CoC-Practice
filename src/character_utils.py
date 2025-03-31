"""
Game Utilities for Call of Cthulhu

This module provides game mechanics utilities for the Call of Cthulhu RPG system,
building on the basic dice rolling and rules modules.

Major functions include:
- Character skill checks
- Opposed checks between characters
- Weapon damage calculation

These functions implement game mechanics based on Call of Cthulhu 7th edition rules.

Author: Unknown
Version: 1.0
Last Updated: Unknown
"""

from typing import Dict, Tuple
from src.dice_roll import roll_dice
from src.coc_rules import success_check
from src.constants import CharacterSheetKeys, Dice, OtherConstants, SuccessLevel, CharacterUtils, ErrorMessages

def skill_check(character_data: Dict, skill_name: str) -> Tuple[int, SuccessLevel]:
    """
    Perform a skill check for a character using their character sheet data.

    The function accesses the character's skill or attribute value and then
    performs a d100 roll to determine the success level.

    Args:
        character_data (dict): The character dictionary containing all character information
        skill_name (str): The name of the skill or attribute to check

    Returns:
        tuple: A tuple containing (roll_result, success_level)

    Raises:
        ValueError: If the specified skill or attribute doesn't exist for the character
    """
    # First, try to locate the skill value in the character data
    skill_value = OtherConstants.NONE
    if CharacterSheetKeys.SKILLS in character_data and skill_name in character_data[CharacterSheetKeys.SKILLS]:
        # Look in skills first
        skill_value = character_data[CharacterSheetKeys.SKILLS][skill_name]
    elif skill_name in character_data[CharacterSheetKeys.ATTRIBUTES]:
        # If not found in skills, check attributes
        skill_value = character_data[CharacterSheetKeys.ATTRIBUTES][skill_name]
    else:
        # If not found in either location, raise an error
        raise ValueError(f"Skill or attribute '{skill_name}' not found for this character")

    return (roll_dice(Dice.BasicDice.PERCENTILE_DIE.value), success_check(skill_value))

def opposed_check(char1_data: Dict, char1_skill: str, char2_data: Dict, char2_skill: str) -> str:
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

    Returns:
        str: A string describing the result of the opposed check
    """
    # Perform skill checks for both characters
    char1_roll, char1_success = skill_check(char1_data, char1_skill)
    char2_roll, char2_success = skill_check(char2_data, char2_skill)

    # Map success levels to numerical values for easy comparison
    success_levels = {
        SuccessLevel.EXTREME_SUCCESS: 4,
        SuccessLevel.HARD_SUCCESS: 3,
        SuccessLevel.REGULAR_SUCCESS: 2,
        SuccessLevel.FAILURE: 1,
        SuccessLevel.FUMBLE: 0
    }

    # Convert success levels to numerical values
    char1_level = success_levels[char1_success]
    char2_level = success_levels[char2_success]

    # Compare success levels
    if char1_level > char2_level:
        return CharacterUtils.opposed_check_win(char1_data['name'], False)
    elif char2_level > char1_level:
        return CharacterUtils.opposed_check_win(char2_data['name'], False)
    else:
        # If same success level, compare the margins of success
        char1_margin = get_skill_value(char1_data, char1_skill) - char1_roll
        char2_margin = get_skill_value(char2_data, char2_skill) - char2_roll

        if char1_margin > char2_margin:
            return CharacterUtils.opposed_check_win(char1_data['name'], True)
        elif char2_margin > char1_margin:
            return CharacterUtils.opposed_check_win(char2_data['name'], True)
        else:
            return CharacterUtils.OPP_CHECK_TIE

def get_skill_value(character_data: Dict, skill_name: str) -> int:
    """
    Helper function to get a skill or attribute value from character data.

    Args:
        character_data (dict): The character dictionary data
        skill_name (str): The name of the skill or attribute to retrieve

    Returns:
        int: The value of the skill or attribute

    Raises:
        ValueError: If the skill or attribute doesn't exist for the character
    """
    if 'skills' in character_data and skill_name in character_data[CharacterSheetKeys.SKILLS]:
        return character_data[CharacterSheetKeys.SKILLS][skill_name]
    elif skill_name in character_data[CharacterSheetKeys.ATTRIBUTES]:
        return character_data[CharacterSheetKeys.ATTRIBUTES][skill_name]
    else:
        raise ValueError(ErrorMessages.skill_value_not_found(skill_name))

def roll_damage(weapon_data: Dict) -> int | str:
    """
    Calculate damage for a weapon attack based on its damage formula.

    Handles various damage formulas including those with character damage bonuses.

    Args:
        weapon_data (dict): The weapon dictionary containing the damage formula

    Returns:
        int or str: The calculated damage result or the damage formula if it can't be calculated
    """
    
    try:
        # Try to directly roll the damage formula
        return roll_dice(weapon_data[CharacterSheetKeys.DAMAGE])
    except ValueError:
        # Handle damage formulas that might involve damage bonus
        damage_formula = weapon_data[CharacterSheetKeys.DAMAGE]

        # Special handling for common damage bonus pattern
        if '+1D4' in damage_formula:
            # Split the formula and roll parts separately
            base_damage = damage_formula.replace(Dice.DamageBonusDice.ONE_BONUS_DICE, '')
            bonus_damage = roll_dice(Dice.BasicDice.DFOUR.value)
            return roll_dice(base_damage) + bonus_damage
        else:
            # Return the formula string if we can't parse it
            return damage_formula