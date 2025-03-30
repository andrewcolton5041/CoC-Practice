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
Version: 1.1
Last Updated: 2025-03-30
"""

import os
import json
import os.path
import sys

# Global cache for storing loaded character data
character_cache = {}


def load_character_from_json(filename):
    """
    Load a premade character from a JSON file with intelligent caching.

    Checks if the character is already in the cache and if the file hasn't changed.

    Args:
        filename (str): Path to the JSON file containing character data

    Returns:
        dict: Dictionary containing the character data or None if file cannot be loaded

    Raises:
        FileNotFoundError: If the file doesn't exist
        PermissionError: If the file cannot be accessed due to permissions
        json.JSONDecodeError: If the file contains invalid JSON
    """
    # Get the file's last modification time
    try:
        mod_time = os.path.getmtime(filename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except PermissionError:
        print(f"Error: No permission to access '{filename}'.")
        return None
    except OSError as e:
        print(f"Error accessing '{filename}': {e}")
        return None

    # Check if file is in cache and if cached version is still current
    if filename in character_cache and character_cache[filename]["mod_time"] == mod_time:
        return character_cache[filename]["data"]

    # Load from file
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            character_data = json.load(f)

        # Validate required character data fields
        required_fields = ['name', 'attributes']
        for field in required_fields:
            if field not in character_data:
                print(f"Error: Missing required field '{field}' in '{filename}'.")
                return None

        # Store both the data and the modification time
        character_cache[filename] = {
            "data": character_data,
            "mod_time": mod_time
        }
        return character_data
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filename}'.")
        return None
    except Exception as e:
        print(f"Error loading character from '{filename}': {e}")
        return None


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

    # Print closing divider
    print("=" * 50 + "\n")


def invalidate_cache(filename=None):
    """
    Invalidate the character cache.

    Args:
        filename (str, optional): Specific file to remove from cache.
            If None, clears the entire cache.

    Returns:
        None
    """
    global character_cache

    if filename is None:
        # Clear the entire cache
        character_cache = {}
        print("Cache cleared successfully.")
    elif filename in character_cache:
        # Remove specific file from cache
        del character_cache[filename]
        print(f"'{filename}' removed from cache successfully.")
    else:
        print(f"'{filename}' not found in cache.")


def get_cache_status():
    """
    Get information about the current state of the character cache.

    Returns:
        dict: Dictionary with cache statistics including:
            - size: Number of characters in cache
            - characters: List of character filenames in cache
            - memory_usage: Approximate memory usage of cached data
    """
    return {
        "size": len(character_cache),
        "characters": list(character_cache.keys()),
        "memory_usage": sum(len(str(data)) for data in character_cache.values())
    }


def list_character_files():
    """
    List all character JSON files in the characters directory.

    Returns:
        list: List of character filenames, or empty list if directory not found
            or no character files exist
    """
    try:
        if not os.path.exists('characters'):
            print("Error: Characters directory not found!")
            return []

        character_files = [f for f in os.listdir('characters') if f.endswith('.json')]
        if not character_files:
            print("No character files found in the characters directory!")
        return character_files
    except PermissionError:
        print("Error: No permission to access the characters directory.")
        return []
    except Exception as e:
        print(f"Error listing character files: {e}")
        return []


def get_user_selection(prompt, min_value, max_value):
    """
    Get a numeric selection from the user within a specified range.

    Args:
        prompt (str): Prompt to display to the user
        min_value (int): Minimum acceptable value
        max_value (int): Maximum acceptable value

    Returns:
        int: User's selection as an integer, or None if user provides invalid input
    """
    while True:
        try:
            selection = input(prompt)
            # Allow empty input to return None for cancel operations
            if not selection.strip():
                return None

            selection = int(selection)
            if min_value <= selection <= max_value:
                return selection
            else:
                print(f"Invalid selection. Please enter a number between {min_value} and {max_value}.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None
        except EOFError:
            print("\nInput closed.")
            return None


def main():
    """
    Main menu function that handles user interaction with the application.

    This function displays the main menu, handles user input, and
    calls the appropriate functions based on user selection.
    Implements character caching for improved performance.

    Returns:
        None
    """
    try:
        while True:
            # Display main menu
            print("\n=== Call of Cthulhu Character Viewer ===")
            print("1. View Premade Characters")
            print("2. Clear Character Cache")
            print("3. View Cache Status")  # New option
            print("4. Exit")

            # Get user choice
            choice = get_user_selection("\nEnter your choice (1-4): ", 1, 4)

            # Handle canceled selection
            if choice is None:
                continue

            if choice == 1:
                # List character files
                character_files = list_character_files()
                if not character_files:
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
                selection = get_user_selection(
                    f"\nSelect a character (1-{len(character_files) + 1}): ", 
                    1, 
                    len(character_files) + 1
                )

                # Handle canceled selection
                if selection is None:
                    continue

                # Handle valid character selection
                if 1 <= selection <= len(character_files):
                    # Load and display the selected character (now with caching)
                    filename = os.path.join('characters', character_files[selection - 1])
                    try:
                        character_data = load_character_from_json(filename)
                        if character_data:  # Check if load was successful
                            display_character(character_data)
                    except Exception as e:
                        print(f"Error loading character: {e}")

                    # Wait for user to press Enter before returning to menu
                    try:
                        input("Press Enter to continue...")
                    except (KeyboardInterrupt, EOFError):
                        pass

            elif choice == 2:
                # Clear the character cache
                invalidate_cache()

            elif choice == 3:
                # Display cache status
                status = get_cache_status()
                print("\n--- Cache Status ---")
                print(f"Characters in cache: {status['size']}")
                print(f"Approximate memory usage: {status['memory_usage']} bytes")
                if status['characters']:
                    print("\nCached characters:")
                    for i, char_file in enumerate(status['characters'], 1):
                        print(f"{i}. {char_file}")
                else:
                    print("\nNo characters in cache.")

                # Wait for user to press Enter before returning to menu
                try:
                    input("\nPress Enter to continue...")
                except (KeyboardInterrupt, EOFError):
                    pass

            elif choice == 4:
                # Exit the application
                print("Exiting program. Goodbye!")
                break

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())