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
Version: 1.2
Last Updated: 2025-03-30
"""

import dice_roll as dr
import coc_rules as rules

def skill_check(character_data, skill_name):
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
    skill_value = None
    if 'skills' in character_data and skill_name in character_data['skills']:
        # Look in skills first
        skill_value = character_data['skills'][skill_name]
    elif skill_name in character_data['attributes']:
        # If not found in skills, check attributes
        skill_value = character_data['attributes'][skill_name]
    else:
        # If not found in either location, raise an error
        raise ValueError(f"Skill or attribute '{skill_name}' not found for this character")

    # Roll a d100 for the check
    roll = dr.roll_dice("1D100")

    # Determine the success level based on the roll and skill value
    if roll <= skill_value / 5:
        success_level = "Extreme Success"
    elif roll <= skill_value / 2:
        success_level = "Hard Success"
    elif roll <= skill_value:
        success_level = "Regular Success"
    elif (skill_value <= 50 and 96 <= roll <= 100) or (skill_value > 50 and roll == 100):
        success_level = "Fumble"
    else:
        success_level = "Failure"

    return (roll, success_level)

def opposed_check(char1_data, char1_skill, char2_data, char2_skill):
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
        "Extreme Success": 4,
        "Hard Success": 3,
        "Regular Success": 2,
        "Failure": 1,
        "Fumble": 0
    }

    # Convert success levels to numerical values
    char1_level = success_levels[char1_success]
    char2_level = success_levels[char2_success]

    # Compare success levels
    if char1_level > char2_level:
        return f"{char1_data['name']} wins the opposed check"
    elif char2_level > char1_level:
        return f"{char2_data['name']} wins the opposed check"
    else:
        # If same success level, compare the margins of success
        char1_margin = get_skill_value(char1_data, char1_skill) - char1_roll
        char2_margin = get_skill_value(char2_data, char2_skill) - char2_roll

        if char1_margin > char2_margin:
            return f"{char1_data['name']} wins the opposed check (better margin)"
        elif char2_margin > char1_margin:
            return f"{char2_data['name']} wins the opposed check (better margin)"
        else:
            return "The opposed check results in a tie"

def get_skill_value(character_data, skill_name):
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
    if 'skills' in character_data and skill_name in character_data['skills']:
        return character_data['skills'][skill_name]
    elif skill_name in character_data['attributes']:
        return character_data['attributes'][skill_name]
    else:
        raise ValueError(f"Skill or attribute '{skill_name}' not found for this character")

def roll_damage(weapon_data):
    """
    Calculate damage for a weapon attack based on its damage formula.

    Handles various damage formulas including those with character damage bonuses.

    Args:
        weapon_data (dict): The weapon dictionary containing the damage formula

    Returns:
        int or str: The calculated damage result or the damage formula if it can't be calculated
    """
    try:
        # Try to roll the damage directly using the new parser
        damage_formula = weapon_data['damage']

        # Handle common damage bonus pattern
        if '+1D4' in damage_formula:
            # Split formula at the bonus
            parts = damage_formula.split('+1D4')
            base_formula = parts[0]

            # Roll the base damage and bonus separately
            base_damage = dr.roll_dice(base_formula)
            bonus_damage = dr.roll_dice('1D4')

            return base_damage + bonus_damage
        else:
            # Use the new parser for standard formulas
            return dr.roll_dice(damage_formula)
    except ValueError:
        # If parsing fails, return the original formula
        return weapon_data['damage']