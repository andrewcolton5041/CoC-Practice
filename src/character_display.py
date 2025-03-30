"""Character Display Module for Call of Cthulhu Character Viewer

Handles formatting and displaying character information in a consistent way.
"""

from src.constants import (
    MAX_ATTRIBUTE_VALUE,
    HIGH_THRESHOLD,
    LOW_THRESHOLD,
    SEPARATOR_WIDTH
)

def format_attribute_value(value, max_value=MAX_ATTRIBUTE_VALUE):
    """Format an attribute value for display with visual indicators."""
    # Ensure the value is converted to an integer
    try:
        value = int(value)
    except (ValueError, TypeError):
        return str(value)

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

    # Safely get values with default fallbacks
def safe_get(data, key, default='Unknown'):
    return str(data.get(key, default)) if data else default

print("\n" + "=" * SEPARATOR_WIDTH)
print(f"Name: {safe_get(character_data, 'name')}")
print(f"Age: {safe_get(character_data, 'age')}")
print(f"Occupation: {safe_get(character_data, 'occupation')}")
print(f"Nationality: {safe_get(character_data, 'nationality')}")

# Display Attributes
attributes = character_data.get('attributes', {})
if attributes:
    print("\n--- Attributes ---")
    for attr, value in attributes.items():
        print(f"{attr}: {format_attribute_value(value)}")

# Display Skills
skills = character_data.get('skills', {})
if skills:
    print("\n--- Skills ---")
    for skill, value in sorted(skills.items()):
        print(f"{skill}: {value}")

# Display Weapons
weapons = character_data.get('weapons', [])
if weapons:
    print("\n--- Weapons ---")
    for weapon in weapons:
        # Safely handle weapon details
        name = weapon.get('name', 'Unknown Weapon')
        skill = weapon.get('skill', 'N/A')
        damage = weapon.get('damage', 'N/A')
        print(f"{name} - Skill: {skill} - Damage: {damage}")

# Display Backstory
backstory = safe_get(character_data, 'backstory')
if backstory and backstory != 'Unknown':
    print("\n--- Backstory ---")
    print(backstory)

# Display Description
description = safe_get(character_data, 'description')
if description and description != 'Unknown':
    print("\n--- Description ---")
    print(description)

# Display Traits
traits = safe_get(character_data, 'traits')
if traits and traits != 'Unknown':
    print("\n--- Traits ---")
    print(traits)

# Display Ideology
ideology = safe_get(character_data, 'ideology')
if ideology and ideology != 'Unknown':
    print("\n--- Ideology/Beliefs ---")
    print(ideology)

# Display Treasured Possession
treasured_possession = safe_get(character_data, 'treasuredPossession')
if treasured_possession and treasured_possession != 'Unknown':
    print("\n--- Treasured Possession ---")
    print(treasured_possession)

# Display Notes
notes = safe_get(character_data, 'notes')
if notes and notes != 'Unknown':
    print("\n--- Notes ---")
    print(notes)

print("=" * SEPARATOR_WIDTH + "\n")