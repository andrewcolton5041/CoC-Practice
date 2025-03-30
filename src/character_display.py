"""Character Display Module for Call of Cthulhu Character Viewer

Handles formatting and displaying character information in a consistent way.
"""

from constants import (
    MAX_ATTRIBUTE_VALUE,
    HIGH_THRESHOLD,
    LOW_THRESHOLD,
    SEPARATOR_WIDTH
)

def format_attribute_value(value, max_value=MAX_ATTRIBUTE_VALUE):
    """Format an attribute value for display with visual indicators."""
    formatted_value = str(value)
    if value >= max_value * HIGH_THRESHOLD:
        formatted_value = f"{formatted_value} (Exceptional)"
    elif value <= max_value * LOW_THRESHOLD:
        formatted_value = f"{formatted_value} (Poor)"
    return formatted_value

def display_character(character_data):
    """Display a character's sheet in a formatted way to the console."""
    if not character_data:
        print("Error: No character data to display.")
        return

    print("\n" + "=" * SEPARATOR_WIDTH)
    print(f"Name: {character_data['name']}")
    print(f"Age: {character_data.get('age', 'Unknown')}")
    print(f"Occupation: {character_data.get('occupation', 'Unknown')}")
    print(f"Nationality: {character_data.get('nationality', 'Unknown')}")

    print("\n--- Attributes ---")
    for attr, value in character_data.get('attributes', {}).items():
        print(f"{attr}: {format_attribute_value(value)}")

    if 'skills' in character_data:
        print("\n--- Skills ---")
        for skill, value in character_data['skills'].items():
            print(f"{skill}: {value}")

    if 'weapons' in character_data:
        print("\n--- Weapons ---")
        for weapon in character_data['weapons']:
            print(
                f"{weapon['name']} - Skill: {weapon['skill']} - Damage: {weapon['damage']}"
            )

    if 'backstory' in character_data:
        print("\n--- Backstory ---")
        print(character_data['backstory'])

    if 'description' in character_data:
        print("\n--- Description ---")
        print(character_data['description'])

    if 'traits' in character_data:
        print("\n--- Traits ---")
        print(character_data['traits'])

    if 'ideology' in character_data:
        print("\n--- Ideology/Beliefs ---")
        print(character_data['ideology'])

    if 'treasuredPossession' in character_data:
        print("\n--- Treasured Possession ---")
        print(character_data['treasuredPossession'])

    if 'notes' in character_data:
        print("\n--- Notes ---")
        print(character_data['notes'])

    print("=" * SEPARATOR_WIDTH + "\n")
