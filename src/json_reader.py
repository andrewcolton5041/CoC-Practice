"""
JSON Reader
This module provides a function to read JSON character files and return their contents.

Author: Andrew C
Version: 1.0
Last Updated: 3/31/2025
"""

import json
from src.constants import FileFlags, JSONReaderConst, CharacterSheetKeys, Extra

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
    with open(filename, FileFlags.READ_FLAG) as f:
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
    print(JSONReaderConst.TOP_DIVIDER)
    print(JSONReaderConst.character_name(character_data[CharacterSheetKeys.NAME]))
    print(JSONReaderConst.character_age(character_data[CharacterSheetKeys.AGE]))
    print(JSONReaderConst.character_occupation(character_data.get(CharacterSheetKeys.OCCUPATION, Extra.UNKNOWN)))
    print(JSONReaderConst.character_nationality(character_data.get(CharacterSheetKeys.NATIONALITY, Extra.UNKNOWN)))

    # Print character attributes
    print(JSONReaderConst.ATTRIBUTES_DIVIDER)
    for attr, value in character_data[CharacterSheetKeys.ATTRIBUTES].items():
        print(JSONReaderConst.character_sheet_att_ski_printer(attr,value))

    # Print character skills if available
    if CharacterSheetKeys.SKILLS in character_data:
        print(JSONReaderConst.SKILLS_DIVIDER)
        for skill, value in character_data[CharacterSheetKeys.SKILLS].items():
            print(JSONReaderConst.character_sheet_att_ski_printer(skill,value))

    # Print character weapons if available
    if CharacterSheetKeys.WEAPONS in character_data:
        print(JSONReaderConst.WEAPONS_DIVIDER)
        for weapon in character_data[CharacterSheetKeys.WEAPONS]:
            print(JSONReaderConst.character_sheet_weapons(weapon[CharacterSheetKeys.NAME],weapon[CharacterSheetKeys.SKILLS], weapon[CharacterSheetKeys.DAMAGE]))

    # Print character backstory if available
    if CharacterSheetKeys.BACKSTORY in character_data:
        print(JSONReaderConst.BACKSTORY_DIVIDER)
        print(character_data[CharacterSheetKeys.BACKSTORY])

    # Print closing divider
    print(JSONReaderConst.BOTTOM_DIVIDER)