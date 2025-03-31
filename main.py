"""
Call of Cthulhu Character Viewer

This is the main module for a Call of Cthulhu character management application.
It provides functionality to:
- Load premade characters from JSON files
- Display character information in a formatted way
- Navigate through a menu-based interface

This application can be used by game masters and players to quickly access
character information for the Call of Cthulhu roleplaying game.

Author: Unknown
Version: 1.0
Last Updated: Unknown
"""

import os
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

def main():
    """
    Main menu function that handles user interaction with the application.

    This function displays the main menu, handles user input, and
    calls the appropriate functions based on user selection.
    """
    while True:
        # Display main menu
        print("\n=== Call of Cthulhu Character Viewer ===")
        print("1. View Premade Characters")
        print("2. Exit")

        # Get user choice
        choice = input("\nEnter your choice (1-2): ")

        if choice == '1':
            # Try to list character files from the characters directory
            character_files = []
            try:
                character_files = [f for f in os.listdir('characters') if f.endswith('.json')]
            except FileNotFoundError:
                print("Characters directory not found!")
                continue

            # Check if any character files were found
            if not character_files:
                print("No character files found!")
                continue

            # Display list of available characters
            print("\n--- Available Characters ---")
            for i, filename in enumerate(character_files, 1):
                # Format the name nicely by removing the file extension
                name = filename.replace('.json', '').capitalize()
                print(f"{i}. {name}")

            # Add option to return to main menu
            print(f"{len(character_files) + 1}. Back to Main Menu")

            # Let user select a character
            while True:
                try:
                    selection = int(input(f"\nSelect a character (1-{len(character_files) + 1}): "))

                    # Handle valid character selection
                    if 1 <= selection <= len(character_files):
                        # Load and display the selected character
                        filename = os.path.join('characters', character_files[selection - 1])
                        character_data = load_character_from_json(filename)
                        display_character(character_data)

                        # Wait for user to press Enter before returning to menu
                        input("Press Enter to continue...")
                        break
                    # Handle return to main menu
                    elif selection == len(character_files) + 1:
                        break
                    else:
                        print("Invalid selection.")
                except ValueError:
                    print("Please enter a valid number.")

        elif choice == '2':
            # Exit the application
            print("Exiting program. Goodbye!")
            break

        else:
            # Handle invalid main menu choice
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()