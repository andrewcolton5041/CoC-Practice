"""
Character Display Module for Call of Cthulhu Character Viewer

This module handles the formatting and display of character information,
providing consistent representation of character data in the console.

The module focuses solely on character display logic, separated from
user interface interaction and character data loading.

Author: Unknown
Version: 1.0
Last Updated: 2025-03-30
"""


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

    Returns:
        None
    """
    if not character_data:
        print("Error: No character data to display.")
        return

    # Print divider line and basic character information
    print("\n" + "=" * 50)
    print(f"Name: {character_data['name']}")
    print(f"Age: {character_data.get('age', 'Unknown')}")
    print(f"Occupation: {character_data.get('occupation', 'Unknown')}")
    print(f"Nationality: {character_data.get('nationality', 'Unknown')}")

    # Print character attributes
    print("\n--- Attributes ---")
    for attr, value in character_data.get('attributes', {}).items():
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
            print(
                f"{weapon['name']} - Skill: {weapon['skill']} - Damage: {weapon['damage']}"
            )

    # Print character backstory if available
    if 'backstory' in character_data:
        print("\n--- Backstory ---")
        print(character_data['backstory'])

    # Print character description if available
    if 'description' in character_data:
        print("\n--- Description ---")
        print(character_data['description'])

    # Print character traits if available
    if 'traits' in character_data:
        print("\n--- Traits ---")
        print(character_data['traits'])

    # Print character ideology if available
    if 'ideology' in character_data:
        print("\n--- Ideology/Beliefs ---")
        print(character_data['ideology'])

    # Print treasured possession if available
    if 'treasuredPossession' in character_data:
        print("\n--- Treasured Possession ---")
        print(character_data['treasuredPossession'])

    # Print any notes if available
    if 'notes' in character_data:
        print("\n--- Notes ---")
        print(character_data['notes'])

    # Print closing divider
    print("=" * 50 + "\n")


def display_character_summary(metadata):
    """
    Display a brief summary of a character based on metadata.

    This function is used for showing character information in lists
    without loading the full character data.

    Args:
        metadata (CharacterMetadata): Metadata object containing basic character info

    Returns:
        None
    """
    print(f"{metadata.name} - {metadata.occupation} ({metadata.nationality})")


def format_attribute_value(value, max_value=100):
    """
    Format an attribute value for display, potentially with visual indicators.

    Args:
        value (int): The attribute value to format
        max_value (int, optional): The maximum possible value. Defaults to 100.

    Returns:
        str: Formatted attribute value string
    """
    # Basic formatting
    formatted_value = str(value)

    # Optional: Add visual indicators for very high or low values
    if value >= max_value * 0.9:  # 90% or more of max
        formatted_value = f"{formatted_value} (Exceptional)"
    elif value <= max_value * 0.2:  # 20% or less of max
        formatted_value = f"{formatted_value} (Poor)"

    return formatted_value


def format_skill_value(value):
    """
    Format a skill value for display, including success thresholds.

    In Call of Cthulhu, skill checks succeed on rolls <= skill value,
    with special success levels at half and one-fifth the skill value.

    Args:
        value (int): The skill value to format

    Returns:
        str: Formatted skill value string with success thresholds
    """
    regular = value
    hard = value // 2
    extreme = value // 5

    return f"{value} (Hard: {hard}, Extreme: {extreme})"


def display_cache_stats(stats):
    """
    Display statistics about the character cache in a formatted way.

    Args:
        stats (dict): Dictionary with cache statistics

    Returns:
        None
    """
    print("\n--- Cache Status ---")
    print(f"Characters in cache: {stats['size']}")
    print(f"Maximum cache size: {stats['max_size']}")
    print(f"Approximate memory usage: {stats['memory_usage']} bytes")

    # Display hit rate statistics
    total_accesses = stats.get('hits', 0) + stats.get('misses', 0)
    if total_accesses > 0:
        print(f"Cache hit rate: {stats.get('hit_rate', 0):.1f}% ({stats.get('hits', 0)} hits, {stats.get('misses', 0)} misses)")

    if stats['size'] > 0:
        print("\nCached characters:")
        for i, char_file in enumerate(stats['files'], 1):
            print(f"{i}. {char_file}")

        if 'oldest_entry_age' in stats:
            print(f"\nOldest entry age: {stats['oldest_entry_age']:.1f} seconds")
            print(f"Newest entry age: {stats['newest_entry_age']:.1f} seconds")
    else:
        print("\nNo characters in cache.")