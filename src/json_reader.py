"""
JSON Reader
This module provides a function to read JSON character files and return their contents.

Author: Andrew C
Version: 1.0
Last Updated: 3/31/2025
"""

import json
from src.constants import (
    FileConstants,
    UIStrings,
    CharacterSheetKeys,
    Defaults
)

def load_character_from_json(filename):
    """
    Load a premade character from a JSON file.

    Args:
        filename (str): Path to the JSON file containing character data

    Returns:
        dict: Dictionary containing the character data

    Raises:
        Various exceptions related to file operations or JSON parsing
    """
    with open(filename, FileConstants.READ_MODE) as f:
        character_data = json.load(f)
    return character_data

def display_character(character_data):
    """
    Display a character's sheet in a formatted way to the console.

    Prints all relevant character information including:
    - Basic info (name, age, occupation)
    - Attributes (STR, DEX, etc.)
    - Skills
    - Weapons
    - Backstory

    Args:
        character_data (dict): Dictionary containing the character data
    """
    # Print divider line and basic character information
    print(UIStrings.CharacterSheet.DIVIDER)
    print(UIStrings.CharacterSheet.format_header(
        character_data[CharacterSheetKeys.NAME],
        character_data[CharacterSheetKeys.AGE],
        character_data.get(CharacterSheetKeys.OCCUPATION, Defaults.UNKNOWN),
        character_data.get(CharacterSheetKeys.NATIONALITY, Defaults.UNKNOWN)
    ))

    # Print character attributes
    print(UIStrings.CharacterSheet.SECTION_ATTRIBUTES)
    for attr, value in character_data[CharacterSheetKeys.ATTRIBUTES].items():
        print(UIStrings.CharacterSheet.format_stat(attr, value))

    # Print character skills if available
    if CharacterSheetKeys.SKILLS in character_data:
        print(UIStrings.CharacterSheet.SECTION_SKILLS)
        for skill, value in character_data[CharacterSheetKeys.SKILLS].items():
            print(UIStrings.CharacterSheet.format_stat(skill, value))

    # Print character weapons if available
    if CharacterSheetKeys.WEAPONS in character_data:
        print(UIStrings.CharacterSheet.SECTION_WEAPONS)
        for weapon in character_data[CharacterSheetKeys.WEAPONS]:
            print(UIStrings.CharacterSheet.format_weapon(
                weapon[CharacterSheetKeys.WEAPON_NAME],
                weapon[CharacterSheetKeys.WEAPON_SKILL],
                weapon[CharacterSheetKeys.WEAPON_DAMAGE]
            ))

    # Print character backstory if available
    if CharacterSheetKeys.BACKSTORY in character_data:
        print(UIStrings.CharacterSheet.SECTION_BACKSTORY)
        print(character_data[CharacterSheetKeys.BACKSTORY])

    # Print closing divider
    print(UIStrings.CharacterSheet.DIVIDER)