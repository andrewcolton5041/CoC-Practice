"""
JSON Reader
This module provides a function to read JSON character files and return their contents.

Author: Andrew C
Version: 1.0
Last Updated: 3/31/2025
"""

import json

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
    with open(filename, 'r') as f:
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
    print("\n" + "="*50)
    print(f"Name: {character_data['name']}")
    print(f"Age: {character_data['age']}")
    print(f"Occupation: {character_data.get('occupation', 'Unknown')}")
    print(f"Nationality: {character_data.get('nationality', 'Unknown')}")

    # Print character attributes
    print("\n--- Attributes ---")
    for attr, value in character_data['attributes'].items():
        print(f"{attr}: {value}")

    # Print character skills if available
    if 'skills' in character_data:
        print("\n--- Skills ---")
        for skill, value in character_data['skills'].items():
            print(f"{skill}: {value}")

    # Print character weapons if available
    if 'weapons' in character_data:
        print("\n--- Weapons ---")
        for weapon in character_data['weapons']:
            print(f"{weapon['name']} - Skill: {weapon['skill']} - Damage: {weapon['damage']}")

    # Print character backstory if available
    if 'backstory' in character_data:
        print("\n--- Backstory ---")
        print(character_data['backstory'])

    # Print closing divider
    print("="*50 + "\n")