"""
User Interface Module for Call of Cthulhu Application

This module provides the menu-based user interface for interacting with
the Call of Cthulhu character management application.

Author: Andrew C
Version: 1.1
Last Updated: 3/31/2025
"""

import os
from src.test_runner import test_menu
from src.json_reader import display_character, load_character_from_json
from src.constants import UIStrings, FileConstants, ErrorMessages, Defaults


def display_main_menu():
    """
    Display the main menu options.

    Returns:
        None
    """
    print(UIStrings.MainMenu.TITLE)
    print(UIStrings.MainMenu.OPTION_VIEW_CHARACTER)
    print(UIStrings.MainMenu.OPTION_RUN_TESTS)
    print(UIStrings.MainMenu.OPTION_EXIT)


def run_character_view(character_files):
    """
    Run the character viewing process.

    Args:
        character_files (list): List of available character JSON files

    Returns:
        dict or None: The loaded character data or None if no character selected
    """
    # Display list of available characters
    print(UIStrings.CharacterViewer.TITLE)
    for i, filename in enumerate(character_files, 1):
        # Format the name nicely by removing the file extension
        name = filename.replace(FileConstants.JSON_EXTENSION, Defaults.EMPTY_STRING).capitalize()
        print(UIStrings.CharacterViewer.character_option(i, name))

    # Add option to return to main menu
    print(UIStrings.CharacterViewer.return_option(len(character_files) + 1))

    # Let user select a character
    while True:
        try:
            selection = int(input(UIStrings.CharacterViewer.selection_prompt(len(character_files) + 1)))

            # Handle valid character selection
            if 1 <= selection <= len(character_files):
                # Construct full file path - this is key for the test
                filename = os.path.join('characters', character_files[selection - 1])

                # Explicitly load the character data
                character_data = load_character_from_json(filename)

                # Display the character
                display_character(character_data)

                # Wait for user to press Enter before returning to menu
                input(UIStrings.CharacterViewer.CONTINUE_PROMPT)
                return character_data
            # Handle return to main menu
            elif selection == len(character_files) + 1:
                return None
            else:
                print(UIStrings.MainMenu.INVALID_CHOICE)
        except ValueError:
            print(ErrorMessages.INVALID_CHOICE)


def menu():
    """
    Display and handle the main application menu.

    Presents options to view premade characters or exit the application.
    Manages user input and calls appropriate functions based on selection.
    """
    while True:
        # Display main menu
        display_main_menu()

        # Get user choice
        try:
            choice = input(UIStrings.MainMenu.PROMPT)

            if choice == "1":  # View Character option
                # Try to list character files from the characters directory
                try:
                    character_files = [f for f in os.listdir(UIStrings.CharacterViewer.CHARACTERS_DIR) 
                                    if f.endswith(FileConstants.JSON_EXTENSION)]
                except FileNotFoundError:
                    print(ErrorMessages.CHARACTER_FILE_NOT_FOUND)
                    continue

                # Check if any character files were found
                if not character_files:
                    print(ErrorMessages.NO_CHARACTER_FILES)
                    continue

                # Run character view process
                run_character_view(character_files)

            elif choice == "2":
                # Run tests - ensure test_menu is called explicitly
                test_menu()
            elif choice == "3":  # Exit option
                # Exit the application
                print(UIStrings.MainMenu.EXIT_MESSAGE)
                break
            else:
                # Handle invalid main menu choice with exact error messaging
                print(UIStrings.MainMenu.INVALID_CHOICE)

        except ValueError:
            print(ErrorMessages.INVALID_CHOICE)


if __name__ == "__main__":
    menu()